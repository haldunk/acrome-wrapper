'''Demonstration of module management.

'''

from acrome_wrapper import Master, discover, layout, Module
from acrome_wrapper import MultipleModulesFound, ModuleNotFound



if __name__ == '__main__':

  # Settin up communication gateway master(s)
  master = Master.add('/dev/ttyUSB0', baudrate=112500, name='USB0')

  # Automatic discovery of all modules in the system
  print("Executing module discovery...", end="", flush=True)
  discover()
  print("done.")
  print()

  # Print out of the entire system architecture
  print("Discovered system architecture")
  layout()
  print()

  # Accessing a list of __all__ module in the system
  print("All modules in the system:")
  for module in Module.all():
    print(f"  {module}")
  print()

  # Finding modules that satisfy a collection of conditions
  print("All modules of type MOTOR:")
  motor_modules = Module.find(kind=Module.Kind.MOTOR)
  for module in motor_modules:
    print(f"  {module}")
  print()

  # Getting a specific module satisfying a set of
  # conditions
  print("Getting MOTOR module with index 0:")
  try:
    motor_0 = Module.get(
      kind=Module.Kind.MOTOR,
      mod_id=0)
    print(f"  {motor_0}")
  except MultipleModulesFound:
    print("  Multiple matching modules found")
  except ModuleNotFound:
    print("  No matching module found")
  
  # Setting the human readable name for the last found
  # module
  motor_0.name = 'Motor 0'
  print("System architecture after the module name update")
  layout()

  # Listing of unique short form labels for modules
  print("Module short form labels:")
  for module in Module.all():
    print(f"  {module.name[:20]:<20s} - {module.label[:10]:<10s}")
