import itertools, ray
from sales.etl.settings import Settings
from Common.db.models import Product
import pandas as pd

@ray.remote
def transform_row(df):
    import sys
    from pathlib import Path
    parent_path = str(Path().resolve().parent)
    if parent_path not in sys.path:
        sys.path.insert(1, str(Path().resolve().parent))
    from sales.configManager import ConfigManager
    from sales.etl.settings import Settings
    configManager = ConfigManager.createInstance()
    from Common.db import set_db
    set_db(configManager)
    from Common.db.models import Product
    data_provider_options = Settings(configManager.get_data_provider_settings())
    for index, row in df.iterrows():
        try:
            a = Product.get(Product.room_id == row[data_provider_options.source_room_id_field]).name
            df.loc[index, data_provider_options.product_name_field] = a
        except:
            df.loc[index, data_provider_options.product_name_field] = ''
    return df

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

    # def transform_row(self, df):
    #     from Common.db.models import Product
    #     for index, row in df.iterrows():
    #         try:
    #             a = Product.get(Product.room_id == row[self._data_provider_options.source_room_id_field]).name
    #             df.loc[index, self._data_provider_options.product_name_field] = a
    #         except:
    #             df.loc[index, self._data_provider_options.product_name_field] = ''
    #     return df

    def transform_file(self, in_file_path, out_file_path):
        import time, math
        self._log.info(f"start Transforming Sales Data file {in_file_path} to {out_file_path} on {time.ctime()}")
        df = pd.read_excel(in_file_path)
        df.columns = map(str.title, df.columns)
        index = self._data_provider_options.fields.index(self._data_provider_options.product_name_field) + 1
        df.insert(loc=index, column=self._data_provider_options.product_name_field, value='')
        chunks = list()
        skip_record = math.ceil(len(df.index) / 1000)
        start_row = 1
        for i in range(0,skip_record):
            stop_row = start_row + skip_record
            df_chunk = df.loc[start_row:stop_row]
            start_row = stop_row
            if not df_chunk.shape[0]:
                break
            else:
                chunks.append(transform_row.remote(df_chunk))

        b = ray.get(chunks)
        # for index, chunk_df in df.groupby(np.arange(len(df)) // 1000):
        #     chunk_df = self.transform_row(chunk_df)
        #     a = dask.delayed(self.transform_row)(chunk_df)
        #     chunks.append(a)
        # b = dask.compute(*chunks)
        new_df = pd.concat(b)
        new_df.to_excel(out_file_path)
        self._log.info(f"Completed Transforming Sales Data file {in_file_path} to {out_file_path} on {time.ctime()}")



