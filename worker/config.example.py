from src.devices import Device

# Switch HackademINT
config_switch_hackademint = {
    'ip': '172.16.0.252',
    'device_type': 'cisco_s300',
    'username': 'username',
    'password': 'password',
    'secret': 'secret',
    'global_delay_factor': 1,
    'verbose': True
}

# Switch Evryone 
config_switch_evryone = {
    'ip': '172.16.0.254',
    'device_type': 'cisco_s300',
    'username': 'username',
    'password': 'password',
    'secret': 'secret',
    'global_delay_factor': 1,
    'verbose': True
}

# Router Evryone 
config_router_evryone = {
    'ip': '172.16.0.251',
    'device_type': 'cisco_s300',
    'username': 'username',
    'password': 'password',
    'secret': 'secret',
    'global_delay_factor': 1,
    'verbose': True
}

switch_hackademint = Device(name='Switch HackademINT', config=config_switch_hackademint)
switch_evryone = Device(name='Switch Evryone', config=config_switch_evryone)
router_evryone = Device(name='Router Evryone', config=config_router_evryone)
