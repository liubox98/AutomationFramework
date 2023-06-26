import subprocess
import logging
from airtest.core.api import *
from multiprocessing import Process
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 客户端重启脚本

devices_list = ['00008101-00091DA11AB9003A', '00008101-00050C6C36D0001E', '00008020-001B05522688002E',
                '10ffc55dc1f54c8c3abd633823069db040eeac42', '00008030-00114CE63E46402E',
                '6540ec990bbb0fe1e97a296c052340b07cc93221']
NAME = 'Garden Affairs'


def main():
    wda_devices_dict = {}
    queue = []
    port = 8300
    for uuid in devices_list:
        process = start_wda(uuid, port)
        wda_devices_dict[uuid] = {"process": process, "port": port}
        print('uuid', uuid)
        print('port', port)
        t = Process(target=start, args=(uuid, port,))
        queue.append(t)
        port += 100

    for i in queue:
        i.start()
    for i in queue:
        i.join()


def start_wda(uuid, port):
    cmd = [sys.executable, "-m", "tidevice", "-u", uuid, "wdaproxy", "-B",
           "com.facebook.WebDriverAgentRunner.xctrunner", "--port", str(port)]
    logging.info(f"启动wda进程{cmd}")
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return p


def start(uuid, port):
    print('SLEEP 10 ...')
    time.sleep(10)
    connect_device("iOS:///127.0.0.1:{}".format(port))
    activity(uuid)


def activity(uuid):
    start_app('com.huayuan.xiaochu')
    print('SLEEP 30 ...')
    time.sleep(30)
    FLAG = False
    for activity in activity_ps(uuid):
        print('activity:', activity)
        if NAME in activity:
            FLAG = True
            break
    if FLAG:
        stop(uuid)
    else:
        raise uuid


def stop(uuid):
    stop_app('com.huayuan.xiaochu')
    activity(uuid)


def activity_ps(uuid):
    cmd = f'tidevice -u {uuid} ps'
    result = os.popen(cmd).readlines()
    return result


if __name__ == '__main__':
    main()
