from typing import List, Tuple

from ciscoconfparse import CiscoConfParse
from ciscoconfparse.models_cisco import IOSIntfLine


def parse(key: int, config: str) -> Tuple[List[IOSIntfLine], List[IOSIntfLine], List[IOSIntfLine]]:
    path = f'/tmp/config_cisco_{key}.conf'
    f = open(path, 'w')
    f.write(config)
    f.close()
    parsed_config = CiscoConfParse(path, factory=True)
    interfaces_gi = parsed_config.find_objects('^interface [g|G]iga')
    interfaces_vlan = parsed_config.find_objects('^interface [v|V]lan')
    interfaces_po = parsed_config.find_objects('^interface Port-channel')
    return interfaces_vlan, interfaces_po, interfaces_gi
