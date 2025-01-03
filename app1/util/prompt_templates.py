class Person:
    def __init__(self, **kwargs):
        self.name = kwargs.name
        self.age = kwargs.age
        self.sex = kwargs.sex
        self.job = kwargs.job
        self.hobby = kwargs.hobby
        self.mbti = kwargs.mbti
        self.favor_topic = kwargs.favor_topic
        self.oppose_topic = kwargs.oppose_topic

    @property
    def setting(self):
        person_setting = f"""
            <person setting:>
            名前:<{self.name}>
            年齢:<{self.age}>
            性別:<{self.sex}>
            職業:<{self.job}>
            趣味:<{self.hobby}>
            性格(MBTI):<{self.mbti}>
            好きな話題：<{self.favor_topic}>
            苦手な話題：<{self.oppose_topic}>
        """
        return person_setting