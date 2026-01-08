class ClassicSingleton:
    _instance = None

    def __init__(self):
        #raise an error everytime someone tries to access this class from an instance other than itself
        raise RuntimeError('Call get_instance() instead')

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = cls.__new__(cls)
        return cls._instance
# to not here __init__ is not a constructor but an initializer
# __new__ is the actual constructor
# this is a bad implementation though, its not the best way for python

class Singleton:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

# here we will directly override the new method which creates the instance

class SingletonMeta(type):
    _instances = {}
    def __init__(cls):
        super().__init__()
        cls._instances[cls] = super().__call__()
    def __call__(cls, *args, **kwargs):
        return cls._instances[cls]

class SingletonMetaClass(metaclass=SingletonMeta):
    def __init__(self):
        print('Object initialised')

