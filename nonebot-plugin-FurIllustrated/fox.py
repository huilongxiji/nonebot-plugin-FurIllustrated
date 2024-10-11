from nonebot.adapters.onebot.v11 import Message,MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import on_command
from loguru import logger
import httpx

help = '''========毛毛图鉴========
随机兽图(随机获取一张兽图)
来只毛(随机获取一张兽图)
来只+名字(根据名字或id搜图片)
来只毛+名字(根据名字搜毛图)
来只兽+名字(根据名字搜设定图)
查sid+名字(查看对方图片数量)
兽云搜索+数字(查看此sid图片详情)
投兽图(投稿照片)
图片反馈(删除,换图,修改图片)
兽云祭信息(查看兽云祭api详情)
========FurBot========'''

fur_help = on_command("兽云菜单", priority=10, block=True)

@fur_help.handle()
async def _(args: Message = CommandArg()):
    if args.extract_plain_text(): await fur_help.finish()
    await fur_help.finish(help)

fur_random = on_command("随机兽图", priority=10, block=True)

@fur_random.handle()
async def furry_random(args: Message = CommandArg()):
    '''随机兽图获取实现'''
    if args.extract_plain_text(): await fur_random.finish()
    random = await syj.random_data("0")
    if random:
        data = await syj.apidata(random["picture"]["id"],0)
        if data:
            await fur_random.finish(data)
    await fur_random.finish("图片获取失败")

fur_random_mao = on_command("来只毛", priority=10, block=True)

@fur_random_mao.handle()
async def furry_random_mao(args: Message = CommandArg()):
    '''随机毛图获取实现'''
    if args.extract_plain_text():
        random = await syj.random_data("1",str(args))
        if random:
            data = await syj.apidata(random["picture"]["id"],0)
            if data:
                await fur_random.finish(data)
        await fur_random.finish("图片获取失败")
    else:
        random = await syj.random_data("1")
        if random:
            data = await syj.apidata(random["picture"]["id"],0)
            if data:
                await fur_random.finish(data)
        await fur_random.finish("图片获取失败")

fur_random_shou = on_command("来只兽", priority=10, block=True)

@fur_random_shou.handle()
async def furry_random_shou(args: Message = CommandArg()):
    '''随机兽兽图'''
    if args.extract_plain_text():
        random = await syj.random_data("2",str(args))
        if random:
            data = await syj.apidata(random["picture"]["id"],0)
            if data:
                await fur_random.finish(data)
        await fur_random.finish("图片获取失败")
    else:
        random = await syj.random_data("2")
        if random:
            data = await syj.apidata(random["picture"]["id"],0)
            if data:
                await fur_random.finish(data)
        await fur_random.finish("图片获取失败")

fur_pictures = on_command("来只", priority=10, block=True)

@fur_pictures.handle()
async def furry_pictures(args: Message = CommandArg()):
    '''搜索指定图片'''
    if args.extract_plain_text():
        data = await syj.in_type(str(args))
        if data == "sid":
            sid = await syj.apidata(str(args),1)
            if sid:
                await fur_pictures.finish(sid)
        elif data == "name":
            name = await syj.apidata(str(args),2)
            if name:
                await fur_pictures.finish(name)
        else:
            await fur_random.finish("图片获取失败")
    await fur_pictures.finish("请携带SID或者名称关键字查询w")
    
fur_pulllist = on_command("查sid", priority=10, block=True)

@fur_pulllist.handle()
async def furry_pulllist(args: Message = CommandArg()):
    '''查询指定名称的所有图片'''
    if args.extract_plain_text():
        data = await syj.in_type(str(args))
        if data == "name":
            json = await syj.pulllist_data(str(args))
            if json:
                await fur_pictures.finish(f"{json}")
            await fur_pictures.finish("该名称没有图片哦")
    await fur_pictures.finish("请输入名字全称来查询")

fur_sousuo = on_command("兽云搜索", priority=10, block=True)

@fur_sousuo.handle()
async def furry_sousuo(args: Message = CommandArg()):
    '''查询图片详情'''
    if args.extract_plain_text():
        data = await syj.in_type(str(args))
        if data == "sid":
            json = await syj.pullpic_sid(str(args))
            if json:
                power_data = {"0": "私密","1": "公开","2": "特定"}
                examine_data = {"0": "待审核","1": "已通过","2": "被拒绝"}
                type_data = {"0": "设定图","1": "毛图","2": "插画"}
                account = json['picture'][0]['account']
                name = json['picture'][0]['name']
                sid = json['picture'][0]['id']
                uid = json['picture'][0]['picture']
                suggest = json['picture'][0]['suggest']
                time = json['picture'][0]['time']
                power_id = json['picture'][0]['power']
                power = power_data[f"{power_id}"]
                examine_id = json['picture'][0]['examine']
                examine = examine_data[f"{examine_id}"]
                type_id = json['picture'][0]['type']
                type = type_data[f"{type_id}"]
                md5 = json['picture'][0]['md5']
                format = json['picture'][0]['format']
                text = f"上传账号: {account}\n名称: {name}\nSID: {sid}\nUID: {uid}\n留言: {suggest}\n上传时间: {time}\n查看范围: {power}\n审核状态: {examine}\n图片类型: {type}\n图片格式: {format}\nMD5: {md5}\n"
                await fur_sousuo.finish("======毛毛图鉴======\n" + text + "======FurBot======\n#更多功能请发送“兽云菜单”")
            await fur_sousuo.finish("您输入的内容暂无数据")
    await fur_sousuo.finish("请输入sid来查询")

