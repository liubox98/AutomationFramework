import sys

from config.path import IOS
from tools.GmApi import GmApi
from airtest.core.api import *
import subprocess
import logging


def start_wda(uuid: str, port: int):
    cmd = [sys.executable, "-m", "tidevice", "-u", uuid, "wdaproxy", "-B",
           "com.facebook.WebDriverAgentRunner.xctrunner", "--port", str(port)]
    logging.info(f"启动wda进程{cmd}")
    p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    return p


def start_test(uuid: str, port: int):
    print('Connect Device ...')
    time.sleep(10)
    connect_device("iOS:///127.0.0.1:{}".format(port))
    install(uuid, IOS)
    start_ipa(uuid)


def start_ipa(uuid):
    cmd = "tidevice -u {} launch com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()
    time.sleep(20)
    close_system_pop()
    print('SLEEP 120s ...')
    time.sleep(120)
    print('开始执行用例 ...')
    from run import execution_use_case
    execution_use_case()


def close_system_pop():
    dev = device()
    for x in range(3):
        while True:
            if dev.alert_exists():
                dev.alert_click(["无线局域网与蜂窝网络", "要求App不跟踪", "允许", "好", "OK"])
                time.sleep(1)
                continue
            else:
                break
        time.sleep(4)


def stop_ipa(uuid):
    cmd = "tidevice -u {} kill com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()


def install(uuid, ipa):
    cmd = "tidevice -u {} install {}".format(uuid, ipa)
    os.popen(cmd).readlines()


def uninstall(uuid):
    cmd = "tidevice -u {} uninstall com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()


def delete_user():
    import requests
    requests.delete(
        f"http://10.10.240.207:30021/novaUser/{GmApi().get_info()[1]['userid']}")


def activity(uuid):
    NAME = 'Garden Affairs'
    cmd = ['tidevice', '-u', uuid, 'ps']
    if NAME in subprocess.check_output(cmd).decode():
        return True
    raise uuid + '活动不存在'
