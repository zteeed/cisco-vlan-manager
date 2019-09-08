import ipaddress

from netmiko.cisco.cisco_s300 import CiscoS300SSH

from src import log
from src.devices import ConnectedDevice


def add_vlan_switch_hackademint(handler: CiscoS300SSH, n: int, subnet: str):
    config_commands = [f'interface vlan {n}', f'name \"HackademINT {subnet}\"']
    handler.send_config_set(config_commands)
    config_commands = ['interface range po1-2', f'switchport trunk allowed vlan add {n}']
    handler.send_config_set(config_commands)


def add_vlan_switch_evryone(handler: CiscoS300SSH, n: int, subnet: str):
    config_commands = [f'interface vlan {n}', f'name \"HackademINT {subnet}\"']
    handler.send_config_set(config_commands)
    config_commands = ['interface po2', f'switchport trunk allowed vlan add {n}']
    handler.send_config_set(config_commands)
    config_commands = ['interface gi1/1/49', f'switchport trunk allowed vlan add {n}']
    handler.send_config_set(config_commands)


def remove_vlan_switch(handler: CiscoS300SSH, n: int):
    config_commands = [f'no vlan {n}']
    handler.send_config_set(config_commands)


def get_acl(subnet: str) -> str:
    subnet = ipaddress.ip_network(subnet)
    ip, netmask = subnet.network_address, subnet.netmask
    rev_mask = '.'.join([str(255 - int(group)) for group in str(netmask).split('.')])
    return f'permit {ip} {rev_mask}'


def add_vlan_router(handler: CiscoS300SSH, n: int, subnet: str):
    acl = get_acl(subnet)
    config_commands = [f'vlan {n}', f'name HackademINT-{n}']
    handler.send_config_set(config_commands)
    config_commands = [f'interface vlan {n}', f'description \"HackademINT {subnet}\"',
                       f'ip access-group HackademINT-{n} in', f'ip access-group HackademINT-{n} out']
    handler.send_config_set(config_commands)
    config_commands = [f'ip access-list standard HackademINT-{n}', f'{acl}', 'deny any']
    handler.send_config_set(config_commands)
    config_commands = ['router rip', f'passive-interface vlan {n}']
    handler.send_config_set(config_commands)
    config_commands = ['interface range po10-11', f'switchport trunk allowed vlan add {n}']
    handler.send_config_set(config_commands)
    return


def remove_vlan_router(handler: CiscoS300SSH, n: int):
    config_commands = [f'no vlan {n}']
    handler.send_config_set(config_commands)
    config_commands = [f'no interface vlan {n}']
    handler.send_config_set(config_commands)
    config_commands = [f'no ip access-list standard HackademINT-{n}']
    handler.send_config_set(config_commands)
    config_commands = ['router rip', f'no passive-interface vlan {n}']
    handler.send_config_set(config_commands)
    config_commands = ['interface range po10-11', f'switchport trunk allowed vlan remove {n}']
    handler.send_config_set(config_commands)


def add_vlan(device: ConnectedDevice, vlan_number: int, subnet: str):
    if device.name == 'Switch HackademINT':
        add_vlan_switch_hackademint(device.handler, vlan_number, subnet)
    elif device.name == 'Switch Evryone':
        add_vlan_switch_evryone(device.handler, vlan_number, subnet)
    elif device.name == 'Router Evryone':
        add_vlan_router(device.handler, vlan_number, subnet)
    else:
        log.warn('Unknown device used in add_vlan function', device=device)
        return False
    update_config(device)
    return True


def remove_vlan(device: ConnectedDevice, vlan_number: int):
    if device.name == 'Switch HackademINT':
        remove_vlan_switch(device.handler, vlan_number)
    elif device.name == 'Switch Evryone':
        remove_vlan_switch(device.handler, vlan_number)
    elif device.name == 'Router Evryone':
        remove_vlan_router(device.handler, vlan_number)
    else:
        log.warn('Unknown device used in remove_vlan function', device=device)
        return False
    update_config(device)
    return True


def update_config(device: ConnectedDevice):
    return device.handler.send_command('show run')


def save_config(device: ConnectedDevice):
    return device.handler.send_command('write memory')
