import cv2
import PIL
import numpy as np
from PIL import Image
from pathlib import Path


def imshow(img, winname='test', delay=0):
    """cv2展示图片"""
    cv2.imshow(winname, img)
    cv2.waitKey(delay)
    cv2.destroyAllWindows()


def pil_to_cv2(img):
    """
    pil转cv2图片
    :param img: pil图像, <type 'PIL.JpegImagePlugin.JpegImageFile'>
    :return: cv2图像, <type 'numpy.ndarray'>
    """
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
    return img


def bytes_to_cv2(img):
    """
    二进制图片转cv2
    :param img: 二进制图片数据, <type 'bytes'>
    :return: cv2图像, <type 'numpy.ndarray'>
    """
    # 将图片字节码bytes, 转换成一维的numpy数组到缓存中
    img_buffer_np = np.frombuffer(img, dtype=np.uint8)
    # 从指定的内存缓存中读取一维numpy数据, 并把数据转换(解码)成图像矩阵格式
    img_np = cv2.imdecode(img_buffer_np, 1)
    return img_np


def cv2_open(img, flag=None):
    """
    统一输出图片格式为cv2图像, <type 'numpy.ndarray'>
    :param img: <type 'bytes'/'numpy.ndarray'/'str'/'Path'/'PIL.JpegImagePlugin.JpegImageFile'>
    :param flag: 颜色空间转换类型, default: None
        eg: cv2.COLOR_BGR2GRAY（灰度图）
    :return: cv2图像, <numpy.ndarray>
    """
    if isinstance(img, bytes):
        img = bytes_to_cv2(img)
    elif isinstance(img, (str, Path)):
        img = cv2.imread(str(img))
    elif isinstance(img, np.ndarray):
        img = img
    elif isinstance(img, PIL.Image.Image):
        img = pil_to_cv2(img)
    else:
        raise ValueError(f'输入的图片类型无法解析: {type(img)}')
    if flag is not None:
        img = cv2.cvtColor(img, flag)
    return img


def get_distance(bg, tp, im_show=False, im_write=False, save_path=None):
    """
    :param bg: 背景图路径或 Path 对象或图片二进制
               eg: 'assets/bg.jpg'、Path('assets/bg.jpg')
    :param tp: 缺口图路径或 Path 对象或图片二进制
               eg: 'assets/tp.jpg'、Path('assets/tp.jpg')
    :param im_show: 是否显示结果, <type 'bool'>; default: False
    :param save_path: 保存路径, <type 'str'/'Path'>; default: None
    :return: 缺口位置
    """
    # 读取图片
    bg_img = cv2_open(bg)
    tp_gray = cv2_open(tp, flag=cv2.COLOR_BGR2GRAY)

    # 金字塔均值漂移
    bg_shift = cv2.pyrMeanShiftFiltering(bg_img, 5, 50)

    # 边缘检测
    tp_gray = cv2.Canny(tp_gray, 255, 255)
    bg_gray = cv2.Canny(bg_shift, 255, 255)

    # 目标匹配
    result = cv2.matchTemplate(bg_gray, tp_gray, cv2.TM_CCOEFF_NORMED)
    # 解析匹配结果
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    distance = max_loc[0]
    if save_path or im_show:
        # 需要绘制的方框高度和宽度
        tp_height, tp_width = tp_gray.shape[:2]
        # 矩形左上角点位置
        x, y = max_loc
        # 矩形右下角点位置
        _x, _y = x + tp_width, y + tp_height
        # 绘制矩形
        bg_img = cv2_open(bg)
        cv2.rectangle(bg_img, (x, y), (_x, _y), (0, 0, 255), 2)
        # 保存缺口识别结果到背景图
        if save_path:
            save_path = Path(save_path).resolve()
            save_path = save_path.parent / f"{save_path.stem}{save_path.suffix}"
            save_path = save_path.__str__()
            cv2.imwrite(save_path, bg_img)
        # 显示缺口识别结果
        if im_show:
            imshow(bg_img)
        if im_write:
            cv2.imwrite('distinguish.jpg', bg_img)
    return distance


# 生成轨迹

import random


def __ease_out_expo(sep):
    """
    缓动函数 easeOutExpo
    参考：https://easings.net/zh-cn#easeOutExpo
    """
    if sep == 1:
        return 1
    else:
        return 1 - pow(2, -10 * sep)


def get_slide_track(distance, time_):
    """
    根据滑动距离生成滑动轨迹
    :param distance: 需要滑动的距离
    :return: 滑动轨迹<type 'list'>: [[x,y,t], ...]
        x: 已滑动的横向距离
        y: 已滑动的纵向距离, 除起点外, 均为0
        t: 滑动过程消耗的时间, 单位: 毫秒
    """

    if not isinstance(distance, int) or distance < 0:
        raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")
    # 初始化轨迹列表
    slide_track = [
        [random.randint(5, 7)+ random.uniform(0.000000000000001, 0.999999999999999), 324, time_],
    ]
    # 共记录count次滑块位置信息
    count = 30 + int(distance / 2)
    # 初始化滑动时间
    t = time_
    # 记录上一次滑动的距离
    _x = 0
    _y = 324
    for i in range(count):
        # 已滑动的横向距离
        if i == 0:
            x = random.randint(7, 10) +  random.uniform(0.0000000000000001, 0.999999999999999)
        else:
            x = round(__ease_out_expo(i / count) * distance) + random.uniform(0.000000000000001, 0.999999999999999)
        # 滑动过程消耗的时间
        t += random.randint(7, 10)
        if x == _x:
            continue
        slide_track.append([x, 324, t])
        _x = x
    slide_track.append(slide_track[-1])
    return slide_track

import base64
from Crypto.Cipher import AES


def pkcs7padding(text):
    need_size = 16
    text_length = len(text)
    bytes_length = len(text.encode('utf-8'))
    padding_size = text_length if (bytes_length == text_length) else bytes_length
    padding = need_size - padding_size % need_size
    padding_text = chr(padding) * padding
    return text + padding_text


def AES_Encryption(secret_key=None, text=None):
    if (secret_key is None) or len(secret_key) == 0:
        secret_key = secret_key
    text = pkcs7padding(text)
    aes = AES.new(secret_key.encode("utf-8"), AES.MODE_ECB)
    en_text = aes.encrypt(text.encode('utf-8'))
    result = str(base64.b64encode(en_text), encoding='utf-8')
    return result



if __name__ == '__main__':
    print(get_slide_track(188, 1688349638059))