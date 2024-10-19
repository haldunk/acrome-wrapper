'''Demonstration of how to setup communication Master(s)

There are three different ways to define Master objects:
- Individually which provides the ability to set baud rate individually
- In bulk using a list of serial device paths
- In bulk using a dictionary of master name and device paths.

'''

from typing import List
import argparse
from acrome_wrapper import Master



METHODS = [
  'individually',
  'by-dev-list',
  'by-dev-dict',
]
  
  
def get_arguments():
  parser = argparse.ArgumentParser(
    prog='master_setup',
    description='Master setup demonstration')
  parser.add_argument(
    'method', nargs='?',
    default='individually', choices=METHODS,
    help='Method to use to setup masters')
  return parser.parse_args()


def setup_individually() -> Master:
  return Master.add(
    '/dev/ttyUSB0',
    baudrate=112500,
    name='USB0'
  )


def setup_by_dev_list() -> List[Master]:
  masters = ['/dev/ttyUSB0']
  return Master.add(masters, baudrate=112500)

  
def setup_by_dev_dict() -> List[Master]:
  masters = {'USB0': '/dev/ttyUSB0'}
  return Master.add(masters, baudrate=112500)

  
def list_masters():
  print("Masters:")
  for master in Master.all():
    print(f" {master.name[:12]:<12s}")
    print(f"   device: {master.device_path:<s}")
    print(f"   baud  : {master.baudrate:,d} bps")
    

if __name__ == '__main__':
  args = get_arguments()

  print(f"Using method: {args.method}")
  match args.method:
    case 'individually':
      setup_individually()
    case 'by-dev-list':
      setup_by_dev_list()
    case 'by-dev-dict':
      setup_by_dev_dict()
    case _:
      raise Exception(
        f"Unknown method: {args.method}")

  list_masters()
  

  
