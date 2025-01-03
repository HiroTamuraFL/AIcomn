import os

from llama_index.llms.ollama import Ollama

import json
import random

llm = Ollama(model='gemma2:9b', request_timeout=600.0)

id = 0

prof = {id:{}}

class Person:
    def __init__(self, **kwargs):
        self.id = kwargs.id
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

def base_setting():
    sex = '女性'

    name_prompt = f"""
    あなたは1人の{sex}プロフィールを作成するAIの一部である。必ず以下の要素だけを生成して。苗字と名前：
    """
    name = llm.complete(name_prompt).text.replace('\n','')

    age_range = [[15]*5,[16]*5,[17]*5,[18]*10,[19]*10,[20]*10,[21]*10,[22]*10,[23]*10,[24]*10,[25]*10,[26]*10,[27]*5,[28]*5,[29]*5,[30]*5]
    weighted_age_range = sum(age_range, [])
    age = random.choice(weighted_age_range)


    if age<18:
        job = '学生'
    elif age<22:
        job = random.choice(['学生','社会人'])
    else:
        job = '社会人'
    if job=='社会人':
        while True:
            job_prompt = f"""
            あなたは1人の{age}の{sex}のプロフィールを作成するAIの一部である。必ず以下の要素を一つだけを生成したときに生成を終了し、それ以外の要素を生成しないで。職業：
            """
            job = llm.complete(job_prompt).text.replace('\n','')
            if age<22 and job in ['教師']:
                pass
            else:
                break
    print(f"name:{name}")
    print(sex)
    print(age)
    print(f"job:{job}")

    prof[id]['name'] = name
    prof[id]['sex'] = sex
    prof[id]['age'] = age
    prof[id]['job'] = job

    with open('F:/Llama/django-chat-app/app1/util/data/person_setting.json', 'w', encoding="utf-8") as f:
        json.dump(prof, f, indent=2, ensure_ascii=False)

def detail_setting():
    with open('F:/Llama/django-chat-app/app1/util/data/person_setting.json','r',encoding="utf-8_sig") as f:
        base_js = json.load(f)[id]
    name = base_js['name']
    sex = base_js['sex']
    age = base_js['age']
    job = base_js['job']

base_setting()
detail_setting()