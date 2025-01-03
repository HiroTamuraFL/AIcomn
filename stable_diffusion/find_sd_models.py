import requests
from pprint import pprint

def listup_sd_models():
    sd_models = requests.get('http://stable-diffusion:7860/sdapi/v1/sd-models').json()

    sd_models = [model["title"] for model in sd_models]

    # pprint(sd_models)

    with open("stable_diffusion/sd_model.txt", '+w', encoding='UTF-8') as f:
        f.write('\n'.join(sd_models))