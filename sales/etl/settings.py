from typing import Dict
from Common.Utils import str_to_list
from Common import SettingsBase


class Settings(SettingsBase):
    """
    Represents Data Provider Configuration Options
    """
    CONFIG_SRC_DATA_FILE_FIELDS = "data_provider_src_fields"
    CONFIG_SRC_FIELDS_DELIMITER = "data_provider_src_fields_delimiter"
    CONFIG_SRC_ROOM_ID_FIELD = "data_provider_src_room_id_field"
    CONFIG_SRC_PRODUCT_NAME_FIELD = "data_provider_product_name_field"
    CONFIG_DATA_PROVIDER_FIELDS = "data_provider_fields"
    ERROR_INVALID_CONFIG_VALUE = "Invalid data provider configuration value: {}"

    def __init__(self, options: Dict[str, str]):
        self._options = options
        self._source_data_fields = None
        self._source_data_delimiter = None
        self._source_room_id_field = None
        self._product_name_field = None
        self._fields = None

    @property
    def source_data_fields(self):
        if not self._source_data_fields:
            value = self._options[self.CONFIG_SRC_DATA_FILE_FIELDS]
            if not value:
                raise ValueError(self.ERROR_INVALID_CONFIG_VALUE.format(self.CONFIG_SRC_DATA_FILE_FIELDS))
            self._source_data_fields = [v.title() for v in str_to_list(value, ',')]
        return self._source_data_fields

    @property
    def source_data_delimiter(self):
        if not self._source_data_delimiter:
            value = self._options[self.CONFIG_SRC_FIELDS_DELIMITER]
            if not value:
                raise ValueError(self.ERROR_INVALID_CONFIG_VALUE.format(self.CONFIG_SRC_FIELDS_DELIMITER))
            self._source_data_delimiter = value.title()
        return self._source_data_delimiter

    @property
    def fields(self):
        if not self._fields:
            value = self._options[self.CONFIG_DATA_PROVIDER_FIELDS]
            if not value:
                raise ValueError(self.ERROR_INVALID_CONFIG_VALUE.format(self.CONFIG_DATA_PROVIDER_FIELDS))
            self._fields = [v.title() for v in str_to_list(value, ',')]
        return self._fields


    @property
    def delimiter(self):
        return self.source_data_delimiter

    @property
    def source_room_id_field(self):
        if not self._source_room_id_field:
            value = self._options[self.CONFIG_SRC_ROOM_ID_FIELD]
            if not value:
                raise ValueError(
                    self.ERROR_INVALID_CONFIG_VALUE.format(self.CONFIG_SRC_ROOM_ID_FIELD))

            self._source_room_id_field = value.title()
        return self._source_room_id_field

    @property
    def product_name_field(self):
        if not self._product_name_field:
            value = self._options[self.CONFIG_SRC_PRODUCT_NAME_FIELD]
            if not value:
                raise ValueError(
                    self.ERROR_INVALID_CONFIG_VALUE.format(self.CONFIG_SRC_PRODUCT_NAME_FIELD))
            self._product_name_field = value.title()
        return self._product_name_field