fur_feedback = on_command("兽云祭信息", priority=10, block=True)

@fur_feedback.handle()
async def _(args: Message = CommandArg()):
    '''兽云祭信息'''
    if args.extract_plain_text(): await fur_feedback.finish()
    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
        url_get = await client.get('https://cloud.foxtail.cn/api/information/feedback')
        if url_get.status_code == 200:
            url_json = url_get.json()
            total = url_json["total"]["count"]
            atlas = url_json["atlas"]["count"]
            power = url_json["power"]["count"]
            examine = url_json["examine"]["count"]
            time = url_json["time"]["count"]
            text =  "======毛毛图鉴======\n" + f"图片调用次数: {total}\n图片统计数量: {atlas}\n图片公开数量: {power}\n图片待审核数量: {examine}\n平台运行时常: {time}\n"+ "======FurBot======\n#更多功能请发送“兽云菜单”"
            await fur_feedback.finish(text)
        else:
            await fur_feedback.finish("请求失败")

class fox:
    def __init__(self):
        self.random_id_url = 'https://cloud.foxtail.cn/api/function/random?type='
        self.random_name_url = "https://cloud.foxtail.cn/api/function/random?name="
        self.pictures_url = "https://cloud.foxtail.cn/api/function/pictures?model=1&picture="
        self.pulllist_url = "https://cloud.foxtail.cn/api/function/pulllist?type=0&name="
        self.picture_url = f"https://cloud.foxtail.cn/api/function/pullpic?model=1&picture="
    
    async def in_type(self, text: str):
        '''判断搜索类型为sid还是名称'''
        try:
            type(eval(text))!=float and type(eval(text))!=int
            return "sid"
        except:
            return "name"
    
    async def random_data(self, type: str, name = ""):
        """随机兽图数据获取"""
        async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
            url_get = await client.get(self.random_id_url + type + f"&name={name}")
            if url_get.status_code == 200:
                return url_get.json()
            else:
                return False
    
    async def pictures_sid(self, sid: str):
        """指定sid数据获取"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
                data = await client.get(self.pictures_url + sid)
        except TimeoutError:
            logger.error("sid搜索模式访问超时")
            return False
        else:
            if data.status_code == 200:
                json = data.json()
                if json['code'] == "20600":
                    return json
            return False
    
    async def pictures_name(self, name: str):
        """指定名称数据获取"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
                data = await client.get(self.random_name_url + name)
        except TimeoutError:
            logger.error("名称搜索模式访问超时")
            return False
        else:
            if data.status_code == 200:
                json = data.json()
                if json['code'] == "20900":
                    json = await self.pictures_sid(json['picture']['id'])
                    return json
            return False
    
    async def pullpic_name(self, name: str):
        '''拉取指定名称下的图片列表'''
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
                data = await client.get(self.pulllist_url + name)
        except TimeoutError:
            logger.error("图片列表访问超时")
            return False
        else:
            if data.status_code == 200:
                url_json = data.json()
                if url_json['code'] == "20700":
                    return url_json
            return False
    
    async def pullpic_sid(self, sid: str):
        '''拉取指定id详情'''
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=60, write=20, pool=30)) as client:
                data = await client.get(self.picture_url + sid)
        except TimeoutError:
            logger.error("sid搜索模式访问超时")
            return False
        else:
            if data.status_code == 200:
                url_json = data.json()
                if url_json['code'] == "20800":
                    return url_json
            return False
    
    async def pulllist_data(self, name: str):
        '''关键字拉取列表构建'''
        json = await self.pullpic_name(name)
        if json['open'] == []: return False
        if json:
            text = ""
            for n in range(len(json['open'])):
                sid = json['open'][n]['id']
                text = text + f"{sid},"
            text_end = "======毛毛图鉴======\n" + f"关键字: {name}\nSID: {text}\n" + "======FurBot======\n#更多功能请发送“兽云菜单”"
            return text_end
        return False

    async def goujian(self, text: str, type: int):
        type_data = {"0":"随机搜索", "1":"sid搜索", "2":"名称搜索"}
        name = text["name"]
        sid = text["id"]
        suggest = text["suggest"]
        url = text["url"]
        fangshi = type_data[f"{type}"]
        text = f"名称: {name}\nSID: {sid}\n搜索方式: 【{fangshi}】\n留言: {suggest}\n"
        return "======毛毛图鉴======\n" + text + MessageSegment.image(url) + "======FurBot======\n#更多功能请发送“兽云菜单”"
    
    async def apidata(self, id: str, type: int):
        '''消息构建，总处理'''
        sid = await self.pictures_sid(id)
        name = await self.pictures_name(id)
        if type == 0 and sid != False:
            return await self.goujian(sid,0)
        elif type == 1 and sid != False:
            return await self.goujian(sid,1)
        elif type == 2 and name != False:
            return await self.goujian(name,2)
        else:
            return False

syj = fox()
'''兽云祭基础实现'''
