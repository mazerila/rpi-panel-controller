#!/usr/bin/env python3
import threading
import configparser
import collections
from pathlib import Path


class SingletonMeta(type):
    # This is a thread-safe implementation of Singleton.

    _instances = {}

    _lock: threading.Lock = threading.Lock()
    # We now have a lock object that will be used to synchronize threads during
    # first access to the Singleton.

    def __call__(cls, *args, **kwargs):

        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

# usage: class MatrixConfig(metaclass=SingletonMeta):



class MatrixConfig():
    configFilePath: str = None
    initialized = False
    # Configurations are loaded in 2-level dictionary: [section,[name,value]]
    sectionDict = None
        
    def __init__(self, path: str = r'configs/matrix.cfg') -> None:
        self.configFilePath = path
        self.__loadMatrixConfigs()

    def __loadMatrixConfigs(self) -> None:
        if not self.initialized :
            # load configs for first time
            if Path(self.configFilePath).is_file():
                config = configparser.RawConfigParser()
                config.read(self.configFilePath)
                self.initialized = True
            
            self.sectionDict = collections.defaultdict()

            if self.initialized :
                for section in config.sections():
                    self.sectionDict[section] = dict(config.items(section))

    def reloadMatrixConfigs(self) -> None:
        self.initialized = False
        self.__loadMatrixConfigs()
    
    def displayConfigs(self):
        if self.initialized:
            for name, value in self.sectionDict.items():
                print (f'\nsection {name!r}')
                for name, value in self.sectionDict[name].items():
                    print (f'   {name:24} = {value}')
        else:
            print('Configurations are not initialized')


# Test code
'''
conf1 = MatrixConfig(r'rpi-panel-controller/configs/matrix.cfg')
conf1.displayConfigs()
conf1.reloadMatrixConfigs(r'rpi-panel-controller/matrix2.cfg')
if conf1.initialized :
    print('1-->', conf1.sectionDict['GENERAL']['led-display-height'])
'''


