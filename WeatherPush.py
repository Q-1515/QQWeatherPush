import requests
from datetime import datetime

from Template import GoCqhttpTemplate
from model import FiveHoursBuilder, Now


# 天气获取基础数据
def get_weather_Data(province, city, district):
    #  observe         实况
    #  forecast_1h     预报
    #  forecast_24h    预报
    #  air             空气质量
    #  index           指数
    #  alarm           天气预警
    #  limit           尾号限行
    url = 'https://wis.qq.com/weather/common'
    params = {
        'source': 'pc',
        'weather_type': "observe|forecast_1h|forecast_24h|index|alarm|limit|tips|rise",
        'province': f'{province}',
        'city': f'{city}',
        'county': f'{district}'
    }
    # 开始发送get请求
    # print(requests.get(url, params=params).text)
    return requests.get(url, params=params).json()


# 判断白天还是晚上
def get_day_or_night(now_time, sunrise, sunset):
    time = f'{now_time.year}-{now_time.month}-{now_time.day} '
    sunrise_time = datetime.strptime(time + sunrise, '%Y-%m-%d %H:%M')
    sunset_time = datetime.strptime(time + sunset, '%Y-%m-%d %H:%M')
    if sunrise_time < now_time < sunset_time:
        return 'day'
    else:
        return 'night'


# 获取日期和星期几
def get_nowData():
    # 获取当前日期和时间
    now = datetime.now()
    # 获取年月日
    year = now.year
    month = now.month
    day = now.day
    # 获取星期几
    weekday = now.weekday()
    day_name = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][weekday]
    # 打印日期和星期几
    now_data = f"{year}-{month}-{day} {day_name}"
    return now_data


# 封装生日数据
def countdown(birthday):
    today = datetime.today()
    next_birthday = datetime(today.year, birthday.month, birthday.day)
    if next_birthday < today:
        next_birthday = datetime(today.year + 1, birthday.month, birthday.day)
    time_to_birthday = abs(next_birthday - today)
    return time_to_birthday.days


# 封装今日天气数据
def get_NowData(data):
    observe = data['observe']

    # 现在时间
    now_time = datetime.now()
    # 现在温度
    Now['degree'] = observe['degree'] + '°'
    # 现在天气
    Now['weather'] = observe['weather']

    # 日出日落
    for i in ['0', '1', '2']:
        rise_time = data['rise'][i]['time']
        rise_time_for = datetime.strptime(rise_time, '%Y%m%d')
        if now_time.day == rise_time_for.day:
            rise = data['rise'][i]
    Now['sunrise'] = rise['sunrise']
    Now['sunset'] = rise['sunset']

    # 图片
    day_or_night = get_day_or_night(now_time, Now['sunrise'], Now['sunset'])
    number = observe['weather_code']
    Now['picture'] = f'https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/{day_or_night}/{number}.png'

    # 温差
    for i in ['0', '1', '2']:
        time = data['forecast_24h'][i]['time']
        a = datetime.strptime(time, '%Y-%m-%d')
        if now_time.day == a.day:
            temperature = data['forecast_24h'][i]
    min_degree = temperature['min_degree']
    max_degree = temperature['max_degree']
    Now['temperature'] = f'{min_degree}°C~{max_degree}°C'

    # 每日格言
    motto_url = 'https://v2.jinrishici.com/one.json'
    Headers = {
        'client': 'browser-sdk/1.2',
        'X-User-Token': 'qXs1fbkYAHY7sYhuKHtu3m7URlK2332c'
    }
    response = requests.get(url=motto_url, headers=Headers)
    data = response.json()['data']
    Now['motto'] = data['content']
    return Now


