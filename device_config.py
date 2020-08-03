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


class DeviceConfig(metaclass=SingletonMeta):
    configFilePath: str = None
    initialized = False
    # Configurations are loaded in 2-level dictionary: [section,[name,value]]
    sectionDict = None
    
    provisioningHost: str = None
    azureHostUrl: str = None
    idScope: str = None
    registrationId: str = None
    symmetricKey: str = None
    
    def __init__(self, path: str = r'device.cfg') -> None:
        self.configFilePath = path
        self.__loadDeviceConfigs()

    def __loadDeviceConfigs(self) -> None:
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
                    
        if 'provisioning-host' in self.sectionDict['SERVER'].keys():
            self.provisioningHost = self.sectionDict['SERVER']['provisioning-host']
        if 'azure-host-url' in self.sectionDict['SERVER'].keys():
            self.azureHostUrl = self.sectionDict['SERVER']['azure-host-url']
        if 'id-scope' in self.sectionDict['DEVICE'].keys():
            self.idScope = self.sectionDict['DEVICE']['id-scope']
        if 'registration-id' in self.sectionDict['DEVICE'].keys():
            self.registrationId = self.sectionDict['DEVICE']['registration-id']
        if 'symmetric-key' in self.sectionDict['DEVICE'].keys():
            self.symmetricKey = self.sectionDict['DEVICE']['symmetric-key']

    def reloadDeviceConfigs(self) -> None:
        self.initialized = False
        self.__loadDeviceConfigs()
    
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
conf1 = DeviceConfig(r'device.cfg')
conf1.displayConfigs()
conf1.reloadDeviceConfigs()
conf1.displayConfigs()
if conf1.initialized :
    print('1-->', conf1.provisioningHost)
    print('1-->', conf1.azureHostUrl)
    print('2-->', conf1.idScope)
    print('3-->', conf1.registrationId)
    print('4-->', conf1.symmetricKey)
'''