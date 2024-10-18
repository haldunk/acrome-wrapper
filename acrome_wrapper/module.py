'''Module abstraction layer

'''

from typing import List
from enum import Enum
from smd import red
from .defaults import *


__all__ = [
  'UndefinedModuleKind',
  'UnknownModuleKind',
  'MultipleModulesFound',
  'ModuleNotFound',
  'NonUniqueModuleName',
  'Module',
  'Motor',
  'Distance',
]
  

MODULES = list()


class UndefinedModuleKind(Exception):
  
  def __init__(self, module_kind):
    super().__init__(
      "Module kind is not defined: {}".format(
        module_kind or 'None'))

class UnknownModuleKind(Exception):
  
  def __init__(self, module_kind):
    super().__init__(
      "Unknown module kind: {}".format(module_kind))

class MultipleModulesFound(Exception):

  def __init__(self,
               master:'master.Master'=None,
               kind:'Module.Kind'=None,
               id:int=None):
    super().__init__(
      "Multiple modules returned for: " +
      "master: {}".format(master) if master else '' +
      "kind: {}".format(kind.value) if kind else '',
      "id: {}".format(id) if id else '',
      "name: {}".format(name) if id else '')
    
class ModuleNotFound(Exception):

  def __init__(self,
               master:'master.Master'=None,
               kind:'Module.Kind'=None,
               mod_id:int=None,
               name:str=None):
    super().__init__(
      "Module not found for: " +
      "master: {}".format(master) if master else '' +
      "kind: {}".format(kind.value) if kind else '',
      "id: {}".format(mod_id) if id else '',
      "name: {}".format(name) if id else '')
    
class NonUniqueModuleName(Exception):

  def __init__(self, name):
    super().__init__(
      "Non-unique Module name: {}".format(name))


class Option(Enum):

  @classmethod
  @property
  def choices(cls) -> list['Option']:
    return [k for k in cls]

  @classmethod
  @property
  def values(cls) -> list[str]:
    return [k.value for k in cls]
    
  @classmethod
  def member(cls, value:str) -> 'Option':
    for member in cls:
      if member.value == value:
        return member
    raise ValueError(
      'No member with value ({})'.format(value))
  
        
