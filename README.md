# Encrypted Push Notification Client for Bark / Bark加密推送通知客户端

## Features / 特性

- 支持 AES-128/192/256
- 支持 加密策略（CBC / ECB，可自定义 GCM 等）

## Installation / 安装

```bash
pip3 install bark-python
```

或者

```bash
git clone https://github.com/horennel/bark-python.git
python3 setup.py install
```

## Usage / 用法示例

##### 不使用加密

```python
from bark_python import BarkClient

client = BarkClient(device_key="your_device_key", api_url="https://api.day.app")

# 发送推送通知
client.send_notification(
    title="🔒 Secure Title",
    body="Hello from encrypted Bark client!",
    sound="shake",
    # ... 可增加bark支持的参数
)
```

##### 使用加密

```python
from bark_python import BarkClient, CBCStrategy, ECBStrategy

client = BarkClient(device_key="your_device_key", api_url="https://api.day.app")

# 设置加密方式
client.set_encryption(
    key="1234567890abcdef",  # 默认空，AES128[16位]|AES192[24位]|AES256[32位] 字符串
    iv="abcdef1234567890",  # 默认空，CBC和ECB都为16位字符串
    strategy_cls=CBCStrategy,  # 也可以用 ECBStrategy
)

# 发送推送通知
client.send_notification(
    title="🔒 Secure Title",
    body="Hello from encrypted Bark client!",
    sound="shake"
    # ... 可增加bark支持的参数
)
```

##### 自定义加密策略

```python
from bark_python import BarkClient, EncryptionStrategy

client = BarkClient(device_key="your_device_key", api_url="https://api.day.app")


# 自定义加密策略
class MyNewStrategy(EncryptionStrategy):
    def encrypt(self, key: str, iv: str, data: str, other_params: dict) -> bytes:
        # 返回加密后的bytes数据
        pass


# 设置加密方式
client.set_encryption(
    strategy_cls=MyNewStrategy,  # 使用自定义加密策略
    other_params={"自定义参数": "自定义参数"}  # 可以添加自定义参数，用于自定义加密策略
)

# 发送推送通知
client.send_notification(
    title="🔒 Secure Title",
    body="Hello from encrypted Bark client!",
    sound="shake"
    # ... 可增加bark支持的参数
)
```

## Credits / 致谢

- [Finb/Bark - iOS消息推送工具](https://github.com/Finb/Bark)
- [PyCryptodome - 加密支持库](https://github.com/Legrandin/pycryptodome)
