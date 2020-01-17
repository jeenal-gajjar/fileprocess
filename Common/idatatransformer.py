# Jeenal suthar

class IDataTransform(object):

    def transform_file(self, in_file_path, out_file_path):
        raise NotImplementedError("Must implement this Method.")

    def transform_row(self, row: dict):
        raise NotImplementedError("Must implement this Method.")

    def get_schema(self):
        raise NotImplementedError("Must implement this Method.")