class Module:

  class Kind(Option):
    '''Module kind enumuration.

    The values in this enumuration come from the underlying
    acrome SMD package and should not be altered

    '''
    MOTOR = 'Motor'
    DISTANCE = 'Distance'
    BUZZER = 'Buzzer'
    SERVO = 'Servo'
    RGB = 'RGB'
    BUTTON = 'Button'
    LIGHT = 'Light'
    JOYSTICK = 'Joystick'
    QRT = 'QRT'
    POTMETER = 'Potmeter'
    IMU = 'IMU'
    
  _kind = None
  _name = None
  
  def __init__(self,
               master:'master.Master',
               smd_id:int,
               mod_id:int=None,
               name:str=None):
    '''Initializer for the module base class

    Parameters:
    master: Communication master to be used
    smd_id: ID of the SMD that the device is connected
    mod_id: Module hardware ID of the module.
            For Motor modules it is ignored.
    name  : (optional) unique string label for the module

    Raises:
    UndefinedModuleKind: if kind is not specified
    '''
    if self._kind not in Module.Kind.choices:
      raise UndefinedModuleKind(self._kind)
    self._master = master
    self._smd_id = smd_id
    self._mod_id = mod_id
    self.name = name
    MODULES.append(self)
    
  def __str__(self):
    return self.name

  def __repr__(self):
    return "Module: {:s}".format(str(self))

  @property
  def hash(self):
    return "{}:{}:{}:{}".format(
      self._master.device_path, self._smd_id,
      self._kind.value, self._mod_id or '-')
  
  @property
  def kind(self):
    return self._kind

  @property
  def master(self):
    return self._master

  @property
  def mod_id(self):
    return self._mod_id or self._smd_id
  
  @property
  def label(self):
    if self.kind == Module.Kind.MOTOR:
      return "{}".format(self._smd_id)
    else:
      return "{}:{}".format(
        self._smd_id, self._mod_id)
  
  @property
  def name(self) -> str:
    '''Returns the current module name'''
    return self._name
  
  @name.setter
  def name(self, value:str):
    '''Module name property setter. The uniqueness of the
    given name is checked during the setting process'''
    if value is None:
      value = "{}:{}[{}]".format(
        self.master.name, self.kind.value, self.label)
    if value in map(lambda m: m.name, MODULES):
      raise NonUniqueModuleName(value)
    else:
      self._name = value
  
  @staticmethod
  def clear():
    MODULES.clear()
  
  @staticmethod
  def add(master:'master.Master',
          smd_id:int,
          kind:'Module.Kind',
          mod_id:int=None,
          name:str=None) -> 'module.Module':
    '''Adds a new device into the system

    Parameters:
    master: Master used for communicating with the device
    smd_id: ID of the SMD board serving as bridge for the
            device
    kind  : Module kind (see Kind enum for available values)
    mod_id: Hardware ID assigned to the module. For MOTOR
            kind ID is None
    name  : (optional) unique string label for the module

    Returns:
    Device: device instance for the new device

    Raises:
    UnknownModuleKind: if kind in module_label is unrecognized
    '''

    match kind:
      case Module.Kind.MOTOR:
        module = Motor(
          master=master, smd_id=smd_id, name=name)
      case Module.Kind.BUZZER:
        raise NotImplementedError
      case Module.Kind.SERVO:
        raise NotImplementedError
      case Module.Kind.RGB:
        raise NotImplementedError
      case Module.Kind.BUTTON:
        raise NotImplementedError
      case Module.Kind.LIGHT:
        raise NotImplementedError
      case Module.Kind.JOYSTICK:
        raise NotImplementedError
      case Module.Kind.DISTANCE:
        module = Distance(
          master=master, smd_id=smd_id, mod_id=mod_id,
          name=name)
      case Module.Kind.QRT:
        raise NotImplementedError
      case Module.Kind.POTMETER:
        raise NotImplementedError
      case Module.Kind.IMU:
        raise NotImplementedError
      case _:
        raise UnknownModuleKind(kind)
    return module

  @staticmethod
  def all():
    '''Returns the list of all modules in the system
    abstraction'''
    return MODULES
  
  @staticmethod
  def find(master:'master.Master'=None,
           kind:'Module.Kind'=None,
           mod_id:int=None,
           name:str=None) -> list['module.Module']:
    '''Returns a list of modules satisfying conditions

    Parameters:
    master: (optional) communication gateway master
    kind  : (optional) module kind
    mod_id: (optional) module hardware index
    name  : (optional) full name of the module

    Returns:
    list of Module instances satisfying conditions
    '''
    modules = MODULES
    if master is not None:
      modules = filter(
        lambda m: m.master == master, modules)
    if kind is not None:
      modules = filter(
        lambda m: m.kind == kind, modules)
    if mod_id is not None:
      modules = filter(
        lambda m: m.mod_id == mod_id, modules)
    if name is not None:
      modules = filter(
        lambda m: m.name == name, modules)
    return list(modules)

  @staticmethod
  def get(*args, **kwargs):
    '''Returns the unique module satisfying conditions

    Parameters:
    see find()

    Returns:
    Satisfying single Module instance of None

    Raises:
    MultipleModulesFound: if more than one Module satisfies
    '''
    modules = Module.find(*args, **kwargs)
    if len(modules) == 1:
      return modules[0]
    elif len(modules) > 1:
      raise MultipleModulesFound(*args, **kwargs)
    elif not modules:
      raise ModuleNotFound(*args, **kwargs)
    else:
      return None

  def setup(self):
    '''Module specific hardware setup. If any hardware
    setup on start-up is required this method will be
    overridden by the child module class.'''
    pass
  
  
