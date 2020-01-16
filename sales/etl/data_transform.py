import itertools
from sales.etl.settings import Settings
from Common.db.models import Product
import pandas as pd


class DataTransform:

    def __init__(self, log, config):
        self._log = log
        self.config = config
        self._data_provider_options = Settings(config.get_data_provider_settings())

    def get_schema(self):
        pass

    def _lower_first(self, iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    def _validate_schema(self, header):
        """
        Validate the given out file header. The file should include the expected fields in any order.
        :param header:
        :return:
        """
        return set(self._data_provider_options.source_data_fields) == set([s.lower() for s in header.keys()])

    def transform_file(self, in_file_path, out_file_path):
        self._log.info(f"start Transforming Profile Data file {in_file_path} to {out_file_path}")
        import time

        df = pd.read_excel(in_file_path)
        start_time = time.time()
        print("--- %s seconds ---" % (time.time() - start_time))
        df.columns = map(str.title, df.columns)
        index = self._data_provider_options.fields.index(self._data_provider_options.product_name_field) + 1
        df.insert(loc=index, column=self._data_provider_options.product_name_field, value='')
        for index, row in df.iterrows():
            try:
                a = Product.get(Product.room_id == row[self._data_provider_options.source_room_id_field]).name
                df.loc[index, self._data_provider_options.product_name_field] = a
            except:
                df.loc[index, self._data_provider_options.product_name_field] = ''
        df.to_excel(out_file_path)
        print("--- %s seconds ---" % (time.time() - start_time))
        self._log.info(f"Completed Transforming Profile Data file {in_file_path} to {out_file_path}")



