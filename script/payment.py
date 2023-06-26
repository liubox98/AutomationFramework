from poco.drivers.unity3d import UnityPoco
from airtest.core.api import *
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.GmApi import *
# 进关购买五步支付脚本


def enter_customs_purchase_five_step_payment():
    poco = UnityPoco()
    gm = GmApi()
    gm.set_coin_num(0)
    gm.jump_level(100)
    poco('levelText', type='Text').wait(timeout=30)
    gm.level_fail()
    poco('CoinAni', type='Image').wait(timeout=30)
    time.sleep(10)
    if poco('continueBtn').exists():
        poco('continueBtn').click()
    else:
        print('Waiting timeout for appearance of UIObjectProxy of continueBtn')
        poco('ContinueBtn').click()
    print('sleep 10s ...')
    time.sleep(10)
    print('点击购买礼包！')
    touch(poco('Btn_buy_off', type='Button')[1].get_position())
    print('sleep 30s ...')
    time.sleep(30)
    dev = device()
    if dev.alert_exists():
        dev.alert_click(["OK", "取消"])
    w, h = device().get_current_resolution()
    touch([0.3 * w, 0.3 * h])
