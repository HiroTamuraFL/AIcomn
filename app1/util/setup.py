import os

from llama_index.llms.ollama import Ollama

import json
import random

llm = Ollama(model='gemma2:9b', request_timeout=600.0)

doc = None

topics = {"食事","芸術","ファッション","芸能"}
i = 0
while True:
    print(f'{i}th trial')
    shuffled_topics = list(topics)
    random.shuffle(shuffled_topics)
    prompt = f"""
    あなたは20代若年世代の汎用的な会話のトピックを網羅するAIである。
    必ずトピックだけを日本語で出力し、トピック間は必ず/で区切るようにして重複がないように続きを生成して。
    <トピック>{'/'.join(shuffled_topics)}/
    """

    new_topics = llm.complete(prompt).text
    new_topics = new_topics.replace('\n','').replace(' ','').split('/')
    flag = False
    for new_topic in new_topics:
        if new_topic not in topics:
            topics.add(new_topic)
            flag = True

    if not flag:
        break
    i+=1
    print(topics)

with open('F:/Llama/django-chat-app/app1/util/data/topics.json', 'w', encoding="utf-8") as f:
    json.dump(list(topics), f, indent=2, ensure_ascii=False)