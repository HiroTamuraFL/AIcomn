from llama_index.llms.ollama import Ollama

import random
import json

import os

from django.conf import settings

from stable_diffusion.gen_imgs import generate_img_with_StableDiffusion

ollama_api_url = settings.OLLAMA_API_URL
llm = Ollama(base_url=ollama_api_url, model='gemma2:2b', request_timeout=600.0)


def api_generate_img(prompt):
    generate_img_with_StableDiffusion(prompt)

# 文書を解析してAPI（最終的にはホットペッパーグルメと楽天）を起動する
def use_api_tool(chat):
    analyze_prompt_tool_dicision = f"""
        あなたは以下のチャットを解析して、特に最近のコメントを解析して起動する必要のあるAPIを以下の中から選定するAIです。
        グルメAPI:レストランを紹介するAPI。食べ物やレストランの話が初めて出てきたときに起動。
        旅行API:旅行先を紹介するAPI。旅行や観光の話が初めて出てきた時に起動。
        グッズAPI:グッズを紹介するAPI。グッズやアイテムなど一般的なECサイトで扱われているものの話が初めて出てきた時に起動。
        ファッションAPI:ファッションアイテムを紹介するAPI。洋服の話が初めて出てきた時に起動。
        noAPI:上記のAPIを起動する必要がないときに起動。

        チャット履歴
        {chat}

        起動するAPI:
    """
    
    tool = llm.complete(analyze_prompt_tool_dicision, temperature=0).text
    pass

def use_api_sd(chat, sd_base_prompt):
    analyze_prompt_sd_prompt = f"""
        あなたは以下のチャットの履歴を解析して、stable-diffusionに入力するためのプロンプトを生成するAIである。
        生成するプロンプトはstable-diffusionでチャット履歴の中の最後のメッセージの様子を描画するものである。
        
        チャット:
        {chat}

        stable-diffusion向けプロンプト:
        {sd_base_prompt}
    """
    sd_extra_prompt = llm.complete(analyze_prompt_sd_prompt)
    api_generate_img(sd_base_prompt + sd_extra_prompt)