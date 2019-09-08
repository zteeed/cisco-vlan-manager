import ipaddress
import json
from typing import Dict, Optional


def make_payload(data: Dict) -> object:
    if data['type'] == 'add':
        if 'vlan_number' not in data.keys():
            return None
        if 'subnet' not in data.keys():
            return None
        if not data['vlan_number'].isdigit():
            return None
        if int(data['vlan_number']) <= 121:
            return None
        try:
            ipaddress.ip_network(data['subnet'])
        except Exception:
            return None
        content = dict(type=data['type'], vlan_num=data['vlan_number'], subnet=data['subnet'])
        return json.dumps(content)

    elif data['type'] == 'remove':
        if 'vlan_number' not in data.keys():
            return None
        if not data['vlan_number'].isdigit():
            return None
        if int(data['vlan_number']) <= 121:
            return None
        content = dict(type=data['type'], vlan_num=data['vlan_number'])
        return json.dumps(content)

    elif data['type'] == 'update':
        content = dict(type=data['type'])
        return json.dumps(content)

    elif data['type'] == 'save':
        content = dict(type=data['type'])
        return json.dumps(content)

    else:
        return None
