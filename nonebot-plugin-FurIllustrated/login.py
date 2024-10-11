from nonebot.adapters.onebot.v11 import MessageSegment
from nonebot.plugin import on_command
from nonebot.permission import SUPERUSER
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.params import ArgPlainText
from .config import syj_config
from loguru import logger
from pathlib import Path
from datetime import *
import asyncio
import httpx
import os

cookies_q = {}
token_login = ""

fur_check = on_command("/验证码", permission=SUPERUSER)      # 注册一个消息事件响应器
login = on_command("/登录", permission=SUPERUSER)      # 注册一个消息事件响应器
token_updata = on_command("/更新登录令牌", permission=SUPERUSER)      # 注册一个消息事件响应器
token_look = on_command("/查看登录令牌", permission=SUPERUSER)      # 注册一个消息事件响应器

@fur_check.handle()
async def furry_check(args: Message = CommandArg()):
    if args.extract_plain_text(): await fur_check.finish()    # 中断非命令的情况，减少误触
    t = await login_zd()        # 自动登录
    if t:       # 判断是否登录成功
        check = await check_image()     # 调用验证码函数,将获取到的信息赋值给check变量
        if check["PHPSESSID"]:
            cookies_q["PHPSESSID"] = check["PHPSESSID"]       # 将cookie的值写入全局变量
        await fur_check.finish(MessageSegment.image(check['image']))       # 发送图片信息
    await fur_check.finish("请先登录w")

@login.handle()
async def furry_login(matcher: Matcher, args: Message = CommandArg()):
    t = await login_zd()    # 使用唯一登录令牌进行自动登录
    if t:       # 判断是否登录成功
        await matcher.finish(t)    # 发送信息
    else:
        global cookies_q
        check = await check_image()     # 调用验证码函数
        cookies_q["PHPSESSID"] = check["PHPSESSID"]       # 将cookie的值写入全局变量
        await matcher.send("发送验证码如下")    # 发送信息
        await matcher.send(MessageSegment.image(check['image']))    # 发送信息
        matcher.set_arg("keys", args)

@login.got("key")
async def furry_login(key: str = ArgPlainText("key")):
    global cookies_q
    if not key: await login.finish("登录终止")      # 异常终止
    data = {
        "account":syj_config.syj_account,      # 从配置文件里读取用户名
        "password":syj_config.suj_password,      # 从配置文件里读取密码
        "model":0,              #设置登录模式为图片验证码
        "proving":key      # 消息序列中获取命令后面的文本
    }
    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:       # 异步访问api
        login_data = await client.post('https://cloud.foxtail.cn/api/account/login',cookies=cookies_q,data=data)      # 填入请求数据，data为json，cookie为配置文件中的cookie
        if login_data.status_code == 200:       # 判断是否请求成功
            data = login_data.json()        # 将返回数据转为json格式
            cookie = login_data.cookies     # 获取请求api后产生的cookie数据
            if data["code"] == "10000":     # 判断是否登录成功
                logger.success("登录成功,正在更新cookie")      # 在log里面出输出登录状态
                cookies_q = {"Token":cookie["Token"],"PHPSESSID":cookie["PHPSESSID"],"User":cookie["User"]}       # 将新的cookie存入配置文件
                token = await login_token(1)        # 获取登录令牌
                if token:
                    global token_login
                    token_login = token      # 写入新的唯一登录令牌
                    await wri_token(token)       # 将唯一登录令牌存入本地文件
                    logger.success("登录令牌更新成功")      # 打印日志
                    await login.finish("登录成功")    # 发送信息
                else:
                    logger.error("登录令牌写入失败")      # 打印日志
                    await login.finish("登录令牌写入失败")    # 发送信息
            else:
                await login.send(f"响应码:{data['code']}\n状态:{data['msg']}")    # 发送信息
                cookies_q = {}       # 清空一次cookie，让API重新分配id
                check = await check_image()     # 调用验证码函数
                cookies_q["PHPSESSID"] = check["PHPSESSID"]       # 将cookie的值写入配置文件
                await login.reject(MessageSegment.image(check['image']))    # 发送信息
        else:
            await login.finish("请求失败")    # 发送信息

