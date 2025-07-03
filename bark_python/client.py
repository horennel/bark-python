import base64
import json
from typing import Type
from abc import ABC, abstractmethod

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .exceptions import *


class EncryptionStrategy(ABC):
    """
    加密策略抽象类。
    Base class for all encryption strategies.
    """

    @abstractmethod
    def encrypt(self, key: str, iv: str, data: str, other_params: dict) -> bytes:
        pass


class CBCStrategy(EncryptionStrategy):
    """
    使用 AES-CBC 模式的加密策略。
    Encryption strategy using AES-CBC mode.
    """

    def encrypt(self, key: str, iv: str, data: str, other_params: dict) -> bytes:
        key_bytes, iv_bytes = key.encode('utf-8'), iv.encode('utf-8')
        cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
        padded = pad(data.encode('utf-8'), AES.block_size)
        return cipher.encrypt(padded)


class ECBStrategy(EncryptionStrategy):
    """
    使用 AES-ECB 模式的加密策略。
    Encryption strategy using AES-ECB mode.
    """

    def encrypt(self, key: str, iv: str, data: str, other_params: dict) -> bytes:
        key_bytes, iv_bytes = key.encode('utf-8'), iv.encode('utf-8')
        cipher = AES.new(key_bytes, AES.MODE_ECB)
        padded = pad(data.encode('utf-8'), AES.block_size)
        return cipher.encrypt(padded)


class BaseHandler(object):
    """
    请求处理器基类，用于发送请求的基础逻辑
    Base handler for sending HTTP requests.
    """

    def __init__(self, device_key, api_url):
        self.device_key = device_key  # 设备密钥（唯一标识）
        self.api_url = api_url  # 接口地址

    def request(self, kwargs):
        """
        向服务器发送 GET 请求。
        Send a GET request to the server.

        :param kwargs: 请求参数 / Request parameters
        :return: 响应文本 / Response text
        """
        try:
            response = requests.get(f'{self.api_url}/{self.device_key}', data=kwargs, timeout=30)
            return response.text
        except Exception as e:
            raise APIRequestError(e)  # 请求失败抛出异常


class Default(BaseHandler):
    """
    默认通知处理类，不加密数据。
    Default notification handler without encryption.
    """

    def send_notification(self, **kwargs):
        """
        发送通知（不加密）
        Send notification (without encryption).
        """
        return self.request(kwargs)


class Encryption(BaseHandler):
    """
    支持加密的请求发送类，依赖策略对象实现加密逻辑。
    Encrypted notification sender, using injected encryption strategy.
    """

    def __init__(self, device_key, api_url, key, iv, strategy: EncryptionStrategy, other_params):
        super().__init__(device_key, api_url)
        self.key = key
        self.iv = iv
        self.other_params = other_params
        self.strategy = strategy  # 策略对象注入

    def send_notification(self, **kwargs):
        """
        发送加密通知，使用当前策略对数据加密后发送。
        Send encrypted notification. Uses strategy to encrypt JSON payload.

        :param kwargs: 要加密的键值对参数 / Parameters to encrypt
        :return: 响应文本 / Server response text
        """
        json_string = json.dumps(kwargs, ensure_ascii=False)
        try:
            ciphertext = self.strategy.encrypt(self.key, self.iv, json_string, self.other_params)
            ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        except Exception as e:
            raise EncryptError(e)
        kwargs = {'ciphertext': ciphertext_b64}
        return self.request(kwargs)


class BarkClient(object):
    """
    Bark 客户端接口封装，支持默认和加密通知发送。
    Bark client interface wrapper, supports plain and encrypted notifications.
    """

    def __init__(self, device_key: str, api_url: str = "https://api.day.app"):
        if not device_key:
            raise InvalidParameterError("Device key is required.")
        self.device_key = device_key
        self.api_url = api_url.rstrip('/')
        self.handler = Default(self.device_key, self.api_url)  # 默认使用不加密的 handler

    def set_encryption(
            self,
            key: str = None,
            iv: str = None,
            strategy_cls: Type[EncryptionStrategy] = CBCStrategy,
            other_params=None
    ):
        """
        设置加密参数和策略实例。
        Set encryption key, IV, and strategy class.

        :param key: 加密密钥（16/24/32 长度）/ Key string of length 16/24/32
        :param iv: 初始化向量（长度必须为 16）/ IV string of length 16
        :param strategy_cls: 策略类，默认为 CBC / Strategy class, default is CBC
        :param other_params: 其他参数，用于自定义加密策略
        :raises InvalidParameterError: 若参数格式错误 / If parameter is invalid
        """
        if other_params is None:
            other_params = {}
        strategy = strategy_cls()
        self.handler = Encryption(self.device_key, self.api_url, key, iv, strategy, other_params)

    def send_notification(self, **kwargs):
        """
        发送通知（根据当前 handler 判断是否加密）。
        Send notification (encrypted or plain, depending on current handler).
        """
        self.handler.send_notification(**kwargs)
