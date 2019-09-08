from multiprocessing.pool import ThreadPool
from typing import List, Optional

from netmiko import ConnectHandler

from config import switch_hackademint, switch_evryone, router_evryone
from src import log
from src.devices import Device, ConnectedDevice


def get_device_enabled(cisco_device: Device) -> Optional[ConnectedDevice]:
    cisco_config = cisco_device.config
    if 'secret' not in cisco_config.keys():
        return

    try:
        device = ConnectHandler(**cisco_config)
    except Exception as exception:
        print(exception)
        return

    device.send_command('terminal length 0')  # disable paging
    # device.enable() is not working ....
    device.send_command("enable" + '\n', expect_string=r'Password:')
    device.send_command(cisco_config['secret'], expect_string=r'#')
    device.send_command(cisco_config['secret'])

    running_config = device.send_command('show run')
    if 'Unrecognized command' in running_config:
        print(f'Cannot get running-config of {cisco_device.name}')
        return

    return ConnectedDevice(name=cisco_device.name, config=cisco_device.config, handler=device)


def disconnect_devices(devices: List[Optional[ConnectedDevice]]) -> None:
    for device in devices:
        if device is not None:
            device.handler.disconnect()


def get_devices() -> List[Optional[ConnectedDevice]]:
    cisco_devices = [switch_hackademint, switch_evryone, router_evryone]
    with ThreadPool(len(cisco_devices)) as tp:
        devices = tp.map(get_device_enabled, cisco_devices)
    if None in devices:
        disconnect_devices(devices)
        log.warn('Cannot connect to all devices', devices=devices)
        return []
    return devices