@token_updata.handle()
async def furry_token_updata(args: Message = CommandArg()):
    if args.extract_plain_text(): await fur_check.finish()    # 中断非命令的情况，减少误触
    token = await login_token(1)        # 获取登录令牌
    if token:        # 判断登录令牌是否获取成功
        await wri_token(token)        # 写入唯一登录令牌
        await token_updata.finish(f"令牌更新成功\n新令牌: {token}")    # 发送信息
    else:
        await token_updata.finish("令牌更新失败，请检查登陆状态")    # 发送信息

@token_look.handle()
async def furry_token_look(args: Message = CommandArg()):
    if args.extract_plain_text(): await fur_check.finish()    # 中断非命令的情况，减少误触
    token_data = await login_token(0)    # 查询目前有效的token
    if token_data:
        await token_look.finish(f"令牌更新成功\n网络返回: {token_data}\n本地令牌: {token_login} ")    # 发送信息
    await token_look.finish("令牌查询失败，请检查登陆状态")    # 发送信息

async def check_image():
    '''获取兽云祭图片验证码'''
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
            check = await client.get("https://cloud.foxtail.cn/api/check", cookies=cookies_q)
            key = check.cookies["PHPSESSID"]
            return {"image":check.content,"PHPSESSID":key}
    except KeyError:
        logger.success("二次获取图片验证码,将不写入cookie")
        return {"image":check.content,"PHPSESSID":False}
    except Exception:
        logger.error("图片验证码获取失败")
        return False

async def login_zd():
    '''自动登录函数'''
    try:
        global cookies_q
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
            a = await client.post("https://cloud.foxtail.cn/api/account/login", cookies=cookies_q, data={
                "account":syj_config.syj_account,
                "password":syj_config.suj_password,
                "model":1,
                "token":token_login
            })
            data = a.json()
            if data["code"] == "10000":
                cookie = a.cookies
                logger.success("登录成功,正在更新cookie")
                cookies_q = {"Token":cookie["Token"],"PHPSESSID":cookie["PHPSESSID"],"User":cookie["User"]}
                return "登录成功"
            elif data["code"] == "10020":
                logger.success("重复登录")
                return "客户端已登录"
            else:
                logger.error("登录失败！！！")
                return False
    except Exception:
        logger.error("登录请求发送失败")
        return False

async def login_token(id: int):
    '''登录令牌获取函数'''
    url = "https://cloud.foxtail.cn/api/account/tkapply" if id == 1 else "https://cloud.foxtail.cn/api/account/tkquery"
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
            u = await client.get(url,cookies=cookies_q)
            data = u.json()
            if data["code"] == "12000":
                logger.success("唯一登录令牌重新获取")
                return data["token"]
            elif data["code"] == "12100":
                logger.success("唯一登录令牌读取成功")
                return data["token"]
            elif data["code"] == "11101":
                logger.success("cookie丢失")
                return False
            else:
                print(data)
                logger.error("唯一登录令牌获取失败！！！")
                return False
    except Exception:
        logger.error("获取令牌失败！！")
        return False

async def wri_token(token):
    '''更新令牌函数'''
    with open("./data/token", "w", encoding="utf_8") as w:
        global token_login
        token_login = f"{token}"
        w.write(token)
        w.close

token_data = Path.cwd() / 'data/token'
token_data.parent.mkdir(parents=True, exist_ok=True)

if os.path.isfile("./data/token"):      # 如果存在唯一登录令牌
    with open("./data/token", "r", encoding="utf_8") as r:        # 读取令牌
        y = r.read().strip()
        token_login = y     # 将 唯一登陆令牌写入全局变量
        logger.warning(f"加载key成功:{y}")      # 输出到控制台

logger.warning(f"登录中！！{syj_config.syj_account}")

asyncio.run(login_zd())