class Motor(Module):
  '''Motor driver module abstraction class.

  Note that in function calls where module id is required
  the SMD ID is used instead of MOD ID. This is a special
  case for motor modules and a direct consequence of the
  way underlying acrome library and hardware is designed.

  '''

  _kind = Module.Kind.MOTOR
  _mode = None
  _is_enabled = None
  _voltage = 0.0
  _supply_voltage = DEFAULT_SUPPLY_VOLTAGE
  
  class Mode(Option):
    '''Motor drive control modes'''
    VOLTAGE_CONTROL = red.OperationMode.PWM
    POSITION_CONTROL = red.OperationMode.Position
    VELOCITY_CONTROL = red.OperationMode.Velocity
    TORQUE_CONTROL = red.OperationMode.Torque

  class IncorrectModeError(Exception):

    def __init__(self, current_mode):
      super().__init__(
        "Cannot execute command. Current mode: {}".format(
          current.mode))

  class NotEnabledError(Exception):

    def __init__(self):
      super().__init__("Motor is not enabled")
      
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

  @staticmethod
  def all() -> List['module.Motor']:
    return Module.find(kind=Module.Kind.MOTOR)
  
  @staticmethod
  def find(master:'master.Master'=None,
           mod_id:int=None,
           name:str=None) -> list['module.Motor']:
    '''Returns a list of motor modules satisfying conditions

    Parameters:
    master: (optional) communication gateway master
    mod_id: (optional) module hardware index
    name  : (optional) full name of the module

    Returns:
    list of Module instances satisfying conditions
    '''
    return Module.find(
      master=master, kind=Module.Kind.MOTOR,
      mod_id=mod_id, name=name)

  @staticmethod
  def get(*args, **kwargs) -> 'module.Motor':
    '''Returns the unique Motor module satisfying conditions

    Parameters:
    see find()

    Returns:
    Satisfying single Motor module instance of None

    Raises:
    MultipleModulesFound: if more than one Motor module satisfies
    '''
    kwargs.update({'kind': Module.Kind.MOTOR})
    return Module.get(*args, **kwargs)
  
  def setup(self):
    '''Hardware setup for the motor module.

    By convention when a motor module is initialized the
    motor is put in voltage control mode with terminal
    voltage set to zero and the motor drive is disabled.

    '''
    self.mode = Motor.Mode.VOLTAGE_CONTROL
    self.set_voltage(0.0, forced=True)

  def _get_is_enabled(self):
    '''Updates the internally stored motor drive enable
    state.'''
    try:
      self._is_enabled = bool(self._master.get_variables(
        id=self._smd_id,
        index_list=[red.Index.TorqueEnable])[0])
    except TypeError:
      pass

  @property
  def is_enabled(self) -> bool:
    '''Updates the motor drive enable state and returns it'''
    self._get_is_enabled()
    return self._is_enabled
  
  def enable(self):
    '''Enables motor driver.'''
    self._master.enable_torque(
      id=self._smd_id, en=True)
    self._is_enabled = True

  def disable(self):
    '''Disables motor driver.'''
    self._master.enable_torque(
      id=self._smd_id, en=False)
    self._is_enabled = False

  def _get_mode(self):
    '''Updates the internally managed motor drive mode
    register'''
    self._mode = Motor.Mode.member(
      self._master.get_operation_mode(id=self._smd_id))
  
  @property
  def mode(self) -> 'Motor.Mode':
    '''Acquires the the currently active mode from motor drive
    hardware and returns it'''
    self._get_mode()
    return self._mode

  @mode.setter
  def mode(self, operation:'Motor.Mode'):
    '''Sets the operation mode of the motor drive hardware.

    By convention the motor drive is disabled when mode is
    changed. If the requested mode is the same with the
    current mode no action is taken.

    '''
    if self._mode == operation:
      return
    self.disable()
    self._mode = operation
    self._master.set_operation_mode(
      id=self._smd_id, mode=operation.value)

  @property
  def supply_voltage(self) -> float:
    '''Returns the currently set supply voltage'''
    return self._supply_voltage
    
  @supply_voltage.setter
  def supply_voltage(self, voltage:float):
    '''Sets the supply voltage setting
    Args:
      voltage: Supply voltage in volts
    '''
    assert voltage > 0.0, \
      'Supply voltage must be a positive value'
    self._supply_voltage = voltage
    
  def set_voltage(self,
                  voltage:float,
                  forced:bool=False) -> float:
    '''Sets the motor terminal voltage. Requires the
    current control mode to be VOLTAGE_CONTROL otherwise
    raises IncorrectModeError exception. If the motor is
    not enabled NotEnabled exception is raised.
    
    Args:
      voltage: (float) Voltage in volts
      forced: (bool) If True ignore drive enable state
    Return:
      Actual voltage generated (after clapping)

    '''
    if self._mode != Motor.Mode.VOLTAGE_CONTROL:
      raise Motor.IncorrectModeError(self._mode)
    if not forced and not self._is_enabled:
      raise Motor.NotEnabledError
    duty_cycle = voltage / self._supply_voltage * 100.0
    duty_cycle = max(-100.0, min(duty_cycle, 100.0))
    self._master.set_duty_cycle(
      id=self._smd_id, pct=duty_cycle)
    self._voltage = duty_cycle * 0.01 * self._supply_voltage
    return self._voltage

  def get_voltage(self) -> float:
    '''Returns the currently applied motor terminal
    voltage. Requires the current control mode to be
    VOLTAGE_CONTROL otherwise raises IncorrectModeError
    excetion.'''
    if self._mode != Motor.Mode.VOLTAGE_CONTROL:
      raise Motor.IncorrectModeError(self._mode)
    return self._voltage

  
class Distance(Module):

  _kind = Module.Kind.DISTANCE

  @staticmethod
  def all() -> List['module.Distance']:
    '''Returns a list of all distance modules'''
    return Module.find(kind=Module.Kind.DISTANCE)
  
  @staticmethod
  def find(master:'master.Master'=None,
           mod_id:int=None,
           name:str=None) -> list['module.Distance']:
    '''Returns a list of distance modules satisfying conditions

    Parameters:
    master: (optional) communication gateway master
    mod_id: (optional) module hardware index
    name  : (optional) full name of the module

    Returns:
    list of Distance instances satisfying conditions
    '''
    return Module.find(
      master=master, kind=Module.Kind.DISTANCE,
      mod_id=mod_id, name=name)

  @staticmethod
  def get(*args, **kwargs) -> 'module.Distance':
    '''Returns the unique Distance module satisfying conditions

    Parameters:
    see find()

    Returns:
    Satisfying single Distance module instance of None

    Raises:
    MultipleModulesFound: if more than one Distance module satisfies
    '''
    kwargs.update({'kind': Module.Kind.DISTANCE})
    return Module.get(*args, **kwargs)
  
  def setup(self):
    '''Hardware setup for the distance module.
    '''
    pass

  
  def measure(self) -> int:
    '''Returns the most recent measured range.'''
    return self._master.get_distance(
      self._smd_id, self._mod_id)
    