# 封装5小时天气数据
def get_Five_hoursData(data, current_weather):
    # 现在时间
    now_time = datetime.now()

    forecast_1h = data['forecast_1h']
    # 获取当小时的坐标
    for i in forecast_1h:
        update_time = forecast_1h[f'{i}']['update_time']
        update_time = datetime.strptime(update_time, '%Y%m%d%H%M%S')
        if now_time.hour == update_time.hour:
            index = i
            break

    # 添加现在数据
    Five_data = [
        FiveHoursBuilder()
        .set_time('现在')
        .set_picture(current_weather['picture'])
        .set_degree(current_weather['degree'])
        .set_weather(current_weather['weather'])
        .build()
    ]
    for i in range(4):
        index = str(int(index) + 1)
        # 图片
        day_or_night = get_day_or_night(now_time, current_weather['sunrise'], current_weather['sunset'])
        number = forecast_1h[index]['weather_code']
        picture = f'https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/{day_or_night}/{number}.png'
        # 时间
        time = datetime.strptime(forecast_1h[index]['update_time'], '%Y%m%d%H%M%S').strftime('%H:%M')
        Five_data.append(
            FiveHoursBuilder()
            .set_time(time)
            .set_picture(picture)
            .set_degree(forecast_1h[index]['degree']+'°')
            .set_weather(forecast_1h[index]['weather_short'])
            .build()
        )
    return Five_data


# GoCqhttp 发送信息
def send_message(qq, qqHttp_url, message):
    data = {
        "user_id": qq,
        "message": message
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    res = requests.post(url=qqHttp_url, headers=headers, json=data)
    print(res.text)


# GoCqhttp 发送图片url转义
def escape_picture_url(Five):
    for i in Five:
        picture_url = i.picture.replace('&', '&amp;').replace(',', '&#44;')
        i.picture = picture_url


# 雨雪预计 需和风天气授权key
def get_estimate():
    url = 'https://devapi.qweather.com/v7/minutely/5m'
    params = {
        'location': '118.76741,32.04155', # 经纬度
        'key': '34bfxxxxxxxxxxxxxxxxxxx',
        'lang': 'zh'
    }

    try:
        res = requests.get(url, params=params)
        summary = res.json()['summary']

        if summary:
            summary = summary.replace('，', '\n')
            summary += '\n'
            Now['estimate'] = summary

    except Exception as e:
        print(f'Error occurred: {e}')


# 设置天气图标
def set_icon(Now):
    weather = Now['weather']
    icon = ''  # 定义默认图标编号为None
    if '晴' in weather:
        icon = '☀'
    elif '云' in weather or '阴' in weather:
        icon = '☁️'
    elif '雷' in weather and '雨' in weather:
        icon = '⛈'
    elif '雨' in weather:
        icon = '🌧️'
    elif '雪' in weather:
        icon = '❄️'
    elif '雾' in weather:
        icon = '🌫'
    Now['icon'] = icon


if __name__ == '__main__':
    # 省
    province = '江苏'
    # 市
    city = '南京'
    district = ''
    name = '傻憨憨'
    qq = 'xxxxx'
    # 自定义图片
    bigPictureUrl = 'https://s2.xptou.com/2023/04/01/6427ff09b65ef.jpg'
    GoCqhttpUrl = 'http://localhost:1515/send_private_msg'

    res = get_weather_Data(province, city, district)
    if res['status'] == 200:
        resData = res['data']
        # 获取今日天气数据
        Now = get_NowData(resData)
        # 雨雪预计
        get_estimate()
        # 获取5小鼠天气数据
        Five_hours = get_Five_hoursData(resData, Now)
        # 转义可以发送的url
        escape_picture_url(Five_hours)
        # 生日
        Now['birthday'] = countdown(datetime(2002, 8, 12))
        # 日期和星期几
        Now['time'] = get_nowData()
        # 姓名
        Now['name'] = name
        # 城市
        Now['city'] = city
        # 大图url
        Now['bigPicture'] = bigPictureUrl.replace('&', '&amp;').replace(',', '&#44;')
        # 天气傍边小图标id
        set_icon(Now)

        # 获取发送模板
        TemplateMessage = GoCqhttpTemplate(Now, Five_hours).__str__()
        print(TemplateMessage)
        send_message(qq, GoCqhttpUrl, TemplateMessage)
    else:
        print(res['status'])
        print(res['message'])