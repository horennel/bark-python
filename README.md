# Encrypted Push Notification Client for Bark / Bark加密推送通知客户端

## Features / 特性

- 支持 AES-128/192/256
- 支持 加密策略（CBC / ECB，可扩展 GCM 等）


## Installation / 安装

```bash
pip3 install bark-python
或者
git clone https://github.com/horennel/bark-python.git
python3 setup.py install
```

## Usage / 用法示例

```python
from bark_python import BarkClient, CBCStrategy, EncryptionStrategy

client = BarkClient(device_key="your_device_key", api_url="https://api.day.app")

# 设置加密方式（可选，默认明文）
client.set_encryption(
    key="1234567890abcdef",  # 必须是 16/24/32 字符
    iv="abcdef1234567890",  # 必须是 16 字符
    strategy_cls=CBCStrategy  # 也可以用 ECBStrategy，或者自己扩展
)

# 发送推送通知
client.send_notification(
    title="🔒 Secure Title",
    body="Hello from encrypted Bark client!",
    sound="shake"
)


# 自定义加密算法（可选）
class MyNewStrategy(EncryptionStrategy):
    def encrypt(self, key: bytes, iv: bytes, data: str) -> bytes:
        pass
```

## Credits / 致谢

- [Finb/Bark - iOS消息推送工具](https://github.com/Finb/Bark)
- [PyCryptodome - 加密支持库](https://github.com/Legrandin/pycryptodome)
