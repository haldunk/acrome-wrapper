'''Demonstration of motor module use

'''

from acrome_wrapper import Master, discover, setup, layout, Motor



if __name__ == '__main__':

  # Setup system hardware abstraction layer
  print("Setting up system abstraction layer...", end="", flush=True)
  Master('/dev/ttyUSB0', baudrate=112500, name='USB0')
  discover()
  setup()
  print("done.")

  # Get the target motor for use
  motor = Motor.get(mod_id=0)
  motor.name = 'Motor'

  # Print out the system architecture
  layout()
  print()

  # Print out initial state of the motor
  print("Initial state of the motor:")
  print("Status : {}".format('ENABLED' if motor.is_enabled else 'DISABLED'))
  print(f"Mode   : {motor.mode}")
  print(f"Supply : {motor.supply_voltage:>4.1f}")
  print(f"Voltage: {motor.get_voltage():>4.1f}")
  print()
