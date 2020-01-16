

class DbConfigManager(object):
    """
    Contain list of common methods to get database information from config file
    Will inherit by other modules in ConfigManager class.

    """

    config = None

    def get_db_name(self):
        """
        Return the database name from config file

        :return:
        """
        return self.config.get("db", "name")

    def get_db_username(self):
        """
        Return the database username from config file

        :return:
        """
        return self.config.get("db", "user")

    def get_db_password(self):
        """
        Return the database password from config file

        :return:
        """
        return self.config.get("db", "password")

    def get_db_host(self):
        """
        Return the host name for database

        :return:
        """
        host = self.config.get('db', 'host')
        return host
