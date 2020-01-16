import click
from pathlib import Path
import sys, os
os.chdir(sys.path[0])
from shutil import move, copyfile
import collections
import ray
ray.init(configure_logging=False, object_store_memory=100000000)

parent_path = str(Path().resolve().parent)
if parent_path not in sys.path:
    sys.path.insert(1, str(Path().resolve().parent))
from sales.configManager import ConfigManager
from Common.db import set_db
configManager = ConfigManager.createInstance()
set_db(configManager)
from sales.fileFetchManager import FileFetchManager
from Common.logging.loggingManager import LogManager, get_applogger
from Common.working_dir_manager import WorkingDirectoryManager
from sales.dataProviderManager import get_data_provider_manager
from Common.Utils import FileFetchException
_log = get_applogger()

FileInfo = collections.namedtuple('FileInfo', 'name path size')

@ray.remote
def  ray_fun(dataFileNames, file_manager):
    for i in dataFileNames:
        selected_file_name = i
        info = file_manager.file_info(selected_file_name)
        source_file_path = file_manager.get_file_path(selected_file_name)
        working_file_path = os.path.join(WorkingDirectoryManager().path, selected_file_name)
        _log.debug('[]downloading remote file ' + selected_file_name)
        file_manager.get_file(source_file_path, working_file_path)
        _log.debug('[]download is complete ')
        data_provider_manager = get_data_provider_manager(configManager)
        data_transformer = data_provider_manager.create_data_transformer(_log, configManager)
        move(working_file_path, working_file_path + ".old")
        data_transformer.transform_file(working_file_path + ".old", working_file_path)
        transformed_data_file = FileInfo(name=selected_file_name, path=working_file_path, size=info.st_size)
        _log.info(f"Downloaded Data Provider File {transformed_data_file}")
        destination_file_path = configManager.get_destination_file_path(transformed_data_file.name)
        _log.debug(f"Copying data file:{transformed_data_file.path} to master location: {destination_file_path}")
        copyfile(transformed_data_file.path, destination_file_path)
        _log.info(f'Profile Data File for TODAY has  been fetched and stored in {destination_file_path}')
        backup_file_path = file_manager.generate_backup_file(selected_file_name)
        move(source_file_path, backup_file_path)

def get_remote_data_file(file_date: str):
    with FileFetchManager(config=configManager) as file_manager:
        file_manager.create_backup_directory()
        files_list = file_manager.list_dir()
        print(files_list)
        file_prefix= configManager.get_data_file_prefix()
        dataFileNames = []
        last_file_name = ""
        for remote_file in files_list:
            last_file_name = remote_file
            if file_prefix in remote_file and \
                    remote_file.endswith(configManager.get_data_file_extension()):
                dataFileNames.append(remote_file)
        if len(dataFileNames) > 0:
            dataFileNames.sort(reverse=True)
            for i in dataFileNames:
                selected_file_name = i
                info = file_manager.file_info(selected_file_name)
                source_file_path = file_manager.get_file_path(selected_file_name)
                working_file_path = os.path.join(WorkingDirectoryManager().path, selected_file_name)
                _log.debug('[]downloading remote file ' + selected_file_name)
                file_manager.get_file(source_file_path, working_file_path)
                _log.debug('[]download is complete ')
                data_provider_manager = get_data_provider_manager(configManager)
                data_transformer = data_provider_manager.create_data_transformer(_log, configManager)
                move(working_file_path, working_file_path + ".old")
                data_transformer.transform_file(working_file_path + ".old", working_file_path)
                transformed_data_file = FileInfo(name=selected_file_name, path=working_file_path, size=info.st_size)
                _log.info(f"Downloaded Data Provider File {transformed_data_file}")
                destination_file_path = configManager.get_destination_file_path(transformed_data_file.name)
                _log.debug(f"Copying data file:{transformed_data_file.path} to master location: {destination_file_path}")
                copyfile(transformed_data_file.path, destination_file_path)
                _log.info(f'Profile Data File for TODAY has  been fetched and stored in {destination_file_path}')
                backup_file_path = file_manager.generate_backup_file(selected_file_name)
                move(source_file_path, backup_file_path)
        else:
            _log.info(
                "last proccesed file : " + last_file_name + " remote path : " + configManager.get_remote_data_directory())

            raise FileFetchException(
                configManager.messageformat('Profile Data File fetch for TODAY has failed', 'no file found',True))



@click.command()
@click.option('--file_date', '-d', help="Profile Data File Date to fetch in YYYYMMDD format. Defaults to today",
              default=configManager.get_datepattern())
def transform_file(file_date: str):
    try:
        get_remote_data_file(file_date)


    except FileFetchException as e:
        raise

    except Exception as e:
        _log.error(e)


if __name__ == '__main__':
    with LogManager('Sales Data Sync', reraise_except=False):
        _log.info(f"Downloaded Data Provider File")
        with WorkingDirectoryManager(_log, configManager.get_working_directory()):
            transform_file()