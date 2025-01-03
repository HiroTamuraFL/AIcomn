from requests.exceptions import ConnectionError, Timeout
import requests,base64,io

import cv2

import json

base_url = 'http://stable-diffusion:7860'

def load_controlnet_model(model):
	url_controlnet_setting = f"{base_url}/controlnet/settings"
	payload = {
		"controlnet_model": model  # ロードしたいモデル名
	}

	response = requests.post(url_controlnet_setting, json=payload)

	if response.status_code == 200:
		print("ControlNetモデルがロードされました。")
	else:
		print(f"モデルロード失敗: {response.text}")
		print(response.text)

def send_request_with_exception(Imgsetting):
	
	try:
		resp = requests.post(url=f'{base_url}/sdapi/v1/txt2img', json=Imgsetting)
		resp.raise_for_status()
		print(f'response.text:{resp.text}')
		return resp.json()
	except ConnectionError:
		print("Failed to connect to Stable Diffusion API. Is it running?")
	except Timeout:
		print("The request to Stable Diffusion API timed out.")
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
	# 明示的に None を返す
	return None

def easy_controlnet_args(input_image, control_type, control_weight=1):
	# Read Image in RGB order
	img = cv2.imread(input_image)

	# Encode into PNG and send to ControlNet
	retval, bytes = cv2.imencode('.png', img)
	encoded_image = base64.b64encode(bytes).decode('utf-8')
	#encoded_image = input_image
	if control_type=="canny":
		module = "canny"
		model = "control_lora_rank128_v11p_sd15_canny_fp16[5c99b5e5]"
	elif control_type=="depth":
		module = "depth_midas"
		model = "control_lora_rank128_v11f1p_sd15_depth_fp16 [09d26c32]"
	elif control_type=="open_pose":
		module = "openpose_full"
		model = "control_lora_rank128_v11p_sd15_openpose_fp16 [1f2abd70]"
	elif control_type=="reference":
		module = "reference_only"
		model = None
	elif control_type=="soft_edge":
		module = "softedge_pidinet"
		model = "control_lora_rank128_v11p_sd15_softedge_fp16 [918f47aa]"
	elif control_type=="normal":
		module = "normal_bae"
		model = "control_lora_rank128_v11p_sd15_normalbae_fp16 [586bcefe]"
	else:
		module = model = None
	available_models = requests.get(f'{base_url}/controlnet/model_list').json()['model_list']
	available_modules = requests.get(f'{base_url}/controlnet/module_list').json()['module_list']
	print(f'available_models:{available_models}')
	if model not in available_models or module not in available_modules:
		print(f'{model} or {module} not in all available models or modules')
		return
	load_controlnet_model(model)
	print(f'{model} and {module} are ready!!')
	return {
				"enabled": True,
				"image": encoded_image,
				"module": module,
				"model": model,
				"weight": control_weight,
			}
	pass

def change_model(model):
	option_payload = {
		"sd_model_checkpoint": model,
		# "CLIP_stop_at_last_layers": 2
	}

	response = requests.post(url=f'{base_url}/sdapi/v1/options', json=option_payload)

def generate_img_with_StableDiffusion(prompt, negative_prompt, ckpt, vae, filename, num_steps=20, img_size=[512,640], controlnet_args=None):
	print(f'''generate_img_with_SD called
	ckpt:{ckpt}
	prompt:{prompt}, 
	negative prompt:{negative_prompt}''')
	
	Imgsetting = {
		"prompt": prompt,
		"negative_prompt":negative_prompt,
		"steps": num_steps,
		"sampler_index":"DPM++ 2M Karras",
		"width": img_size[0],
		"height": img_size[1],
		"cfg_scale": 7,
		"seed": -1,
		"checkpoint":ckpt,
		"vae":vae,
		}

	if controlnet_args is not None:
		Imgsetting["alwayson_scripts"] = {"controlnet": {
					"args": [
							controlnet_args
						]
					}
		}

	#print(json.dumps(Imgsetting, indent=4))

	json = send_request_with_exception(Imgsetting)
	if json and "info" in json:
	    print("Info section:", json["info"])


	# ControlNetが適切に動作したか確認
	if "info" in json and "ControlNet" in json["info"]:
		print("ControlNetが適切に呼び出されました。")
	else:
		print("ControlNetの呼び出しに問題がある可能性があります。")
	# None チェックを追加
	if json is None:
		print("No response received from Stable Diffusion API. Exiting function.")
		return

	# "images" キーの存在確認
	if "images" not in json or not json["images"]:
		print("Response JSON does not contain 'images'. Exiting function.")
		return

	# 正常にデータを処理
	imgdata = json["images"][0]
	with open(filename, "wb") as f:
		buf = base64.b64decode(imgdata)
		f.write(buf)
	print(f"Image successfully generated and saved as {filename}")
	return

def gen_2d_img_yden(prompt, filename, negative_prompt="(worst quality, low quality:1.2),ugly,error,lowres,blurry,multipul angle, split view, grid view,text,signature,watermark,bad anatomy", img_size=[512,640], controlnet_args=None):
	ckpt = "yden_v30.safetensors [51c94b7aae]"
	vae = ".stable-diffusion-webui-docker/data/models/VAE/vae-ft-mse-840000-ema-pruned.ckpt"
	change_model(model=ckpt)
	generate_img_with_StableDiffusion(
		prompt=prompt, 
		negative_prompt=negative_prompt, 
		ckpt=ckpt, 
		vae=vae, 
		filename=filename, 
		img_size=img_size, 
		controlnet_args=controlnet_args
		)

def gen_3d_person_img_sdv1(prompt, filename, num_steps=10, img_size=[1024,1280], negative_prompt="", controlnet_args=None):
	ckpt = "yayoiMix_v20.safetensors [260570b6f8]"
	vae = ".stable-diffusion-webui-docker/data/models/VAE/vae-ft-mse-840000-ema-pruned.ckpt"
	change_model(model=ckpt)
	generate_img_with_StableDiffusion(
		prompt=prompt, 
		negative_prompt=negative_prompt, 
		ckpt=ckpt, 
		vae=vae, 
		filename=filename, 
		num_steps=num_steps, 
		img_size=img_size, 
		#controlnet_args=controlnet_args
		)

def gen_3d_person_img_sdxl(prompt, filename, num_steps=10, img_size=[1024,1280], negative_prompt="", controlnet_args=None):
	ckpt = "SDXL/hadukiMix_v15.safetensors [c97ffe1bf2]"
	vae = ".stable-diffusion-webui-docker/data/models/VAE/sdxl_vae.safetensors"
	change_model(model=ckpt)
	generate_img_with_StableDiffusion(
		prompt=prompt, 
		negative_prompt=negative_prompt, 
		ckpt=ckpt, 
		vae=vae, 
		filename=filename, 
		num_steps=num_steps, 
		img_size=img_size, 
		#controlnet_args=controlnet_args
		)

