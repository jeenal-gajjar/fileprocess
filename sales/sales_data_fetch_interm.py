import click
from pathlib import Path
import sys, os
from shutil import move, copyfile
import collections
parent_path = str(Path().resolve().parent)
if parent_path not in sys.path:
    sys.path.insert(1, str(Path().resolve().parent))
import ray
from sales.configManager import ConfigManager
from Common.db import set_db
configManager = ConfigManager.createInstance()
set_db(configManager)
ray.init(configure_logging=False, object_store_memory=100000000)
from sales.fileFetchManager import FileFetchManager
from Common.logging.loggingManager import LogManager, get_applogger
from Common.working_dir_manager import WorkingDirectoryManager
from sales.dataProviderManager import get_data_provider_manager
from Common.Utils import FileFetchException
from sales.emailManager import EmailManager
_log = get_applogger()

FileInfo = collections.namedtuple('FileInfo', 'name path size')

@ray.remote
def start_transformation(selected_file_name, working_file_path, info):
    import sys, time
    parent_path = str(Path().resolve().parent)
    if parent_path not in sys.path:
        sys.path.insert(1, str(Path().resolve().parent))
    from sales.configManager import ConfigManager
    from Common.db import set_db
    configManager = ConfigManager.createInstance()
    set_db(configManager)
    from sales.dataProviderManager import get_data_provider_manager
    from Common.logging.loggingManager import get_applogger
    _log = get_applogger()
    FileInfo = collections.namedtuple('FileInfo', 'name path size')
    start_time = time.time()

    _log.info(f"start file Processing Start : {selected_file_name} at {start_time} seconds")
    data_provider_manager = get_data_provider_manager(configManager)
    data_transformer = data_provider_manager.create_data_transformer(_log, configManager)
    move(working_file_path, working_file_path + ".old")
    data_transformer.transform_file(working_file_path + ".old", working_file_path)
    transformed_data_file = FileInfo(name=selected_file_name, path=working_file_path, size=info.st_size)
    _log.info(f"Downloaded Transformed data File {transformed_data_file}")
    destination_file_path = configManager.get_destination_file_path(transformed_data_file.name)
    _log.debug(f"Copying Transformed data file:{transformed_data_file.path} to Destination Location: {destination_file_path}")
    copyfile(transformed_data_file.path, destination_file_path)
    _log.info(f'Sales Data Files has been fetched and stored in {destination_file_path}')
    _log.info(f"file Processing End : {selected_file_name} at{time.time() - start_time} seconds")
    return True

def get_remote_data_file(file_date: str):
    with FileFetchManager(config=configManager) as file_manager:
        files_list = file_manager.list_dir()
        file_prefix= configManager.get_data_file_prefix()
        dataFileNames = []
        last_file_name = ""

        for remote_file in files_list:
            last_file_name = remote_file
            if file_prefix in remote_file and remote_file.endswith(configManager.get_data_file_extension()):
                dataFileNames.append(remote_file)

        if len(dataFileNames) > 0:
            dataFileNames.sort(reverse=True)
            result_ids = []
            backup_dict = dict()
            file_manager.create_backup_directory()

            for i in dataFileNames:
                selected_file_name = i
                info = file_manager.file_info(selected_file_name)
                source_file_path = file_manager.get_file_path(selected_file_name)
                working_file_path = os.path.join(WorkingDirectoryManager().path, selected_file_name)
                backup_file_path = file_manager.generate_backup_file(selected_file_name)
                backup_dict.update({source_file_path: backup_file_path})
                _log.debug('[]downloading remote file ' + selected_file_name)
                file_manager.get_file(source_file_path, working_file_path)
                _log.debug('[]download is complete ')
                result_ids.append(start_transformation.remote(selected_file_name, working_file_path, info))
            is_transformed = ray.get(result_ids)

            if is_transformed:
                for k, v in backup_dict.items():
                    move(k, v)
        else:
            _log.info("last proccesed file : " + last_file_name)

            raise FileFetchException(
                configManager.messageformat('Profile Data File fetch for TODAY has failed', 'no file found',True))

def send_email():
    try:
        email = EmailManager(configManager)
        print(email)
        email.send_mail()
        _log.info(f"Email send Successfully")
    except Exception as e:
        _log.error(e)


@click.command()
@click.option('--file_date', '-d', help="Profile Data File Date to fetch in YYYYMMDD format. Defaults to today",
              default=configManager.get_datepattern())
def transform_file(file_date: str):
    try:
        get_remote_data_file(file_date)
        send_email()
    except FileFetchException as e:
        raise

    except Exception as e:
        _log.error(e)


if __name__ == '__main__':
    with LogManager('Sales Data Sync', reraise_except=False):
        _log.info(f"Downloaded Data Provider File")
        with WorkingDirectoryManager(_log, configManager.get_working_directory()):
            transform_file()