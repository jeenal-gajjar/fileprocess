# Jeenal Suthar

class SettingsBase:
    @property
    def fields(self):
        pass

    @property
    def op_uid_field(self):
        pass

    @property
    def uid_field(self):
        return 'uid' #REMOVE_ME: implement this properly

    @property
    def delimiter(self):
        pass