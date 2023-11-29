import time
import json
import hashlib
import random
import requests
import base64
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
env_file = os.environ

temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp")
if not os.path.exists(temp_path):
    os.mkdir(temp_path)
else:
    for file in os.listdir(temp_path):
        os.remove(os.path.join(temp_path, file))

def Img_To_Text(image_url = None,image_base64 = None):
    # 签名对象
    getSha256 = lambda content: hashlib.sha256(content.encode("utf-8")).hexdigest()

    secret_id = env_file.get("AIGC_SECRET_ID")
    secret_key = env_file.get("AIGC_SECRET_KEY")

    # 请求地址
    url = "https://api.aigcaas.cn/v3/application/image_recognition/action/paddleocr"
    # 构建请求头
    nonce = str(random.randint(1, 10000))
    timestamp = str(int(time.time()))
    token = getSha256(("%s%s%s" % (timestamp, secret_key, nonce)))
    headers = {
        'SecretID': secret_id,
        'Nonce': nonce,
        'Token': token,
        'Timestamp': timestamp,
        'Content-Type': 'application/json'
    }

    # 构建请求 body，可以自行根据上面的内容，添加更多参数
    data = {
        "image_base64": image_base64,
        "image_url": image_url,
        "ocr_type": "ocr"
    }

    # 获取响应
    response = requests.request("POST", url, headers=headers, data=json.dumps(data))
    response_dict = json.loads(response.text)
    if response_dict['status'] == 'Success':
        res_msg = response_dict["data"]
        return res_msg
    else:
        return -1

# 读取单张图片的内容
def Img2Text(img_path):
    print(f'正在进行图像的向量化')
    try:
        with open(img_path, "rb") as f:
            base64_image = base64.b64encode(f.read()).decode("utf-8")
            # 将图片转换为Base64字符串
            # image_bytes = bytes(img)  # 首先转化为字节串格式
            text = Img_To_Text(image_base64 = base64_image)
            file = os.path.basename(img_path)
            txt_file = file.rsplit(".", 1)[0] + ".txt"
            with open(os.path.join(temp_path, txt_file), "w", encoding="utf-8") as f:
                f.write(text)
            print(f'图像的向量化完成, 保存在{os.path.join(temp_path, txt_file)}')
            return os.path.join(temp_path, txt_file)
    except:
        return -1
