'''Demonstration of automatic module discovery.

'''

from acrome_wrapper import Master, discover, layout


if __name__ == "__main__":

  # Setup gateway master(s) in the system
  Master.add('/dev/ttyUSB0', baudrate=112500, name='acrome')

  # Execute automatic discovery of all modules attached to
  # the master(s)
  print(
    "Discovering modules attached to master(s)...",
    end="", flush=True)
  discover()
  print("done.")

  # Print out the layout of the (discovered) system
  # structure
  layout()
