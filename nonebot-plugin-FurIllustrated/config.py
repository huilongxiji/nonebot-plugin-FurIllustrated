from pydantic import BaseModel, Extra
from typing import Optional
import nonebot

# ============Config=============
class Config(BaseModel, extra=Extra.ignore):
    superusers: list = []

    # 插件版本号勿动！！！！
    syj_version: Optional[str] = "1.1.0"

    syj_account: Optional[str] = "furbot"
    '''兽云祭用户名'''

    suj_password: Optional[str] = "python"
    '''兽云祭账号密码'''

    image_token: Optional[str] = None
    '''操作令牌'''

    image_token_user: Optional[str] = None
    '''令牌用户名'''

    image_token_key: Optional[str] = None
    '''令牌密码'''

global_config = nonebot.get_driver().config
syj_config = Config(**global_config.dict())  # 载入配置
