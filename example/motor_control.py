'''Demonstration of motor module use

'''

import argparse
import math
from time import sleep
from acrome_wrapper import Master, discover, setup, layout, Motor


MODES = [
  'voltage',
  'position',
  'velocity',
  'torque',
]


def get_arguments():
  parser = argparse.ArgumentParser(
    prog='motor_control',
    description='Motor module demonstration')
  parser.add_argument(
    'mode', nargs='?',
    default='voltage', choices=MODES,
    help='Motor control mode to use for control')
  return parser.parse_args()
  

def execute_voltage_control(motor:Motor):
  motor.mode = Motor.Mode.VOLTAGE_CONTROL
  print("VOLTAGE control mode is set")
  motor.supply_voltage = 12.0
  motor.polarity = Motor.Polarity.NEGATIVE
  motor.enable()
  amplitude = motor.supply_voltage
  frequency = 0.1
  T = 0.1
  for t in [n*T for n in range(0, 1000)]:
    voltage = amplitude * math.sin(2*math.pi*frequency*t)
    motor.set_voltage(voltage)
    print(f"{voltage:>4.2f}")
    sleep(T)

def execute_position_control(motor:Motor):
  motor.mode = Motor.Mode.POSITION_CONTROL
  print("POSITION control mode is set")
  raise NotImplementedError

def execute_velocity_control(motor:Motor):
  motor.mode = Motor.Mode.VELOCITY_CONTROL
  print("VELOCITY control mode is set")
  raise NotImplementedError

def execute_torque_control(motor:Motor):
  motor.mode = Motor.Mode.TORQUE_CONTROL
  print("TORQUE control mode is set")
  raise NotImplementedError


if __name__ == '__main__':

  args = get_arguments()
  
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

  # Execute the selected motor control mode demonstration
  try:
    match args.mode:
      case 'voltage':
        execute_voltage_control(motor)
      case 'position':
        execute_position_control(motor)
      case 'velocity':
        execute_velocity_control(motor)
      case 'torque':
        execute_torque_control(motor)
      case _:
        raise Exception(
          f"Unknown mode selection: {args.mode}")
  except KeyboardInterrupt:
    pass

  # Deactivate the motor controller
  motor.reset()
