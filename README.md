### DailyNote
每天推送天气情况、热点新闻和一句话到微信上。

### 定时执行
结合crontab可实现定时推送。
crontab 设置 `30 9 * * *` 即每天9点半执行任务。

### 微信推送
通过企业微信API进行推送，普通微信可关注对应的企业微信应用，即可在普通微信获取推送信息，无需下载企业微信APP

✅ 注册企业微信，并新建一个应用，获取其编号和secret。[官方文档](https://work.weixin.qq.com/api/doc/90000/90135/90248)

企业微信注册链接：[注册](https://work.weixin.qq.com/wework_admin/register_wx?from=myhome_openApi)

### 使用条件
1. Python版本 >= 3.6

2. 需要Requests库，没有的则执行：`pip install requests`

3. 需要获得企业微信的wxid及应用的secret，并填入底部对应的`wxid`、`wxsecret`

4. 到中国天气网查询自己想要的城市的天气信息，并将对应的html编号填入项目底部`city_code`之中

### 说明
1. 本项目不得用于商业、营利性用途

2. 新闻来源：[新浪新闻排行榜](http://news.sina.com.cn/hotnews/)

3. 天气预报来源：[中国天气网](http://www.weather.com.cn/)

4. 可使用云函数触发执行，需要增加main.handler方法
