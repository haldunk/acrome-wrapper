'''Serial communication master'''

from typing import Union, List, Dict
from pathlib import Path
from smd import red
from .module import Module


__all__ = [
  'NonUniqueMasterName',
  'MasterNameConflict',
  'NoMasterSetup',
  'Master',
]


# Default serial baud rate in Hz
BAUDRATE = 112500 

# List of all communication masters in the system
MASTERS = list() 


class NonUniqueMasterName(Exception):

  def __init__(self, name):
    super().__init__(
      "Non-unique Master name: {}".format(name))
    
class MasterNameConflict(Exception):
  
  def __init__(self, device_path):
    super().__init__(
      "Master bound to {} exists".format(device_path))

class NoMasterSetup(Exception):
    
  def __init__(self):
    super().__init__("No master has set up")

  
class Master(red.Master):
  '''A customized implementation of red.Master'''

  def __init__(self,
               device_path:str,
               baudrate:int=BAUDRATE,
               name:str=None):
    '''Initializer for Master

    Parameters:
    device_path: path to the serial device
    baudrate: serial baud rate in Hz
    name: (optional) Unique name for Master

    Raises:
    NonUniqueMasterName: if there is a master with the same
    name exists

    '''
    self.device_path = device_path
    self.name = name or Path(device_path).name
    super().__init__(
      portname=device_path, baudrate=baudrate)
    MASTERS.append(self)

  @property
  def name(self):
    return self._name
  @name.setter
  def name(self, value):
    if value in map(lambda m: m.name, MASTERS):
      raise NonUniqueMasterName(value)
    else:
      self._name = value

  @property
  def device_path(self):
    return self._device_path
  @device_path.setter
  def device_path(self, value):
    if value in map(lambda m: m.device_path, MASTERS):
      raise MasterNameConflict(value)
    else:
      self._device_path = value

  @property
  def baudrate(self) -> int:
    '''Returns the current serial baud rate in Hz'''
    return self._Master__baudrate
      
  def __str__(self):
    return self.name

  def __repr__(self):
    return 'Master: {}'.format(self.name)
  
  def discover(self):
    for smd_id in self.scan():
      Module.add(
        master=self, smd_id=smd_id, kind=Module.Kind.MOTOR)
      module_labels = self.scan_modules(smd_id) or []
      for module_label in module_labels:
        kind_name, index = module_label.split('_')
        kind = Module.Kind.member(kind_name)
        Module.add(master=self, smd_id=smd_id,
                   kind=kind, mod_id=int(index))

  def layout(self, prefix=''):
    print(prefix, self)
    for module in Module.find(master=self):
      print(prefix, ' ', module)

  @staticmethod
  def clear():
    MASTERS.clear()
      
  @staticmethod
  def add(device_paths:Union[str, List[str], Dict[str, str]],
          baudrate:int=BAUDRATE,
          name:str=None) -> Union['Master', List['Master']]:
    if isinstance(device_paths, str):
      return Master(
        device_path=device_paths, baudrate=baudrate, name=name)
    elif isinstance(device_paths, list):
      return [
        Master(device_path=path, baudrate=baudrate)
        for path in device_paths]
    elif isinstance(device_paths, dict):
      return [
        Master(device_path=path, baudrate=baudrate, name=name)
        for name,path in device_paths.items()]
    else:
      raise Exception(
        '''device_paths must be a string representing the
        device path or a list of device path strings or
        dictionary of names mapped to device paths.''')
      
  @staticmethod
  def all():
    if MASTERS:
      return MASTERS
    else:
      raise NoMasterSetup

