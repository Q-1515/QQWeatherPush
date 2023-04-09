Now = {
    'degree': None,  # 温度
    'picture': None,  # 图片
    'weather': None,  # 天气情况
    'temperature': None,  # 温差
    'sunrise': None,  # 日出
    'sunset': None,  # 日落
    'motto': None,  # 格言
    'time': None,  # 日期和星期几
    'birthday': None,  # 距离生日天数
    'name': None,  # 姓名
    'bigPicture': None,  # 大图
    'city': None,  # 城市
    'icon': '',  # 天气傍边小图标id
    'estimate': None  # 雨雪预计
}


class FiveHours:

    def __init__(self, time, picture, degree, weather):
        self.time = time
        self.picture = picture
        self.degree = degree
        self.weather = weather

    def __str__(self):
        return f'time: {self.time}, picture: {self.picture}, degree: {self.degree}, weather: {self.weather}'


class FiveHoursBuilder:
    def __init__(self):
        self.time = None
        self.picture = None
        self.degree = None
        self.weather = None

    def set_time(self, time):
        self.time = time
        return self

    def set_picture(self, picture):
        self.picture = picture
        return self

    def set_degree(self, degree):
        self.degree = degree
        return self

    def set_weather(self, weather):
        self.weather = weather
        return self

    def build(self):
        return FiveHours(self.time, self.picture, self.degree, self.weather)
