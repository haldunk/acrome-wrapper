'''Demonstration of manual module setup.

This method is used for systems with known and fixed
architecture. It provides an _explicit way_ to initialize
the system without sweeping each Master network.

After module specification of the system architecture a
validation is to be executed. This is both required for the
underlying acrome API to operate properly and also provides
a sanity check for the manual setup.

'''

import sys
from acrome_wrapper import \
  Master, Module, layout, validate, MissingPhysicalModule, setup



if __name__ == '__main__':

  # Define gateway master(s) in the system
  master = Master(
    '/dev/ttyUSB0', baudrate=112500, name='USB0')

  # Manually define module(s) in the system
  motor_left = Module.add(
    master=master,
    smd_id=0,
    kind=Module.Kind.MOTOR,
    name='Left Motor')
  motor_right = Module.add(
    master=master,
    smd_id=6,
    kind=Module.Kind.MOTOR,
    name='Right Motor')

  # Print out the system architecture
  layout()

  # If requested validate the manual setup
  print("Validating the module setup...", end="", flush=True)
  try:
    validate()
    print("done.")
  except MissingPhysicalModule as e:
    print("failed.")
    print(e)
    sys.exit(1)

  # Setup all module hardware
  print("Setting up module hardware...", end="", flush=True)
  setup()
  print("done.")
