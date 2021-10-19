import requests,json
from os import environ
from datetime import datetime
environ['NO_PROXY'] = '*' #忽略系统代理，开着代理requests会报错

def weather_info(cookie,city_code,timestamps):
    w_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "DNT": "1",
        "Host": "d1.weather.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://www.weather.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
    }
    weather_url = 'http://d1.weather.com.cn/dingzhi/%s.html?_=%s'%(city_code,timestamps)
    weather_req = requests.get(url=weather_url,headers=w_headers).content.decode('utf-8')
    weather_info = json.loads(weather_req.replace("var cityDZ%s ="%city_code, "").split(";var alarmDZ%s ="%city_code)[0])['weatherinfo']
    warning_json = json.loads(weather_req.replace("var cityDZ%s ="%city_code, "").split(";var alarmDZ%s ="%city_code)[1])
    try:
        warning = json.loads(str(warning_json).replace("'",'"'))['w'][0]
        warning_info = warning['w5'] + warning['w7']
    except:
        warning_info = "当前无预警信息"
    weather_messages = (
        "城市名称：%s"%weather_info['cityname']+
        "\n当前温度：%s"%weather_info['temp']+
        "\n最低温度：%s"%weather_info['tempn']+
        "\n天气情况：%s"%weather_info['weather']+
        "\n风力风向：%s"%weather_info['wd']+weather_info['ws']+
        "\n预警信息：%s"%warning_info
    )
    return weather_messages

def get_news(news_type,news_time):
    news_headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "DNT": "1",
        "Host": "top.news.sina.com.cn",
        "Pragma": "no-cache",
        "Referer": "http://news.sina.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
    }
    news_url = 'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=%s&top_time=%s&top_show_num=20&top_order=DESC&js_var=news_'%(news_type,news_time)
    news_req = requests.get(url=news_url,headers=news_headers).text.replace("var news_ = ","").replace(r"\/\/","//").replace(";","")
    format_news = json.loads(json.dumps(news_req ,ensure_ascii=False))
    news_sub = json.loads(format_news)['data'] #很奇怪，不loads两次的话，type会是str导致无法取值
    news_list = []
    for item in news_sub:
        if str(item['url']).split(".")[0] == "https://video": #新浪的视频新闻总会提示下载APP，直接过滤掉，选择不看
            continue
        else:
            news = item['title'] + ' <a href="%s">详情</a>'%item['url']
            news_list.append(news) 
    return news_list

def get_sentence():
    sen_url = 'https://v1.hitokoto.cn?c=d&c=h&c=i&c=k'
    get_sen = requests.get(url=sen_url).json()
    sentence = get_sen['hitokoto']+"\n\n出自：%s"%get_sen['from']
    return sentence

def message_content(city_code,timestamps,info_time,news_list,sentence):
    week_dict = {
        0:"星期一",
        1:"星期二",
        2:"星期三",
        3:"星期四",
        4:"星期五",
        5:"星期六",
        6:"星期日"
    }
    day = datetime.strftime(info_time,"%Y-%m-%d") + " " + week_dict[datetime.weekday(info_time)]
    content = (
        "******%s******\n"%day+
        "*************天气************\n\n"+
        weather_info(cookie,city_code,timestamps)+
        "\n\n*************热闻************\n\n"+
        str(news_list[0:10]).replace("['","").replace("', '",'\n').replace("']",'\n')+ #只截取前10条新闻，微信推送有长度限制
        "\n*************一句************\n\n"+
        sentence
    )
    return content

def weixin_push(content):
    wx_push_token = requests.post(url='https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s'%(wxid,wxsecret),data="").json()['access_token']
    wx_push_data = {
            "agentid":1000002,
            "msgtype":"text",
            "touser":"@all",
            "text":{
                    "content":content
            },
            "safe":0
        }
    requests.post('https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s'%wx_push_token,json=wx_push_data)

if __name__ == '__main__':
    #设定天气预报城市与查询时间
    city_code = '' #先在weather.com.cn上查询城市天气，网址结尾的数字替换即可
    cookie = "" #在查询天气的时候，按F12，在控制台复制对应的cookie并填入
    info_time = datetime.now()
    timestamps = round(datetime.timestamp(info_time)*1000)
    #设定企业微信推送参数
    wxid = ''
    wxsecret = '' 
    # 设定新闻时间（当天）与类型
    #财经：finance_0_suda 社会：news_society_suda 国内：news_china_suda 国际：news_world_suda
    #科技：tech_news_suda 军事：news_mil_suda 娱乐：ent_suda 体育：sports_suda 总排行：www_www_all_suda_suda
    news_type = 'news_china_suda'
    news_time = datetime.strftime(info_time,"%Y%m%d") 
    weixin_push(message_content(city_code,timestamps,info_time,get_news(news_type,news_time),get_sentence()))
