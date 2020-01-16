'''
Copyright (c) Noqoush Mobile Media Group FZ LLC - All Rights Reserved Proprietary and confidential
Unauthorized copying of this file, via any medium is strictly prohibited
This file is subject to the terms and conditions defined in file 'LICENSE.txt',
which is part of this source code package.
'''

from logging import Logger
from typing import Any, Dict
from Common.decorators.singletonDecorator import Singleton
from sales.configManager import ConfigManager
from Common.ReflectionUtils import ReflectionUtils
from Common.idatatransformer import IDataTransform


def get_data_provider_manager(configManager: ConfigManager):
    return DataProviderManager(configManager.get_data_provider_name(), configManager.get_data_provider_settings())


@Singleton
class DataProviderManager:
    def __init__(self, data_provider_name: str, options: Dict[str, str]):
        self._data_provider_name = data_provider_name
        self._settings = self._load_settings(options)

    def create_data_transformer(self, logger: Logger, configManager: ConfigManager) -> IDataTransform:
        concrete_cls = ReflectionUtils.get_class(self._data_provider_name + ".data_transform.DataTransform")
        return concrete_cls(logger, configManager)

    def _load_settings(self, options: Dict[str, str]):
        concrete_cls = ReflectionUtils.get_class(self._data_provider_name + ".settings.Settings")
        return concrete_cls(options)

    @property
    def settings(self):
        return self._settings



