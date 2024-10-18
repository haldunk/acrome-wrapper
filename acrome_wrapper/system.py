'''System level management'''

from .module import Module
from .master import Master


__all__ = [
  'MissingPhysicalModule',
  'discover',
  'layout',
  'validate',
  'setup',
  'clear',
]



class MissingPhysicalModule(Exception):

  def __init__(self, hashes):
    super().__init__(
      "Missing physical modules: {}".format(
        ', '.join([m.name for m in hashes.values()])))



def discover():
  Module.clear()
  for master in Master.all():
    master.discover()

        
def layout(prefix:str=''):
  for master in Master.all():
    master.layout(prefix=prefix)
    

def validate():
  '''Validates manually setup module system'''
  hashes = {m.hash: m for m in Module.all()}
  def remove_hash(master, smd_id, kind, mod_id=None):
    hash = "{}:{}:{}:{}".format(
      master.device_path, smd_id, kind, mod_id or '-')
    try:
      hashes.pop(hash)
    except KeyError:
      pass
  for master in Master.all():
    for smd_id in master.scan():
      remove_hash(master, smd_id, 'Motor')
      module_labels = \
        master.scan_modules(smd_id) or []
      for module_label in module_labels:
        kind, mod_id = module_label.split('_')
        remove_hash(master, smd_id, kind, mod_id)
  if hashes:
    raise MissingPhysicalModule(hashes)
  else:
    return True


def setup():
  '''Sweeps all modules in the system and executes their
  start-up hardware setup methods'''
  for module in Module.all():
    module.setup()
    
        
def clear():
  Module.clear()
  Master.clear()
