# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This module Provide an instance of the class.

from logging import Logger
from typing import Dict
from Common.decorators.singletonDecorator import Singleton
from sales.configManager import ConfigManager
from Common.ReflectionUtils import ReflectionUtils
from Common.idatatransformer import IDataTransform


def get_data_provider_manager(configManager: ConfigManager):
    """
         Get the current Data Provider Manager
        :param configManager: Configuration Manager object
        :return: Return Data Provider Manager Singleton Instance
    """
    return DataProviderManager(configManager.get_data_provider_name(), configManager.get_data_provider_settings())


@Singleton
class DataProviderManager:
    """
       Provides high level API and abstraction over the Data Providers integration and plus-in architecture
    """
    def __init__(self, data_provider_name: str, options: Dict[str, str]):
        self._data_provider_name = data_provider_name
        self._settings = self._load_settings(options)

    def create_data_transformer(self, logger: Logger, configManager: ConfigManager) -> IDataTransform:
        """
         Create Data Provider Data Transformer Object responsible for converting the source data file to the needed schema
        :param logger: Logger instance
        :param config: Config Manager Instance
        :return: DataTransform object
        """
        concrete_cls = ReflectionUtils.get_class(self._data_provider_name + ".data_transform.DataTransform")
        return concrete_cls(logger, configManager)

    def _load_settings(self, options: Dict[str, str]):
        concrete_cls = ReflectionUtils.get_class(self._data_provider_name + ".settings.Settings")
        return concrete_cls(options)

    @property
    def settings(self):
        return self._settings



