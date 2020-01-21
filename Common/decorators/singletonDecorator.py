# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      This Module Provide Singleton.

class Singleton(object):

    def __init__(self, class_name):
        """

        :param className:
        """
        self.class_name = class_name
        self.instance = None

    def __call__(self, *args, **kwargs):
        """
        being called with every class instantiation
        :param args:
        :param kwargs:
        :return:
        """
        if not self.instance:
            self.instance = self.class_name(*args, **kwargs)

        return self.instance

