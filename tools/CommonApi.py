import os
import subprocess


def install_ipa(uuid, ipa):
    # 安装应用
    cmd = "tidevice -u {} install {}".format(uuid, ipa)
    os.popen(cmd).readlines()


def stop(uuid):
    # 停止进程
    cmd = "tidevice -u {} kill com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()


def uninstall(uuid):
    # 卸载应用
    cmd = "tidevice -u {} uninstall com.huayuan.xiaochu".format(uuid)
    os.popen(cmd).readlines()


def activity_ps(uuid):
    # 获取当前活动列表
    cmd = ['tidevice', '-u', uuid, 'ps']
    return subprocess.check_output(cmd).decode()
