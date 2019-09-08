from datetime import timedelta

from timeloop import Timeloop

from src import redis_app, log
from src.devices_functions import get_devices, disconnect_devices
from src.redis_job import parse, make

tl = Timeloop()


@tl.job(interval=timedelta(seconds=15))
def main() -> None:
    response = redis_app.xread(streams={'todo': 0}, count=1)
    log.info('Response', response=response)
    if not response:
        return

    devices = get_devices()
    if not devices:
        return

    id, action = parse(response)

    try:
        make(devices, action, id.decode())
    except Exception as exception:
        log.warn('Exception triggered', exception=exception)
        return

    disconnect_devices(devices)
    redis_app.xdel('todo', id)


if __name__ == '__main__':
    tl.start(block=True)
