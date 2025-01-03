from llama_index.llms.ollama import Ollama

import random
import json

import os

from django.conf import settings

ollama_api_url = settings.OLLAMA_API_URL
llm = Ollama(base_url=ollama_api_url, model='gemma2:2b', request_timeout=600.0)

class Person():
    def __init__(self, profile) -> None:
        self.profile = profile

    def save_profile(self):
        with open('tmp.json', 'wt') as f:
            json.dump(di, f)
        pass

cwd = os.getcwd()

with open(cwd+'/app1/util/mbti.json','r',encoding="utf-8_sig") as f:
    mbti_js = json.load(f)

with open(cwd+'/app1/util/profiles.json','r',encoding="utf-8_sig") as f:
    profiles_js = json.load(f)

mbti_list = [['E','I'],['S','N'],['T','F'],['J','P']]

mbti_explanation0 ="""
    <MBTI:>
    エネルギーの方向 | 外向型（E）もしくは内向型（I）
    興味や関心など、エネルギーの方向性を示すカテゴリーです。自分のエネルギーの源が人と接する外側に向いているのか、自分の時間を大切にする内側に向いているのかが分かります。

    「外向型（E：Extraversion）」は社交的で、人や活動からエネルギーを得ることを好み、周囲の人や環境を重視します。
    「内向型（I：Introversion）」は前に出たくない性格で、エネルギーを内省や単独での活動から得る傾向があり、自己の内面や個人的な価値観を重んじます。

    ものの見方 | 感覚型（S）もしくは直観型（N）
    ものの見方や認識のスタイルを意味するカテゴリーです。情報を受け取ったときに、事実をベースに解釈するのか、未来や概念を重視して解釈するのかが分かります。

    「感覚型（S：Sensing）」は現実重視タイプで、具体的な事実やデータに基づいて、物事を冷静に捉える能力があります。
    「直観型（N：Intuition）」は理想主義タイプで、可能性や将来の展望に目を向け、目に見えない要素や未来の展望に深い関心を持ちます。

    判断の仕方 | 思考型（T）もしくは感情型（F）
    判断や意思決定の基準を示すカテゴリーです。なにかを判断するときに、真実を優先するのか、人の気持ちを優先するのかが分かります。

    「思考型（T：Thinking）」は論理重視型で、判断を下す際に論理や客観性を重視し、事実や原則に基づいて冷静に決断を下す傾向があります。
    「感情型（F：Feeling ）」は感情重視型で、判断を下す際に人間関係や感情を重視し、調和や共感を大切にする傾向があります。

    外部との接し方 | 判断型（J）もしくは知覚型（P）
    外部環境とのアプローチや態度を示すカテゴリーです。計画通りに進めたいのか、ある程度の余白が欲しいのかが分かります。

    「判断型（J：Judging）」は計画的で組織的なアプローチを好み、効率的に決断を下すことを重視します。
    「知覚型（P：Perceiving）」は柔軟性と適応力に優れ、臨機応変に対応できます。規則が苦手で、流れに任せた余裕のあるアプローチを好みます。
    """

persons = []

