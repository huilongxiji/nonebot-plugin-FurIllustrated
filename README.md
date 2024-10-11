<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-FurIllustrated

_✨ 兽云祭官方API插件 ✨_

</a>
<a href="https://github.com/Ekac00/nonebot-plugin-RanFurryPic/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Ekac00/nonebot-plugin-RanFurryPic.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-RanFurryPic">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-RanFurryPic.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

基于NoneBot2进行适配的FURRY图鉴（毛图，插画）插件

## 📖 介绍

本插件使用官方<a href="https://console-docs.apipost.cn/preview/6bf01cfebd3e5f96/c4e20a5d1a5db86c?target_id=83fb4f89-221c-4196-bb85-4abf73af73af"> API </a>进行编写，集成了随机兽图，名称查询，id查询，图片信息查询等一系列的吸毛功能。安装即用！！
如果你有兽云祭账号可以按照要求填入配置项来使用涉及账户操作相关功能。
若本插件存在bug请及时反馈~
目前只支持 onebotV11 暂时还未上传nonebot商店

## 💿 安装

<details open>
<summary>使用 nb-cli 安装（推荐）</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```
nb plugin install nonebot-plugin-FurIllustrated
```

</details>

<details>
<summary>使用PIP安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 输入安装命令

```
pip install nonebot-plugin-FurIllustrated
```

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

```
plugins = ["nonebot-plugin-FurIllustrated"]
```

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置，不填任何配置则自动使用默认账户

```
# 你的兽云祭账户
syj_account = 账户
# 你的兽云祭密码
suj_password = 密码
# 令牌模式的token
image_token = 令牌
# 你的令牌用户名
image_token_user = "用户名"
# 你的令牌密码
image_token_key = "密码"
```

## 🎉 使用

### 指令表

|    指令    | 权限 |   是否需要参数   |            说明            |
| :--------: | :--: | :---------------: | :-------------------------: |
|  随机兽图  | 群员 |        否        |      随机获取一张兽图      |
|    来只    | 群员 | 可用sid或毛毛名字 |     根据名字或id搜图片     |
|   来只毛   | 群员 |  可空也可带名字  |       根据名字搜毛图       |
|   来只兽   | 群员 |  可空也可带名字  |      根据名字搜设定图      |
|   查sid   | 群员 |    需要纯数字    | 根据关键字查询图片的sid列表 |
|  兽云搜索  | 群员 |    需要纯数字    |      查看此sid图片详情      |
| 兽云祭信息 | 群员 |        否        |      根据名字搜设定图      |

## 插件完成度

目前进度:

- [x] 随机毛图
- [x] 指定图片查询
- [x] 服务状态查询
- [x] 登录模块（自动登录）
- [ ] 上传图片
- [ ] 用户图片管理

