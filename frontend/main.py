import re

from flask import Flask, render_template, abort, Response

from config import EXTERNAL_API_URL
from src.cisco_config import get_content, get_date
from src.cisco_parser import parse

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', API_URL=EXTERNAL_API_URL)


@app.route('/raw/<int:config_id>')
def raw(config_id):
    content = get_content()
    if content is None:
        abort(404)
    configs = [item for item in content['message']]
    config_id = config_id - 1
    if config_id < 0 or config_id > len(configs):
        abort(404)
    return Response(configs[config_id]['config'], mimetype="text/plain")


@app.route('/config/<int:config_id>')
def config(config_id):
    content = get_content()
    if content is None:
        abort(404)
    date = get_date(content)

    configs = [item for item in content['message']]
    config_id = config_id - 1
    if config_id < 0 or config_id > len(configs):
        abort(404)

    selected_config = configs[config_id]
    obj = lambda: None
    obj.id = config_id + 1
    obj.config_raw = selected_config['config']
    interfaces_vlan, interfaces_po, interfaces_gi = parse(config_id, obj.config_raw)
    obj.interfaces_vlan = interfaces_vlan
    obj.interfaces_po = interfaces_po
    obj.interfaces_gi = interfaces_gi
    obj.device_name = selected_config['name']
    return render_template('config.html', API_URL=EXTERNAL_API_URL, date=date, obj=obj)


@app.route('/devices')
def devices():
    content = get_content()
    date = get_date(content)
    return render_template('devices.html', API_URL=EXTERNAL_API_URL, date=date)


@app.route('/vlan')
def vlan():
    content = get_content()
    if content is None:
        abort(404)
    configs = [item for item in content['message']]
    selected_config = configs[-1]
    interfaces_vlan, _, _ = parse(-1, selected_config['config'])
    vlan_data = []
    for interface_vlan in interfaces_vlan:
        name = interface_vlan.text.split()[-1]
        vlan_id = int(re.findall('Vlan(\d+)', name)[0])
        d = {'id': vlan_id, 'name': name, 'description': '', 'subnet': ''}
        raw_data = ''.join([i.text for i in interface_vlan.children])
        result = re.findall(r'description "(.*?) (\d+)\.(\d+)\.(\d+)\.(\d+)/(\d+)"', raw_data)
        if result:
            result = result[0]
            (description, ip1, ip2, ip3, ip4, mask) = result
            d['description'] = description
            d['subnet'] = f'{ip1}.{ip2}.{ip3}.{ip4}/{mask}'
        vlan_data.append(d)
    return render_template('vlan.html', API_URL=EXTERNAL_API_URL, vlan_data=vlan_data)


if __name__ == '__main__':
    app.run(port=80)
