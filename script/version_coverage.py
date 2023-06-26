import subprocess
import logging
from poco.drivers.unity3d import UnityPoco
from multiprocessing import Process
from airtest.core.api import *
from tools.GmApi import *
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 版本覆盖脚本

devices_list = ['00008110-000514690E01401E']
NAME = 'Garden Affairs'

v40 = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '\\package',
                   'ggxc_20230504_1415_0702_PrivateJudianIos_release_V40.ipa')
v41 = os.path.join(os.path.dirname(os.path.dirname(__file__)) + '\\package',
                   'ggxc_20230513_0629_0716_ReleaseJudianIos_trunk.ipa')


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
    try:
        for i in queue:
            i.start()
        for i in queue:
            i.join()
    finally:
        use_port = 8300
        for process in range(len(queue)):
            try:
                command = f"netstat -ano | findstr :{use_port}"
                output = subprocess.check_output(
                    command, shell=True).decode("utf-8").strip()
                if output:
                    process_id = output.split()[-1]
                    subprocess.run(
                        f"taskkill /F /PID {process_id}", shell=True, check=True)
                    print(f"进程 {process_id} 已成功终止。")
                else:
                    print(f"端口 {use_port} 没有被占用。")
            except subprocess.CalledProcessError:
                print(f"无法终止端口 {use_port} 的进程。")
            use_port += 100


def start_wda(uuid, port):
    cmd = [sys.executable, "-m", "tidevice", "-u", uuid, "wdaproxy", "-B",
           "com.facebook.WebDriverAgentRunner.xctrunner", "--port", str(port)]
    logging.info(f"启动wda进程{cmd}")
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return p


def start(uuid, port):
    print('SLEEP 10 ...')
    time.sleep(10)
    install_ipa(uuid, v40)
    connect_device("iOS:///127.0.0.1:{}".format(port))
    start_ipa()
    dev = device()
    if dev.alert_exists():
        dev.alert_click(['OK'])
    case(uuid)
    activity(uuid)


def case(uuid):
    poco = UnityPoco()

    poco('serverConfirmBtn').click()
    time.sleep(10)
    GmApi().skip_area('W1A11')
    print('等待DLC下载 ...')
    time.sleep(30)
    print('返回桌面 覆盖安装')
    keyevent('HOME')
    keyevent('HOME')
    install_ipa(uuid, v41)
    activity(uuid)


def activity(uuid):
    start_app('com.huayuan.xiaochu')
    print('SLEEP 30 ...')
    time.sleep(30)
    FLAG = False
    if NAME in activity_ps(uuid):
        FLAG = True
    if FLAG:
        print('进程存在 停止应用')
        stop(uuid)
        print('卸载应用')
        uninstall(uuid)
        install_ipa(uuid, v41)
        start_ipa()
        case(uuid)
        activity(uuid)
    else:
        raise uuid


def start_ipa():
    start_app('com.huayuan.xiaochu')
    time.sleep(5)
    dev = device()
    for win in range(4):
        if dev.alert_exists():
            dev.alert_click(['OK', '好', '允许'])
        time.sleep(2)
    print('SLEEP 120s ...')
    time.sleep(120)


def stop(uuid):
    cmd = "tidevice -u {} kill com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()


def uninstall(uuid):
    cmd = "tidevice -u {} uninstall com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()


def install_ipa(uuid, ipa):
    cmd = "tidevice -u {} install {}".format(uuid, ipa)
    os.popen(cmd).readlines()


def activity_ps(uuid):
    cmd = ['tidevice', '-u', uuid, 'ps']
    return subprocess.check_output(cmd).decode()


if __name__ == '__main__':
    main()
