# Created By:       Jeenal Suthar
# Created Date:
# Last Modified:    22/01/2020
# Description:      A Helper class that providers Reflection related utility functions that allows dynamic creation and calls of objects

class ReflectionUtils:
    @staticmethod
    def get_class(fq_class_name: str):
        """
        Get Class Type object from fully qualified class name such as datetime.datetime
        :return: The Class object which can be used to instantiate an instance or just like using the class directly
            in code such as:
            # instantiate a new instance
            module_()
            module_(are1, arg2,...)
        """
        parts = fq_class_name.split('.')
        top_level_module_name = ".".join(parts[:-1])
        module_ = __import__(top_level_module_name)

        for comp in parts[1:]:
            module_ = getattr(module_, comp)
        return module_

