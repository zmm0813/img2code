# coding=gbk
import os
from PIL import Image
from aip import AipOcr

# 你的 APPID AK SK
APP_ID = '25847667'
API_KEY = 'cEsGZXeYvd2r1b4GvUYaLOE2'
SECRET_KEY = 'ZCO7sEd4zcHXQMO0hCxiCkwFaf5oxOtP'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_content(filePath):
    with open(filePath, "rb") as fp:
        return fp.read()


def get_str(img):
    image_path = img + '.png'
    change_path = img + '(1).png'
    img = Image.open(image_path)

    if img.size[0] < 15 or img.size[1] < 15:
        ResizeImage(image_path, change_path)
        image_path = change_path

    image = get_file_content(image_path)
    options = {
        "detect_direction": "true",
        "detect_language": "true"
    }
    res_image = client.basicGeneral(image, options)

    if len(res_image['words_result']) > 0:
        return res_image['words_result'][0]['words']
    else:
        return 'failed detection'


def ResizeImage(filein, fileout):
    img = Image.open(filein)

    if img.size[0] < 15:
        width = 20
        height = int(img.size[1] * 20 / img.size[0])
        out = img.resize((width, height), Image.LANCZOS)  # 使用 Image.LANCZOS 替换 Image.ANTIALIAS
    elif img.size[1] < 15:
        height = 20
        width = int(img.size[0] * 20 / img.size[1])
        out = img.resize((width, height), Image.LANCZOS)  # 使用 Image.LANCZOS 替换 Image.ANTIALIAS
    else:
        return

    out.save(fileout, format='PNG')  # 使用 format 参数替代 type
    return