class GoCqhttpTemplate:

    def __init__(self, Now, Five_hours):
        # 姓名
        self.name = Now['name']
        # 大图
        self.bigPicture = Now['bigPicture']
        # 距离生日天数
        self.birthday = Now['birthday']
        # 日期和星期几
        self.time = Now['time']
        # 温度
        self.degree = Now['degree']
        # 天气情况
        self.weather = Now['weather']
        # 天气傍边小图标id
        self.icon = Now['icon']
        # 温差
        self.temperature = Now['temperature']
        # 日出
        self.sunrise = Now['sunrise']
        # 日落
        self.sunset = Now['sunset']
        # 格言
        self.motto = Now['motto']
        # 城市
        self.city = Now['city']
        # 雨雪预计
        self.estimate = Now['estimate']

        # 5小时天气数组
        self.Five_hours = Five_hours

    def __str__(self):
        message = f'[CQ:face,id=89]{self.name}\n' \
                  f'今天是 {self.time}\n' \
                  f'[CQ:image,file={self.bigPicture},type=show,id=40004]\n' \
                  f'{self.estimate}' \
                  f'✨✨✨✨✨✨✨✨✨✨\n' \
                  f'城市：{self.city}\n' \
                  f'天气：{self.weather} {self.icon}\n' \
                  f'气温：{self.degree}\n' \
                  f'温差：{self.temperature}\n' \
                  f'日出：{self.sunrise}\n' \
                  f'日落：{self.sunset}\n' \
                  f'距离[CQ:face,id=46]的生日还有{self.birthday}天\n' \
                  f'{self.motto}\n' \
                  f'✨✨✨✨✨✨✨✨✨✨\n'
        # 5小时预测模板
        for hours in self.Five_hours:
            message = message + \
                      f'{hours.time}[CQ:face,id=46]{hours.weather}\n' \
                      f'[CQ:image,file={hours.picture}] {hours.degree}\n' \
                      f' 〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️\n'
        return message