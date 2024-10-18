from acrome_wrapper import Master, Module, validate, layout


master = Master('/dev/ttyUSB0', name='Master')

motor_left = Module.add(
  master=master, smd_id=0,
  kind='Motor')
motor_right = Module.add(
  master=master, smd_id=1,
  kind='Motor')

proximity_left = Module.add(
  master=master, smd_id=0,
  kind='Distance', mod_id=1)
proximity_front = Module.add(
  master=master, smd_id=0,
  kind='Distance', mod_id=2)
proximity_right = Module.add(
  master=master, smd_id=0,
  kind='Distance', mod_id=3)

validate()

layout()
