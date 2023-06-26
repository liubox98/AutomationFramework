import json
import logging
import requests
from requests.adapters import HTTPAdapter
from airtest.core.api import device


LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


class GmApi:
    PORT = 8998

    def __init__(self):
        """
        封装PostInstructions类，使用该类的函数，直接达到操作的目的
        """
        self.ip = device().get_ip_address()
        self.__post_handle = PostInstructions(self.ip, self.PORT)

    def skip_area(self, area: str):
        """
        跳转区域
        """
        parameters = {"area": area}
        result = self.__post_handle.post_by_one_per("skip_area", parameters)
        logging.info("发送接口 跳转区域[type:str] 结果为{}".format(result))
        return result

    def join_level(self, level_id: int):
        """
        设置关卡数
        :param level_id: 关卡数量
        :return:
        """
        parameters = {"level_id": level_id}
        result = self.__post_handle.post_by_one_per("join_level", parameters)
        logging.info("发送接口 设置关卡id为{} 结果为{}".format(level_id, result))
        return result

    def jump_level(self, level_id: int):
        """
        跳转关卡
        :param level_id: 关卡id
        :return:
        """
        parameters = {"level_id": level_id}
        result = self.__post_handle.post_by_one_per("jump_level", parameters)
        logging.info("发送接口 跳转关卡 结果为{}".format(result))
        return result

    def level_pass(self):
        """
        通过关卡
        :return:
        """
        result = self.__post_handle.post_by_one_per("level_pass")
        logging.info("发送接口 通过关卡 结果为{}".format(result))
        return result

    def level_fail(self):
        """
        关卡失败
        :return:
        """
        result = self.__post_handle.post_by_one_per("level_fail")
        logging.info("发送接口 关卡失败 结果为{}".format(result))
        return result

    def set_coin_num(self, coin_num: int):
        """
        设置金币数量
        :param coin_num: 金币数量
        :return:
        """
        parameters = {"coin_num": coin_num}
        result = self.__post_handle.post_by_one_per("set_coin_num", parameters)
        logging.info("发送接口 设置金币数量为{} 结果为{}".format(coin_num, result))
        return result

    def get_info(self):
        """
        获取userId，deviceId
        :return:
        """
        result = self.__post_handle.post_by_one_per("get_info")
        logging.info("发送接口 获取userId，deviceId 结果为{}".format(result))
        return result


class PostInstructions:
    URL_TEMPLATE = 'http://{}:{}/Service/'

    def __init__(self, ip, port):
        self.url = self.URL_TEMPLATE.format(ip, port)

    def post_by_one_per(self, command, parameters=dict()):
        """
        单帧的执行接口
        :param command: 需要执行的接口
        :param parameters: 接口所需的参数
        :return: dict
        """
        if not isinstance(command, str):
            result = '参数类型错误\n' + 'command:' + \
                type(command) + '; parameters:' + type(parameters)
            return result

        data = {"commands": [{"command": command, "parameters": parameters}]}
        logging.debug("发送接口数据：" + json.dumps(data))

        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))

        try:
            res = s.post(self.url, json=data, timeout=10)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            logging.error("发送接口失败：{}".format(e))
            return str(e)

        if res.text == 'request time out.':
            return res.text

        cache = json.loads(res.text)
        res_list = self.parse_return_value(cache)
        logging.debug("接口返回值：{}".format(res_list))
        return res_list

    def parse_return_value(self, res_value):
        """
        解析接口返回值dict并简化，如正确返回[True, data], 如遇错误返回 [False, 错误码]
        :param res_value: 未经处理的接口返回res.text
        :return: 处理后的返回值 list
        """
        res_list = []
        response = res_value['responses'][0]
        if response['result'] == 'false':
            error_num = response['data']['error']
            res_list.append(False)
            res_list.append(error_num)
        elif response['result'] == 'true':
            data = response['data']
            res_list.append(True)
            res_list.append(data)
        return res_list
