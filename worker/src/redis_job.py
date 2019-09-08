import json
from datetime import datetime
from functools import partial
from multiprocessing.pool import ThreadPool
from typing import Dict, List, Tuple

from src import redis_app, log
from src.commands import add_vlan, remove_vlan, update_config, save_config
from src.devices import ConnectedDevice


def parse(response: List) -> Tuple[bytes, Dict]:
    id = response[0][1][0][0]
    action = response[0][1][0][1][b'json']
    return id, json.loads(action)


def make(devices: List[ConnectedDevice], action: Dict[str, str], id: str) -> None:
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    if action['type'] == 'add':
        tp_function = partial(add_vlan, vlan_number=action['vlan_num'], subnet=action['subnet'])
        with ThreadPool(len(devices)) as tp:
            tp.map(tp_function, devices)
        redis_app.xadd('update', {
            'id': id,
            'message': f'VLAN {action["vlan_num"]} ({action["subnet"]}) had been successfully added.'
        })
        log.info(f'VLAN {action["vlan_num"]} ({action["subnet"]}) had been successfully added.')
        make(devices, {'type': 'update'}, '999')

    elif action['type'] == 'remove':
        tp_function = partial(remove_vlan, vlan_number=action['vlan_num'])
        with ThreadPool(len(devices)) as tp:
            tp.map(tp_function, devices)
        redis_app.xadd('update', {'id': id, 'message': f'VLAN {action["vlan_num"]} had been successfully removed.'})
        log.info(f'VLAN {action["vlan_num"]} had been successfully removed.')
        make(devices, {'type': 'update'}, '999')

    elif action['type'] == 'update':
        with ThreadPool(len(devices)) as tp:
            result = tp.map(update_config, devices)
        data = [dict(name=device.name, config=result[key]) for key, device in enumerate(devices)]
        redis_app.set('config_cisco', json.dumps({'json': data, 'time': now}))
        redis_app.xadd('update', {'id': id, 'message': 'Running configurations had been updated successfully.'})
        log.info('Running configurations had been updated.successfully.')

    elif action['type'] == 'save':
        with ThreadPool(len(devices)) as tp:
            tp.map(save_config, devices)
        redis_app.xadd('save', {'time': now})
        redis_app.xadd('update', {'id': id, 'message': 'Running configurations had been saved successfully.'})
        log.info('Running configurations had been saved successfully.')

    else:
        log.warn('Unknown action type')