def get_profile(name=None, age='', gender='', job='', hobby='', mbti=None, id=None, new_prof=False):
    
    if id is None:
        while True:
            id = random.randint(0,3)
            if id not in persons:
                persons.append(id)
                break
    if not new_prof:
        if str(id) in profiles_js:
            return profiles_js[str(id)]['name'],profiles_js[str(id)]['prof']
    if mbti is None:
        mbti = random.choice(mbti_list[0])+random.choice(mbti_list[1])+random.choice(mbti_list[2])+random.choice(mbti_list[3])
    if name is None:
        names = []
        for i, values in profiles_js.items():
            try:
                names.append(values['name'])
            except:
                pass
        think_name = f"""
        <system prompt:>あなたは架空の人間'person'を創造するAIの一部で、
        以下のリストと重複がないように'person'の名前を作成する。{names}
        名前だけを出力して。
        <person>の性別は{gender}で名前は
        """
        name = llm.complete(think_name).text

    if job is None:
        think_job = f"""
        <system prompt:>あなたは架空の人間'person'を創造するAIの一部で、
        以下のリストと重複がないように'person'の職業を作成する。
        職業だけを出力して。
        <person>の性別は{gender}で名前は
        """
        job = llm.complete(think_job).text

    system_prompt = """
    <system prompt:>あなたは架空の人間'person'を創造するAIの一部で、'person'のプロフィールを作成する。
    初めに、<person setting:>のテンプレートで'person'を創造して。なお、MBTIは<MBTI:>で定義される。{}
    典型的な{}の人物は以下のように定義される。{}
    """.format(mbti_explanation0,mbti,mbti_js[mbti]["abs"])

    person_setting =f"""
    <person setting:>
    名前:<{name}>
    年齢:<{age}>
    性別:<{gender}>
    職業:<{job}>
    趣味:<{hobby}>
    性格(MBTI):<{mbti}>
    親しい人と過ごすとき<>
    親しくない人とすごすとき<>
    恋人と過ごすとき<>
    """

    profile = llm.complete(system_prompt + person_setting)

    system_prompt_MBTI = """
    <system prompt:>あなたは架空の人間'person'を創造するAIの一部で、'person'のmbti診断結果を作成する。
    初めに、<MBTI:>に基づいて<MBTI setting:>のテンプレートで'person'のmbti診断結果をアルファベット4文字で創造して。
    """
    profiles_js[str(id)] = {"name":name,"job":job,"prof":profile.text}
    with open('profiles.json', 'w', encoding="utf-8") as f:
        json.dump(profiles_js, f, indent=2, ensure_ascii=False)
    return name, profile



def get_chat(A_name=None,A_prof=None, B_name=None, B_prof=None, log=None):
    prompt = ""
    if A_name is not None and B_name is not None:
        prompt += f"あなたは二人の人間{A_name}と{B_name}のチャットでのやり取りの続きを生成するAIで、メッセージを必ず一つ生成します。"
    else:
        prompt += "あなたは人間のチャットのやり取りを生成するAIで、メッセージを必ず一つ生成します。"
    prompt += "可能な限りメッセージは20文字以内となるようにして。"
    if A_prof is not None and B_prof is not None:
        prompt += f"""
                メッセージを送信するユーザーのプロフィールは以下です。{A_prof}
                メッセージを受信するユーザーのプロフィールは以下です。{B_prof}
                """
    if log is not None:
        prompt += f"""チャットのログは以下です{log}"""
    prompt+=f"{A_name}:"
    _chat = llm.complete(prompt, temperature=2)
    print(_chat)
    #log = f"{log}\n{A_name}:{_chat.text}"
    #with open(log_path, 'w', encoding="utf-8") as f:
    #    json.dump(log, f, indent=2, ensure_ascii=False)
    return _chat.text

def AIchat(sender, receiver, log=None):
    #log_path = f"{cwd}/app1/util/logs/{min((sender.id,receiver.id))}_{max((sender.id,receiver.id))}.json"
    sender_name, sender_prof = get_profile(name=sender.username, id=sender.id)
    receiver_name, receiver_prof = get_profile(name=receiver.username, id=receiver.id)
    message = get_chat(A_name=sender_name, A_prof=sender_prof, B_name=receiver_name, B_prof=receiver_prof, log=log)
    return message


def chat_fin(log):
    prompt = f"""
    あなたは以下の二人の人間のチャットでのやり取りが終了したかどうかTrueまたはFalseでを判別するAIです。
    出力はTrue, Falseのいずれかだけを出力して。
    チャットのログは以下です{log}
    このチャットは終了している：
    """
    fin = llm.complete(prompt)
    print(fin)
    



def main():
    chat_log = ''
    nameA, profileA = get_profile(
        gender='女性',
        hobby='カフェ巡り、スイーツ巡り、インスタグラムにスイーツの写真を投稿すること',
        new_prof=True
    )
    print(profileA)
    nameB, profileB = get_profile(
        gender='女性',
        age='20',
        new_prof=True
    )
    print(profileB)
    speaking = 'A'
    for i in range(10):
        print(f'chat number {i}')
        if speaking=='A':
            chat_log += AIchat(nameA, profileA, nameB, profileB, log=chat_log)
            speaking = 'B'
        else:
            chat_log += AIchat(nameB, profileB, nameA, profileA,log=chat_log)
            speaking = 'A'
        chat_fin(log=chat_log)

if __name__=='__main__':
    main()