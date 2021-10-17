### DailyNote
推送天气情况、热点新闻和精选一句话到微信上。

### 定时执行
结合crontab可实现定时推送。
crontab 设置 `30 9 * * *` 即每天9点半执行任务。

### 微信推送
✅ 通过企业微信官方API进行推送，普通微信可关注对应的企业微信应用，即可在普通微信获取推送信息，无需下载企业微信APP

✅ 注册企业微信，并新建一个应用，获取其编号和secret。[官方文档](https://work.weixin.qq.com/api/doc/90000/90135/90248)

✅ 企业微信注册链接：[注册](https://work.weixin.qq.com/wework_admin/register_wx?from=myhome_openApi)

### 使用条件
1. Python版本 >= 3.6

2. 需要Requests库，没有的则执行：`pip install requests`

3. 需要获得企业微信的wxid及应用的secret，并填入底部对应的`wxid`、`wxsecret`

4. 到中国天气网查询自己想要的城市的天气信息，并将对应的html编号、访问cookie填入项目底部`city_code`、`cookie`之中

### 更改一句话类型
“精选一句话”功能使用了[一言网](https://hitokoto.cn/)API

默认为文学、诗词、影视、哲学。

更改`sen_url = 'https://v1.hitokoto.cn?c=d&c=h&c=i&c=k'`中的查询参数即可更改句子来源类型

具体类型对照如下表所示：

| 参数 | 类型 |
|:---:| :---: |
| a | 动画 |
| b | 漫画 |
| c | 游戏 |
| d | 文学 |
| e | 原创 |
| f | 来自网络 |
| g | 其他 |
| h | 影视 |
| i | 诗词 |
| j | 网易云 |
| k | 哲学 |
| l | 抖机灵 |

类型可以多选，使用`&`连结

### 说明
1. 本项目不得用于商业、营利性用途

2. 新闻来源：[新浪新闻排行榜](http://news.sina.com.cn/hotnews/)

3. 天气预报来源：[中国天气网](http://www.weather.com.cn/)

4. 可使用云函数触发执行，需要增加main.handler方法

### 效果
可直接点击详情查看对应的新闻，手机端也无需确认继续访问，可直接访问（偶尔会触发继续访问提示）
![效果.png](http://tva1.sinaimg.cn/large/008q9lbOgy1gvil1w1jmyj60pv0iw47b02.jpg)
