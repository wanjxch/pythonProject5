# -*- coding: utf-8 -*-
# @Time : 2020/12/24 13:46
# @Author : edward
# @Email : Edward_shang@yunquna.com
# @File : OOCLtracing.py
# @Software: PyCharm
# @project: spider_test1
from lxml import etree
from parsel import Selector
import json
import random
import re
import time
import requests
import numpy as np
import cv2
import datetime
import cloudscraper
import base64
from Crypto.Cipher import AES
import execjs

requests.packages.urllib3.disable_warnings()

code_200 = 200
code_201 = 201
code_202 = 202
code_203 = 203
code_204 = 204
code_205 = 205


def bill_info_item():
    bill_item = {}
    bill_item["bl_no"] = ""
    bill_item["depart"] = ""
    bill_item["arrive"] = ""
    bill_item["load"] = ""
    bill_item["discharge"] = ""
    bill_item["carrier_id"] = ""
    bill_item["carrier_code"] = ""
    bill_item["vessel_name"] = ""
    bill_item["voyage"] = ""
    bill_item["request_url"] = ""
    bill_item["task_id"] = ""
    bill_item["booking_no"] = ""
    bill_item["bl_type"] = ""
    bill_item["bl_surrendered_status"] = ""
    bill_item["bl_status"] = ""
    bill_item["inbound_customs_clearance_status"] = ""
    bill_item["inbound_customs_clearance_date"] = ""
    bill_item["container_count"] = ""  # 必填字段
    bill_item["service_mode"] = ""
    bill_item["service_requirement"] = ""
    bill_item["vgm_cut_off_date"] = ""
    bill_item["vgm_received"] = ""
    bill_item["port_cut_off_date"] = ""
    bill_item["gross_weight"] = ""
    bill_item["measurement"] = ""
    bill_item["eta_at_place_of_delivery"] = ""
    bill_item["manifest_quantity"] = ""
    bill_item["on_board_date"] = ""
    bill_item["gis_depart_port_id"] = ""
    bill_item["gis_depart_port_code"] = ""
    bill_item["gis_arrive_port_id"] = ""
    bill_item["gis_arrive_port_code"] = ""
    bill_item["container_list"] = []
    return bill_item


def container_info_item():
    contaienr_item = dict()
    contaienr_item["bl_no"] = ""
    contaienr_item["container_no"] = ""
    contaienr_item["seal_no"] = ""
    contaienr_item["container_size"] = ""
    contaienr_item["container_type"] = ""
    contaienr_item["event_list"] = []
    contaienr_item["container_weight"] = ""
    contaienr_item["cargo_weight"] = ""
    contaienr_item["real_cargo_weight"] = ""
    contaienr_item["service_type"] = ""
    contaienr_item["eta"] = ""
    contaienr_item["ata"] = ""
    contaienr_item["pod"] = ""
    contaienr_item["latest_location_date"] = ""
    contaienr_item["latest_event_name"] = ""
    contaienr_item["latest_location"] = ""
    contaienr_item["remaining_days"] = ""
    contaienr_item["laden_return"] = ""
    contaienr_item["cargo_pickup"] = ""
    contaienr_item["empty_pick_up_date"] = ""
    contaienr_item["empty_return_date"] = ""
    contaienr_item["quantity"] = ""
    return contaienr_item


def tracking_event_item():
    event_item = {}
    event_item["vessel_name"] = ""
    event_item["voyage"] = ""
    event_item["transport_mode"] = ""
    event_item["event_name"] = ""
    event_item["a_time"] = ""
    event_item["e_time"] = ""
    event_item["location_name"] = ""
    event_item["location_type"] = ""
    return event_item


def return_tracking_info(receive_task_message: dict = None, bill_item: dict = None, container_info: dict = None):
    """
    返回的提单基本信息数据结构报文
    :param receive_task_message: 接受的任务消息报文
    :param bill_item: 爬取的提单信息报文
    :param container_info: 爬取的集装箱信息报文
    :return:
    """
    return_data = {
        "receiveTaskMessage": receive_task_message,
        "billInfo": bill_item,
        "containerInfo": container_info
    }
    return return_data


def clean_str(original_str):
    if original_str:
        cleaned_str = original_str
        cleaned_str = cleaned_str.replace('\r', '')
        cleaned_str = cleaned_str.replace('\t', '')
        cleaned_str = cleaned_str.replace('\n', '')
        cleaned_str = cleaned_str.strip()
        return cleaned_str
    else:
        return ''


def replace_time(t1):
    new_date = re.findall(r'[\s\S]+(?=\s)', t1, re.S)[0]
    return new_date


def format_date(date_string):
    """ 时间格式标准化 """
    import re
    import time
    if not date_string:  # 31-Oct-2019 11:46
        return ''
    # 情况一："2019/10/25 17:02" >>> "2019-10-25 17:02:00"
    re_match_datetime_string_first = re.findall(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}', date_string, re.S)
    # 情况二："2019/10/25" >>> "2019-10-25 00:00:00"
    re_match_datetime_string_second = re.findall(r'\d{4}/\d{2}/\d{2}', date_string, re.S)
    # 情况三："2019-10-28T06:00:00.000" >>> "2019-10-28 06:00:00" """
    re_match_datetime_string_third = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}', date_string, re.S)
    # 情况四："NOV-03-2019 12:00" >>> "2019-11-03 12:00:00"
    re_match_datetime_string_forth = re.findall(r'[A-Z]{3}-\d{2}-\d{4} \d{2}:\d{2}', date_string, re.S)
    # 情况五："05 Nov 2019, 21:10" >>> "2019-11-05 21:10:00"
    re_match_datetime_string_fifth = re.findall(r'\d{2} [A-Za-z]{3} \d{4}, \d{2}:\d{2}', date_string, re.S)
    # 情况六："31-Oct-2019 11:46" >>> "2019-10-31 11:46:00"
    re_match_datetime_string_sixth = re.findall(r'\d{2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2}', date_string, re.S)
    # 情况七："30-Nov-2019" >>> "2019-11-30 00:00:00"
    re_match_datetime_string_seventh = re.findall(r'\d{2}-[A-Za-z]{3}-\d{4}', date_string, re.S)

    if re_match_datetime_string_first:
        time_struct = time.strptime(re_match_datetime_string_first[0], "%Y/%m/%d %H:%M")
        standard_time_format_string = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        return standard_time_format_string
    elif re_match_datetime_string_second:
        time_struct = time.strptime(re_match_datetime_string_second[0], "%Y/%m/%d")
        standard_time_format_string = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        return standard_time_format_string
    elif re_match_datetime_string_third:
        time_struct = time.strptime(re_match_datetime_string_third[0], "%Y-%m-%dT%H:%M:%S.%f")
        standard_time_format_string = time.strftime("%Y-%m-%d %H:%M:%S", time_struct)
        return standard_time_format_string
    elif re_match_datetime_string_forth:
        time_array = time.strptime(re_match_datetime_string_forth[0], '%b-%d-%Y %H:%M')
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
        return time_format
    elif re_match_datetime_string_fifth:
        time_array = time.strptime(re_match_datetime_string_fifth[0], "%d %b %Y, %H:%M")
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
        return time_format
    elif re_match_datetime_string_sixth:
        time_array = time.strptime(re_match_datetime_string_sixth[0], "%d-%b-%Y %H:%M")
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
        return time_format
    elif re_match_datetime_string_seventh:
        time_array = time.strptime(re_match_datetime_string_seventh[0], "%d-%b-%Y")
        time_format = time.strftime('%Y-%m-%d %H:%M:%S', time_array)
        return time_format
    else:
        return ''


def transfor_standard_datetime_to_timestamp(datetime_str):
    """
    将标准时间转化为时间戳
    :param datetime_str: "2019-10-25 17:02:00"
    :return: 1571994120
    """
    if datetime_str:
        # 先转为时间数组
        time_array = time.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        # 转换为时间戳
        time_stamp = int(time.mktime(time_array))
        a_time = None
        e_time = None
        if time_stamp < int(time.time()):
            a_time = datetime_str
        else:
            e_time = datetime_str
        return a_time, e_time
    else:
        return None


import math


def texts(var1, Challenge):
    var1 = int(var1)
    var_str = str(Challenge)
    var_arr = list(var_str)
    LastDig = var_arr[-1]
    var_arr.sort()
    minDig = sorted(var_arr)[0]
    subvar1 = (2 * int(var_arr[2])) + (int(var_arr[1]) * 1)
    subvar2 = str(2 * int(var_arr[2])) + var_arr[1]
    my_pow = math.pow(int(var_arr[0]) * 1 + 2, int(var_arr[1]))
    x = (var1 * 3 + subvar1) * 1
    y = math.cos(math.pi * int(subvar2))
    answer = x * y
    answer -= my_pow * 1
    answer += (int(minDig) * 1) - (int(LastDig) * 1)
    answer = str(int(answer)) + str(subvar2)
    return answer


def retry(tries):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < tries:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += 1

        return wrapper

    return decorator


def random_list(start, stop, length):
    if length >= 0:
        length = int(length)
        start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


class OOCLPareseTracking(object):

    def __init__(self, message):
        self.message = message

        # self.ver_code = "http://9813.pro.yqn.corp:9813/oocl/slider"  # 生产环境
        # self.origin_task_message = deepcopy(self.message.busiData)
        self.busi_data = self.message.get_business_data()
        agent_domain = self.message.get_proxies().get('agentDomain')
        proxy_host = agent_domain.split(':')[0]
        proxy_port = agent_domain.split(':')[1]
        proxy_user = self.message.get_proxies().get('agentAccount')
        proxy_pass = self.message.get_proxies().get('agentToken')
        if proxy_user:
            proxy_meta = "http://%s:%s@%s:%s" % (proxy_user, proxy_pass, proxy_host, proxy_port)
        else:
            proxy_meta = "http://%s:%s" % (proxy_host, proxy_port)
        self.proxies = {
            "http": proxy_meta,
            "https": proxy_meta
        }
        n1 = random.randint(0, 9)
        n2 = random.randint(0, 9)
        n3 = random.randint(0, 9)
        n4 = random.randint(0, 9)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Referer': 'https://www.oocl.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53{n1}.3{n2} (KHTML, like Gecko) Chrome/10{n3}.{n4}.{n3}.0 Safari/53{n1}.3{n2}',
            'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.session = requests.session()
        self.session.headers = headers
        self.session.verify = False
        # self.session = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        # self.isSession = True
        self.session.proxies = self.proxies
        self.timeOut = 30
        self.spiderData = {}  # 存放接口爬取原始数据
        self.pol_pot_pod_list = []

    def spider_Data(self, url, response):
        try:
            self.spiderData[url] = response.text
        except Exception as e:
            pass

    def extract_first(self, values):
        for value in values:
            if value is not None or value != '':
                return value.strip()

    def get_container(self, appKey, sessionKey):

        back = ''
        time1 = str(int(time.time() * 1000))
        for i in range(16):
            back += str(random.randint(0, 9))
        jsonpCallback = f'jQuery1800{back}_{time1}'
        params = {
            'appKey': appKey,
            'captchaType': 'blockPuzzle',
            'sessionKey': sessionKey,
            'jsonpCallback': jsonpCallback,
            '_': str(int(time.time() * 1000)),
        }
        for _ in range(5):
            try:
                url = 'https://cs-captcha-public.cargosmart.com/captcha/public/get'
                response = self.session.get(url=url, params=params, timeout=self.timeOut)
                if response.status_code == 200:
                    break
                time.sleep(1)
            except Exception as e:
                time.sleep(1)
                if _ == 4:
                    break
        originalImageBase64 = re.search(r'originalImageBase64":"(.*?)",', response.text, re.S).group(1)
        jigsawImageBase64 = re.search(r'jigsawImageBase64":"(.*?)",', response.text, re.S).group(1)
        bigimgdata = base64.b64decode(originalImageBase64)
        litimgdata = base64.b64decode(jigsawImageBase64)

        def get_distance(pic_path1, pic_path2):
            pic_path_rgb1 = cv2.imdecode(np.frombuffer(pic_path1, np.uint8), cv2.IMREAD_COLOR)
            pic_path_gray1 = cv2.cvtColor(pic_path_rgb1, cv2.COLOR_BGR2GRAY)
            can1 = cv2.Canny(pic_path_gray1, threshold1=200, threshold2=300)
            pic_path_rgb2 = cv2.imdecode(np.frombuffer(pic_path2, np.uint8), cv2.IMREAD_COLOR)
            pic_path_gray2 = cv2.cvtColor(pic_path_rgb2, cv2.COLOR_BGR2GRAY)
            can2 = cv2.Canny(pic_path_gray2, threshold1=200, threshold2=300)
            res = cv2.matchTemplate(can1, can2, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            return max_loc

        distance = int(get_distance(bigimgdata, litimgdata)[0]) - 8

        def __ease_out_expo(sep):
            if sep == 1:
                return 1
            else:
                return 1 - pow(2, -10 * sep)

        def num():
            re = ''
            for i in range(15):
                re += str(random.randint(1, 9))
            return re

        def get_slide_track(distance):
            if not isinstance(distance, int) or distance < 0:
                raise ValueError(f"distance类型必须是大于等于0的整数: distance: {distance}, type: {type(distance)}")
            slide_track = [
                {"x": 0, "y": 335, "timestamp": str(int(time.time() * 1000))},
                {"x": 2, "y": 336, "timestamp": str(int(time.time() * 1000))},
            ]
            count = 30 + int(distance / 2)
            _x = 0
            _y = 0
            for i in range(count):
                x = round(__ease_out_expo(i / count) * distance)
                if x == _x:
                    continue
                time.sleep(0.01)
                x1 = f'{x}.{num()}'
                y = random.randint(-2, 2)
                y = 365 + y
                slide_track.append({"x": float(x1), "y": y, "timestamp": str(int(time.time() * 1000))})
                _x = x
            slide_track.append(slide_track[-1])
            return slide_track

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

        res = get_slide_track(distance)
        token = re.search(r'"token":"(.*?)"', response.text, re.S).group(1)
        secretKey = re.search(r'secretKey":"(.*?)",', response.text, re.S).group(1)
        pointJson = res[-1]
        pointJson['y'] = 5
        pointJson = str(pointJson)
        pointJson = AES_Encryption(secret_key=secretKey, text=pointJson)
        mousePoint = str(res)
        mousePoint = AES_Encryption(secret_key=secretKey, text=mousePoint)
        num_list = [448, 448, 448, 448, 448, 447, 447, 446, 445, 445, 444, 443, 442, 441, 441, 440, 439, 438, 434, 431,
                    428, 426, 421, 419, 417, 415, 413, 410, 409, 403, 400, 396, 393, 389, 382, 379, 372, 365, 361, 353,
                    349, 342, 339, 333, 319, 305, 298, 293, 289, 281, 280, 277, 278, 277, 274, 274, 274, 274, 274, 274,
                    274, 274, 275, 275, 274, 272, 268, 266, 263, 262, 262, 262, 262, 262, 262, 262, 262, 262, 262, 262,
                    262, 262, 262, 262, 262, 261, 260, 260, 259, 259, 258, 258, 258, 257, 257, 257, 256, 255, 255]
        i = 99
        while i > 89:
            i = i - 1
            num1 = random.randint(0, 98)
            num2 = num_list[num1]
            num_list[num1] = num_list[i]
            num_list[i] = num2
        manualMovementMousePoint = f'{num_list[89:]}'
        manualMovementMousePoint = AES_Encryption(secret_key=secretKey, text=manualMovementMousePoint)
        params = {
            'appKey': appKey,
        }
        json_data = {
            'captchaType': 'blockPuzzle',
            'pointJson': pointJson,
            'token': token,
            'sessionKey': sessionKey,
            'mousePoint': mousePoint,
            'startTime': res[0].get('timestamp'),
            'endTime': res[-1].get('timestamp'),
            'manualMovementMousePoint': manualMovementMousePoint,
        }
        for _ in range(5):
            try:
                url = 'https://cs-captcha-public.cargosmart.com/captcha/public/check'
                response = self.session.post(url=url, params=params, json=json_data, timeout=self.timeOut)
                if response.status_code == 200:
                    break
                time.sleep(1)
            except Exception as e:
                time.sleep(1)
                if _ == 4:
                    break
        back = ''
        time1 = str(int(time.time() * 1000))
        for i in range(16):
            back += str(random.randint(0, 9))
        jsonpCallback = f'jQuery1800{back}_{time1}'
        params = {
            'appKey': appKey,
            'captchaType': 'blockPuzzle',
            'sessionKey': sessionKey,
            'jsonpCallback': jsonpCallback,
            '_': str(int(time.time() * 1000)),
        }
        response = self.session.get('https://cs-captcha-public.cargosmart.com/captcha/public/get', params=params)
        token = re.search(r'token":"(.*?)",', response.text, re.S).group(1)
        token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
        return token

    def blno_search(self, response, token, sessionKey):

        meta = self.message.get_business_data()
        bill_item = bill_info_item()
        container_list = []
        bill_item['bl_no'] = meta.get('blNo')
        bill_item['carrier_id'] = meta.get('carrierId')
        bill_item['carrier_code'] = meta.get('carrierCode')
        bill_item['task_id'] = meta.get('taskId')
        response = etree.HTML(response.text)
        bill_item['depart'] = self.extract_first(response.xpath('//*[@id="form:PORLocation0"]/text()')) \
            if response.xpath('//*[@id="form:PORLocation0"]/text()') else ''
        bill_item['load'] = self.extract_first(response.xpath('//*[@id="form:POLLocation0"]/text()')) \
            if response.xpath('//*[@id="form:POLLocation0"]/text()') else ''

        pot_datas = response.xpath('//div[@id="Tab1"]//table[@id="eventListTable"]//tr')[1:]
        pot_count = len(pot_datas)

        if pot_count > 1:
            discharge = ''
            arrive = ''
            for index, pot_data in enumerate(pot_datas):
                index += 1
                if index == 1:
                    location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[4]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            atd = format_date(date)
                            etd = ''
                        else:
                            etd = format_date(date)
                            atd = ''
                    else:
                        etd = ''
                        atd = ''

                    vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                    vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                        self.extract_first(pot_data.xpath('./td[5]/text()')))
                    span_tab_list = pot_data.xpath('./td[5]/span')
                    span_tab_list1 = pot_data.xpath('./td[5]/text()')
                    voyage_no = ''
                    if span_tab_list:
                        voyage = ''
                        if len(span_tab_list) == 1:
                            for span_tab in span_tab_list:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage_section if voyage_section else ''
                                voyage_no = voyage.strip()
                        else:
                            for span_tab in span_tab_list[:-1]:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage + '/' + voyage_section if voyage else voyage_section
                                voyage_no = voyage.strip()
                    elif span_tab_list1:
                        voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                        voyage_no = voyage.strip() if voyage else ""

                    pol_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Departure_POL",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(pol_data)
                    location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[6]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[6]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            pot_atd = format_date(date)
                            pot_etd = ''
                        else:
                            pot_atd = ''
                            pot_etd = format_date(date)
                    else:
                        pot_etd = ''
                        pot_atd = ''

                    potl_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Berth_Transit",
                        "a_time": pot_atd,
                        "e_time": pot_etd,
                    }

                    self.pol_pot_pod_list.append(potl_data)

                elif index == pot_count:
                    dock_name = pot_data.xpath('./td[7]/text()')
                    if dock_name:
                        dock_name = dock_name[0].strip()
                    else:
                        dock_name = ''
                    location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[4]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            pot_atd = format_date(date)
                            pot_etd = ''
                        else:
                            pot_atd = ''
                            pot_etd = format_date(date)
                    else:
                        pot_etd = ''
                        pot_atd = ''
                    vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                    vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                        self.extract_first(pot_data.xpath('./td[5]/text()')))
                    span_tab_list = pot_data.xpath('./td[5]/span')
                    span_tab_list1 = pot_data.xpath('./td[5]/text()')
                    voyage_no = ''
                    if span_tab_list:
                        voyage = ''
                        if len(span_tab_list) == 1:
                            for span_tab in span_tab_list:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage_section if voyage_section else ''
                                voyage_no = voyage.strip()
                        else:
                            for span_tab in span_tab_list[:-1]:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage + '/' + voyage_section if voyage else voyage_section
                                voyage_no = voyage.strip()
                    elif span_tab_list1:
                        voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                        voyage_no = voyage.strip() if voyage else ""

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Departure_Transit",
                        "a_time": pot_atd,
                        "e_time": pot_etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)
                    location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    discharge = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    arrive = pot_data.xpath('./td[8]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[7]/span[1]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[7]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            atd = format_date(date)
                            etd = ''
                        else:
                            etd = format_date(date)
                            atd = ''
                    else:
                        etd = ''
                        atd = ''

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Berth_POD",
                        "a_time": atd,
                        "e_time": etd,
                        "dock_name": dock_name
                    }
                    self.pol_pot_pod_list.append(potd_data)

                else:

                    location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[4]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            pot_atd = format_date(date)
                            pot_etd = ''
                        else:
                            pot_atd = ''
                            pot_etd = format_date(date)
                    else:
                        pot_etd = ''
                        pot_atd = ''
                    vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                    vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                        self.extract_first(pot_data.xpath('./td[5]/text()')))
                    span_tab_list = pot_data.xpath('./td[5]/span')
                    span_tab_list1 = pot_data.xpath('./td[5]/text()')
                    voyage_no = ''
                    if span_tab_list:
                        voyage = ''
                        if len(span_tab_list) == 1:
                            for span_tab in span_tab_list:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage_section if voyage_section else ''
                                voyage_no = voyage.strip()
                        else:
                            for span_tab in span_tab_list[:-1]:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage + '/' + voyage_section if voyage else voyage_section
                                voyage_no = voyage.strip()
                    elif span_tab_list1:
                        voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                        voyage_no = voyage.strip() if voyage else ""

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Departure_Transit",
                        "a_time": pot_atd,
                        "e_time": pot_etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)
                    location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[6]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[6]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            atd = format_date(date)
                            etd = ''
                        else:
                            etd = format_date(date)
                            atd = ''
                    else:
                        etd = ''
                        atd = ''

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Berth_Transit",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)

            bill_item['discharge'] = discharge
            bill_item['arrive'] = arrive

        elif pot_count == 1:
            discharge = ''
            arrive = ''
            for pot_data in pot_datas:

                dock_name = pot_data.xpath('./td[7]/text()')
                if dock_name:
                    dock_name = dock_name[0].strip()
                else:
                    dock_name = ''

                location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]

                arrive = clean_str(self.extract_first(pot_data.xpath('./td[8]/span[1]/text()')))
                date = pot_data.xpath('./td[4]/span[2]/text()')
                date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                    self.extract_first(pot_data.xpath('./td[5]/text()')))
                span_tab_list = pot_data.xpath('./td[5]/span')
                voyage_no = ''
                if span_tab_list:
                    voyage = ''
                    if len(span_tab_list) == 1:
                        for span_tab in span_tab_list:  # 航次拼接
                            voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                            voyage = voyage_section if voyage_section else ''
                            voyage_no = voyage.strip()
                    else:
                        for span_tab in span_tab_list[:-1]:  # 航次拼接
                            voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                            voyage = voyage + '/' + voyage_section if voyage else voyage_section
                            voyage_no = voyage.strip()
                            if voyage_no:
                                break

                else:
                    voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                    voyage_no = voyage.strip() if voyage else ""

                if not date:
                    etd = ''
                    atd = ''
                else:
                    date = date[0]
                    date_time = date.split(', ')
                    form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                    date = date_time[0].replace(' ', '-') + ' ' + form_date
                    if '(Actual)' in date_content:
                        atd = format_date(date)
                        etd = ''
                    else:
                        etd = format_date(date)
                        atd = ''

                pol_data = {
                    "vessel_name": vessel,
                    "voyage": voyage_no,
                    "location_name": location_name,
                    "event_name": "Departure_POL",
                    "a_time": atd,
                    "e_time": etd,
                }
                self.pol_pot_pod_list.append(pol_data)
                location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                discharge = location_name
                date = pot_data.xpath('./td[7]/span[1]/text()')
                date_content = ''.join(pot_data.xpath('./td[7]//text()'))
                if not date:
                    pot_atd = ''
                    pot_etd = ''
                else:
                    date = date[0]
                    date_time = date.split(', ')
                    form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                    date = date_time[0].replace(' ', '-') + ' ' + form_date
                    if '(Actual)' in date_content:
                        pot_atd = format_date(date)
                        pot_etd = ''
                    else:
                        pot_etd = format_date(date)
                        pot_atd = ''

                potl_data = {
                    "vessel_name": vessel,
                    "voyage": voyage_no,
                    "location_name": location_name,
                    "event_name": "Berth_POD",
                    "a_time": pot_atd,
                    "e_time": pot_etd,
                    "pod_dock_name": dock_name
                }

                self.pol_pot_pod_list.append(potl_data)
            bill_item['discharge'] = discharge
            bill_item['arrive'] = arrive

        vessel_voyage = None
        vessel_voyage_xpath = '//*[@id="contentTable"]//table[@class="sectionTable"]//td[contains(text(),"Vessel Voyage")]/following::td[1]/text()'
        if response.xpath(vessel_voyage_xpath):
            vessel_voyage = clean_str(self.extract_first(response.xpath(vessel_voyage_xpath)))
        if vessel_voyage:
            if re.findall(r'[\s\S]+(?=\s)', vessel_voyage, re.S):
                bill_item['vessel_name'] = re.findall(r'[\s\S]+(?=\s)', vessel_voyage, re.S)[0]
            if re.findall(r'[^\s]+$', vessel_voyage, re.S):
                bill_item['voyage'] = re.findall(r'[^\s]+$', vessel_voyage, re.S)[0]
        # 订舱号
        booking_no = self.extract_first(response.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[text()="Booking Number:"]/following::td[1]/text()'))
        bill_item['booking_no'] = re.findall(r'([\d]+)', booking_no)[0] if booking_no else None
        # 1 x 20' General Purpose Container
        container_count = self.extract_first(response.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[text()="Total Containers:"]/following::td[1]/text()'))
        if container_count:
            container_count = container_count.split('x')[0].strip()
            bill_item['container_count'] = int(container_count)
        # 293 Carton
        manifest_quantity = self.extract_first(response.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[text()="Total Quantity:"]/following::span[1]/text()'))
        if manifest_quantity:
            manifest_quantity = re.findall(r'[\d]+', manifest_quantity)[0]
            bill_item['manifest_quantity'] = manifest_quantity
        # Inbound Customs Clearance Status:
        iccs = self.extract_first(response.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[contains(text(),"Inbound Customs Clearance Status:")]/following::td[1]/text()'))
        bill_item['inbound_customs_clearance_status'] = iccs.strip() if iccs else None
        container_info_tr_list = response.xpath('//*[@id="summaryTable"]/tr')
        '//*[@id="cs_captcha"]'
        appKey = self.extract_first(response.xpath('//*[@id="cs_captcha"]/@app-key'))
        jsf_tree_64 = self.extract_first(response.xpath('//*[@id="jsf_tree_64"]/@value'))
        jsf_state_64 = self.extract_first(response.xpath('//*[@id="jsf_state_64"]/@value'))

        anonymous_token = self.extract_first(response.xpath('//*[@id="ANONYMOUS_TOKEN"]/@value'))

        con_list = []
        for index, tr in enumerate(container_info_tr_list[2:]):
            container_info = container_info_item()
            container_info['bl_no'] = meta.get('blNo')
            container_no = self.extract_first(tr.xpath('./td/a/text()'))
            if container_no and '-' in container_no:
                container_no_parme = container_no.split('-')[0]
                container_info['container_no'] = ''.join(container_no.split('-'))
            else:
                container_no_parme = container_no
                container_info['container_no'] = container_no
            bill_item['container_list'].append(container_info['container_no'])
            container_size_type = tr.xpath('./td[2]/span/text()')[0] if tr.xpath('./td[2]/span/text()') else ''
            if container_size_type:
                container_size = re.findall(r'([\d]+)', container_size_type)[0]
                container_type = container_size_type.replace(container_size, '').strip()
                container_info['container_size'] = container_size
                container_info['container_type'] = container_type
            else:
                container_info['container_size'] = ''
                container_info['container_type'] = ''
            quantity = tr.xpath('./td[3]/span/text()')[0]
            if quantity:
                container_info['quantity'] = re.findall(r'([\d]+)', quantity)[0]
            container_weight = tr.xpath('./td[4]/span/text()')[0]
            if container_weight:
                container_info['container_weight'] = container_weight
            # VGM
            # vgm = tr.xpath('./td[5]/text()')[0]
            # current status
            latest_event_name = self.extract_first(tr.xpath('./td[6]/text()'))
            container_info['latest_event_name'] = latest_event_name.strip() if latest_event_name else ''
            latest_location = self.extract_first(tr.xpath('./td[7]/span/text()'))
            container_info['latest_location'] = latest_location.strip() if latest_location else ''
            # 05 Oct 2019, 06:49 ZAT
            event_time = self.extract_first(tr.xpath('./td[8]/span/text()'))
            if event_time:
                event_time = replace_time(event_time)
                container_info['latest_location_date'] = format_date(event_time)
            # eta  | 22 Sep 2019, 08:00  Local
            eta = self.extract_first(tr.xpath('td[9]//tr[2]/td/span/text()'))
            if eta:
                modify_eta = replace_time(eta.strip())
                container_info['eta'] = format_date(modify_eta.strip())
            # pod
            container_info['pod'] = self.extract_first(tr.xpath('td[9]//tr[1]/td/span/text()'))
            container_list.append(container_info)
            # form_link = 'form:link' + str(index)
            for _ in range(5):
                try:
                    # token, sessionKey = self.get_container(appKey)
                    # if not token:
                    #     continue
                    # cookies = {
                    #     'cscaptachaCookie': sessionKey,
                    #     'AcceptCookie': 'yes',
                    # }
                    n1 = random.randint(0, 9)
                    n2 = random.randint(0, 9)
                    n3 = random.randint(0, 9)
                    n4 = random.randint(0, 9)
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryiOrmPlkwMsV42SJA',
                        'Origin': 'https://pbservice.moc.oocl.com',
                        'Pragma': 'no-cache',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53{n1}.3{n2} (KHTML, like Gecko) Chrome/10{n3}.{n4}.{n3}.0 Safari/53{n1}.3{n2}',
                        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }
                    ib2in1_estimate_date = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime(
                        '%d %b %Y, %H:%M')
                    data = '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ANONYMOUS_TOKEN"\r\n\r\n' \
                           f'{anonymous_token}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ENTRY"\r\n\r\n' \
                           'MCC\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ENTRY_TYPE"\r\n\r\n' \
                           'OOCL\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="PREFER_LANGUAGE"\r\n\r\n' \
                           'en-US\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ANONYMOUS_BEHAVIOR"\r\n\r\n' \
                           'INPAGE_FUNCTION\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:forward_uri"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="currentContainerNumber"\r\n\r\n' \
                           f'{container_no_parme}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaBookingNumber"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaContainerNumbers"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaBillOfLadingNumber"\r\n\r\n' \
                           f'{self.real_bl}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaSearchTypeCode"\r\n\r\n' \
                           'BL\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:rtContainerNumberValueID"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="det_estimate_date"\r\n\r\n' \
                           'dd mmm yyyy, hh:mm\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="dem_estimate_date"\r\n\r\n' \
                           'dd mmm yyyy, hh:mm\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="qr_estimate_date"\r\n\r\n' \
                           'dd mmm yyyy, hh:mm\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ib2in1_estimate_date"\r\n\r\n' \
                           f'{ib2in1_estimate_date}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:crossDomainSaveStateMapString"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form_SUBMIT"\r\n\r\n' \
                           '1\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:_link_hidden_"\r\n\r\n' \
                           'form:selectOneContainerToSearch\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="jsf_tree_64"\r\n\r\n' \
                           f'{jsf_tree_64}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="jsf_state_64"\r\n\r\n' \
                           f'{jsf_state_64}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="jsf_viewid"\r\n\r\n' \
                           '/cargotracking/ct_result_bl.jsp\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA--\r\n'
                    url1 = f'https://pbservice.moc.oocl.com/party/cargotracking/ct_result_bl.jsf?&ANONYMOUS_TOKEN={anonymous_token}&ENTRY=MCC&ENTRY_TYPE=OOCL&PREFER_LANGUAGE=en-US&researchToken={token}'
                    response = self.session.post(url1, data=data, headers=headers, timeout=self.timeOut)
                    self.spider_Data(url1, response)  # 新增字段
                    if response.status_code == 200:

                        event_tr = etree.HTML(response.text)

                        event_tr_list = event_tr.xpath('//*[@id="Tab2"]//table[@id="eventListTable"]/tr')
                        if not event_tr_list:
                            continue

                        break
                    time.sleep(1)
                except Exception as e:
                    time.sleep(1)
                    if _ == 9:
                        break
            # print(994, response)
            # 参数为需传递参数
            datas = self.parse_container_event(response, container_info, bill_item)
            con_list.append(datas)
        result = {"status": "success", "message": "success", "data": con_list, "spiderData": self.spiderData}
        return json.dumps(result)

    def booking_search(self, response):
        meta_s = self.message.get_business_data()
        meta = self.message.get_business_data()
        bill_item = bill_info_item()
        bill_item['bl_no'] = meta_s.get('blNo')
        bill_item['carrier_id'] = meta_s.get('carrierId')
        bill_item['carrier_code'] = meta_s.get('carrierCode')
        bill_item['task_id'] = meta_s.get('taskId')
        # bill_item['request_url'] = response.url
        html = etree.HTML(response.text)
        bill_item['depart'] = self.extract_first(html.xpath('//*[@id="form:PORLocation0"]/text()'))
        bill_item['load'] = self.extract_first(html.xpath('//*[@id="form:POLLocation0"]/text()'))
        pot_datas = html.xpath('//div[@id="Tab1"]//table[@id="eventListTable"]//tr')[1:]
        pot_count = len(pot_datas)

        if pot_count > 1:
            discharge = ''
            arrive = ''
            for index, pot_data in enumerate(pot_datas):
                index += 1
                if index == 1:
                    location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[4]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            atd = format_date(date)
                            etd = ''
                        else:
                            etd = format_date(date)
                            atd = ''
                    else:
                        etd = ''
                        atd = ''

                    vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                    vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                        self.extract_first(pot_data.xpath('./td[5]/text()')))
                    span_tab_list = pot_data.xpath('./td[5]/span')
                    span_tab_list1 = pot_data.xpath('./td[5]/text()')
                    voyage_no = ''
                    if span_tab_list:
                        voyage = ''
                        if len(span_tab_list) == 1:
                            for span_tab in span_tab_list:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage_section if voyage_section else ''
                                voyage_no = voyage.strip()
                        else:
                            for span_tab in span_tab_list[:-1]:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage + '/' + voyage_section if voyage else voyage_section
                                voyage_no = voyage.strip()
                    elif span_tab_list1:
                        voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                        voyage_no = voyage.strip() if voyage else ""

                    pol_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Departure_POL",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(pol_data)
                    location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[6]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            pot_atd = format_date(date)
                            pot_etd = ''
                        else:
                            pot_atd = ''
                            pot_etd = format_date(date)
                    else:
                        pot_etd = ''
                        pot_atd = ''

                    potl_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Berth_Transit",
                        "a_time": pot_atd,
                        "e_time": pot_etd,
                    }

                    self.pol_pot_pod_list.append(potl_data)

                elif index == pot_count:

                    location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[4]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            pot_atd = format_date(date)
                            pot_etd = ''
                        else:
                            pot_atd = ''
                            pot_etd = format_date(date)
                    else:
                        pot_etd = ''
                        pot_atd = ''
                    vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                    vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                        self.extract_first(pot_data.xpath('./td[5]/text()')))
                    span_tab_list = pot_data.xpath('./td[5]/span')
                    span_tab_list1 = pot_data.xpath('./td[5]/text()')
                    voyage_no = ''
                    if span_tab_list:
                        voyage = ''
                        if len(span_tab_list) == 1:
                            for span_tab in span_tab_list:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage_section if voyage_section else ''
                                voyage_no = voyage.strip()
                        else:
                            for span_tab in span_tab_list[:-1]:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage + '/' + voyage_section if voyage else voyage_section
                                voyage_no = voyage.strip()
                    elif span_tab_list1:
                        voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                        voyage_no = voyage.strip() if voyage else ""

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Departure_Transit",
                        "a_time": pot_atd,
                        "e_time": pot_etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)
                    location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    discharge = location_name
                    arrive = pot_data.xpath('./td[8]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[7]/span[1]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[7]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            atd = format_date(date)
                            etd = ''
                        else:
                            etd = format_date(date)
                            atd = ''
                    else:
                        etd = ''
                        atd = ''

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Berth_POD",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)

                else:

                    location_name = pot_data.xpath('./td[4]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[4]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            pot_atd = format_date(date)
                            pot_etd = ''
                        else:
                            pot_atd = ''
                            pot_etd = format_date(date)
                    else:
                        pot_etd = ''
                        pot_atd = ''
                    vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                    vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                        self.extract_first(pot_data.xpath('./td[5]/text()')))
                    span_tab_list = pot_data.xpath('./td[5]/span')
                    span_tab_list1 = pot_data.xpath('./td[5]/text()')
                    voyage_no = ''
                    if span_tab_list:
                        voyage = ''
                        if len(span_tab_list) == 1:
                            for span_tab in span_tab_list:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage_section if voyage_section else ''
                                voyage_no = voyage.strip()
                        else:
                            for span_tab in span_tab_list[:-1]:  # 航次拼接
                                voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                                voyage = voyage + '/' + voyage_section if voyage else voyage_section
                                voyage_no = voyage.strip()
                    elif span_tab_list1:
                        voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                        voyage_no = voyage.strip() if voyage else ""

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Departure_Transit",
                        "a_time": pot_atd,
                        "e_time": pot_etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)
                    location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                    date = pot_data.xpath('./td[6]/span[2]/text()')
                    if date:
                        date = date[0]
                        date_content = ''.join(pot_data.xpath('./td[6]//text()'))
                        date_time = date.split(', ')
                        form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                        date = date_time[0].replace(' ', '-') + ' ' + form_date
                        if '(Actual)' in date_content:
                            atd = format_date(date)
                            etd = ''
                        else:
                            etd = format_date(date)
                            atd = ''
                    else:
                        etd = ''
                        atd = ''

                    potd_data = {
                        "vessel_name": vessel,
                        "voyage": voyage_no,
                        "location_name": location_name,
                        "event_name": "Berth_Transit",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(potd_data)

            bill_item['discharge'] = discharge
            bill_item['arrive'] = arrive

        elif pot_count == 1:
            discharge = ''
            arrive = ''
            for pot_data in pot_datas:

                location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                discharge = location_name
                arrive = clean_str(self.extract_first(pot_data.xpath('./td[8]/span[1]/text()')))
                date = clean_str(self.extract_first(pot_data.xpath('./td[4]/span[2]/text()')))
                date_content = ''.join(pot_data.xpath('./td[4]//text()'))
                vessel_name = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()')))
                vessel = clean_str(vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                    self.extract_first(pot_data.xpath('./td[5]/text()')))
                span_tab_list = pot_data.xpath('./td[5]/span')

                voyage_no = ''
                if span_tab_list:
                    voyage = ''
                    if len(span_tab_list) == 1:
                        for span_tab in span_tab_list:  # 航次拼接
                            voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                            voyage = voyage_section if voyage_section else ''
                            voyage_no = voyage.strip()
                    else:
                        for span_tab in span_tab_list[:-1]:  # 航次拼接
                            voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                            voyage = voyage + '/' + voyage_section if voyage else voyage_section
                            voyage_no = voyage.strip()
                else:
                    voyage = clean_str(self.extract_first(pot_data.xpath('./td[5]/text()[last()]')))
                    voyage_no = voyage.strip() if voyage else ""
                date_time = date.split(', ')
                form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                date = date_time[0].replace(' ', '-') + ' ' + form_date
                if '(Actual)' in date_content:
                    atd = format_date(date)
                    etd = ''
                else:
                    etd = format_date(date)
                    atd = ''

                pol_data = {
                    "vessel_name": vessel,
                    "voyage": voyage_no,
                    "location_name": location_name,
                    "event_name": "Departure_POL",
                    "a_time": atd,
                    "e_time": etd,
                }
                self.pol_pot_pod_list.append(pol_data)
                location_name = pot_data.xpath('./td[6]/span[1]/text()')[0]
                date = pot_data.xpath('./td[7]/span[1]/text()')[0]
                date_content = ''.join(pot_data.xpath('./td[7]//text()'))
                date_time = date.split(', ')
                form_date = re.findall('(\d+:\d+)', date_time[1])[0]
                date = date_time[0].replace(' ', '-') + ' ' + form_date
                if '(Actual)' in date_content:
                    pot_atd = format_date(date)
                    pot_etd = ''
                else:
                    pot_etd = format_date(date)
                    pot_atd = ''

                potl_data = {
                    "vessel_name": vessel,
                    "voyage": voyage_no,
                    "location_name": location_name,
                    "event_name": "Berth_POD",
                    "a_time": pot_atd,
                    "e_time": pot_etd,
                }

                self.pol_pot_pod_list.append(potl_data)
            bill_item['discharge'] = discharge
            bill_item['arrive'] = arrive
        vessel_voyage = None
        vessel_voyage_xpath = '//*[@id="contentTable"]//table[@class="sectionTable"]//td[contains(text(),"Vessel Voyage")]/following::td[1]/text()'
        if html.xpath(vessel_voyage_xpath):
            vessel_voyage = clean_str(self.extract_first(html.xpath(vessel_voyage_xpath))) if html.xpath(
                vessel_voyage_xpath) else ''
        if vessel_voyage:
            if re.findall(r'[\s\S]+(?=\s)', vessel_voyage, re.S):
                bill_item['vessel_name'] = re.findall(r'[\s\S]+(?=\s)', vessel_voyage, re.S)[0]
            if re.findall(r'[^\s]+$', vessel_voyage, re.S):
                bill_item['voyage'] = re.findall(r'[^\s]+$', vessel_voyage, re.S)[0]
        else:
            bill_item['vessel_name'] = ''
            bill_item['voyage'] = ''
        # 订舱号
        booking_no = self.extract_first(html.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[text()="Booking Number:"]/following::td[1]/text()'))
        bill_item['booking_no'] = re.findall(r'([\d]+)', booking_no)[0] if booking_no else ""
        # 1 x 20' General Purpose Container
        container_count = self.extract_first(html.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[text()="Total Containers:"]/following::td[1]/text()'))
        if container_count:
            container_count = container_count.split('x')[0].strip()
            bill_item['container_count'] = int(container_count)
        # 293 Carton
        manifest_quantity = self.extract_first(html.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[text()="Total Quantity:"]/following::span[1]/text()'))
        bill_item['manifest_quantity'] = re.findall(r'[\d]+', manifest_quantity)[0] if manifest_quantity else ""
        # Inbound Customs Clearance Status:
        iccs = self.extract_first(html.xpath(
            '//td[@valign="top" and @class="sectionTable"]/table[1]//table[@cellspacing="2"]//td[contains(text(),"Inbound Customs Clearance Status:")]/following::td[1]/text()'))
        bill_item['inbound_customs_clearance_status'] = iccs.strip() if iccs else ""
        container_info_tr_list = html.xpath('//*[@id="summaryTable"]/tr')
        appKey = self.extract_first(html.xpath('//*[@id="cs_captcha"]/@app-key'))
        jsf_tree_64 = self.extract_first(html.xpath('//*[@id="jsf_tree_64"]/@value'))
        jsf_state_64 = self.extract_first(html.xpath('//*[@id="jsf_state_64"]/@value'))
        jsf_view_id = self.extract_first(html.xpath('//*[@id="jsf_viewid"]/@value'))
        anonymous_token = self.extract_first(html.xpath('//*[@id="ANONYMOUS_TOKEN"]/@value'))
        anonymous_behavior = self.extract_first(html.xpath('//*[@id="ANONYMOUS_BEHAVIOR"]/@value'))
        data_list = []
        for index, tr in enumerate(container_info_tr_list[2:]):
            container_info = container_info_item()
            container_info['bl_no'] = meta.get('blNo')
            container_info['event_list'] = list()
            container_no = self.extract_first(tr.xpath('./td/a/text()'))
            if container_no and '-' in container_no:
                container_no_parme = container_no.split('-')[0]
                container_info['container_no'] = ''.join(container_no.split('-'))
            else:
                container_no_parme = container_no
                container_info['container_no'] = container_no
            bill_item['container_list'].append(container_info['container_no'])
            container_size_type = self.extract_first(tr.xpath('./td[2]/span/text()')) if tr.xpath(
                './td[2]/span/text()') else ''
            if container_size_type:
                container_size = re.findall(r'([\d]+)', container_size_type)[0]
                container_type = container_size_type.replace(container_size, '').strip()
                container_info['container_size'] = container_size
                container_info['container_type'] = container_type
            else:
                container_info['container_size'] = ''
                container_info['container_type'] = ''
            quantity = self.extract_first(tr.xpath('./td[3]/span/text()')) if tr.xpath(
                './td[3]/span/text()') else ''
            container_info['quantity'] = re.findall(r'([\d]+)', quantity)[0] if quantity else ""
            container_weight = self.extract_first(tr.xpath('./td[4]/span/text()'))
            container_info['container_weight'] = container_weight if container_weight else ""
            # VGM
            # vgm = tr.xpath('./td[5]/text()')[0]
            # current status
            latest_event_name = self.extract_first(tr.xpath('./td[6]/text()'))
            container_info['latest_event_name'] = latest_event_name.strip() if latest_event_name else ''
            latest_location = self.extract_first(tr.xpath('./td[7]/span/text()'))
            container_info['latest_location'] = latest_location.strip() if latest_location else ''
            # 05 Oct 2019, 06:49 ZAT
            event_time = self.extract_first(tr.xpath('./td[8]/span/text()'))
            if event_time:
                event_time = replace_time(event_time)
                container_info['latest_location_date'] = format_date(event_time)
            # eta  | 22 Sep 2019, 08:00  Local
            eta = tr.xpath('td[9]//tr[2]/td/span/text()')[0]
            if eta:
                modify_eta = replace_time(eta.strip())
                container_info['eta'] = format_date(modify_eta.strip())
            # pod
            container_info['pod'] = self.extract_first(tr.xpath('td[9]//tr[1]/td/span/text()'))
            # container_no = container_info.get('container_no', '')
            # form_link = 'form:link' + str(index)
            for _ in range(10):
                try:
                    token, sessionKey = self.get_container(appKey)
                    if not token:
                        continue
                    cookies = {
                        'cscaptachaCookie': sessionKey,
                        'AcceptCookie': 'yes',
                    }
                    n1 = random.randint(0, 9)
                    n2 = random.randint(0, 9)
                    n3 = random.randint(0, 9)
                    n4 = random.randint(0, 9)
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'no-cache',
                        'Connection': 'keep-alive',
                        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryiOrmPlkwMsV42SJA',
                        'Origin': 'https://pbservice.moc.oocl.com',
                        'Pragma': 'no-cache',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/53{n1}.3{n2} (KHTML, like Gecko) Chrome/10{n3}.{n4}.{n3}.0 Safari/53{n1}.3{n2}',
                        'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }
                    ib2in1_estimate_date = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime(
                        '%d %b %Y, %H:%M')
                    data = '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ANONYMOUS_TOKEN"\r\n\r\n' \
                           f'{anonymous_token}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ENTRY"\r\n\r\n' \
                           'MCC\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ENTRY_TYPE"\r\n\r\n' \
                           'OOCL\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="PREFER_LANGUAGE"\r\n\r\n' \
                           'en-US\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ANONYMOUS_BEHAVIOR"\r\n\r\n' \
                           'INPAGE_FUNCTION\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:forward_uri"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="currentContainerNumber"\r\n\r\n' \
                           f'{container_no_parme}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaBookingNumber"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaContainerNumbers"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaBillOfLadingNumber"\r\n\r\n' \
                           f'{self.real_bl}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="searchCriteriaSearchTypeCode"\r\n\r\n' \
                           'BL\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:rtContainerNumberValueID"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="det_estimate_date"\r\n\r\n' \
                           'dd mmm yyyy, hh:mm\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="dem_estimate_date"\r\n\r\n' \
                           'dd mmm yyyy, hh:mm\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="qr_estimate_date"\r\n\r\n' \
                           'dd mmm yyyy, hh:mm\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="ib2in1_estimate_date"\r\n\r\n' \
                           f'{ib2in1_estimate_date}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:crossDomainSaveStateMapString"\r\n\r\n\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form_SUBMIT"\r\n\r\n' \
                           '1\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="form:_link_hidden_"\r\n\r\n' \
                           'form:selectOneContainerToSearch\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="jsf_tree_64"\r\n\r\n' \
                           f'{jsf_tree_64}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="jsf_state_64"\r\n\r\n' \
                           f'{jsf_state_64}\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA\r\n' \
                           'Content-Disposition: form-data; name="jsf_viewid"\r\n\r\n' \
                           '/cargotracking/ct_result_bl.jsp\r\n' \
                           '------WebKitFormBoundaryiOrmPlkwMsV42SJA--\r\n'
                    url1 = f'https://pbservice.moc.oocl.com/party/cargotracking/ct_result_bl.jsf?&ANONYMOUS_TOKEN={anonymous_token}&ENTRY=MCC&ENTRY_TYPE=OOCL&PREFER_LANGUAGE=en-US&researchToken={token}'
                    response = self.session.post(url1, data=data, cookies=cookies, headers=headers,
                                                 timeout=self.timeOut)
                    self.spider_Data(url1, response)  # 新增字段
                    if response.status_code == 200:
                        break
                    time.sleep(1)
                except Exception as e:
                    time.sleep(1)
                    if _ == 9:
                        break
            datas = self.parse_container_event(response, container_info, bill_item)
            data_list.append(datas)
        result = {"status": "success", "message": "success", "data": data_list}
        return json.dumps(result)

    def run(self):
        bl_no = self.message.get_business_data().get('blNo')
        self.real_bl = re.findall(r'([\d]+)', bl_no, re.S)[0] if re.findall(r'([\d]+)', bl_no, re.S) else ''
        if not bl_no:
            result_data = {"status": "success", "message": "fail", 'data': []}
            return json.dumps(result_data)
        else:
            ab_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                       'j',
                       'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            sessionKey = ''
            for i in range(1, 37):
                if i == 15:
                    sessionKey += '4'
                    continue
                if i == 16:
                    sessionKey += 'c'
                    continue
                if i == 9 or i == 14 or i == 19 or i == 24:
                    sessionKey += '-'
                    continue
                sessionKey += random.choice(ab_list)
            cookies = {"AcceptCookie": "yes", "cscaptachaCookie": sessionKey}
            self.session.cookies.update(cookies)
            params = {
                'ANONYMOUS_BEHAVIOR': 'BUILD_UP',
                'domainName': 'PARTY_DOMAIN',
                'ENTRY_TYPE': 'OOCL',
                'ENTRY': 'MCC',
                'ctSearchType': 'BL',
                'ctShipmentNumber': bl_no
            }
            for i in range(10):
                try:
                    url = 'https://pbservice.moc.oocl.com/party/cargotracking/ct_search_from_other_domain.jsf'
                    response = self.session.get(url=url, params=params, timeout=self.timeOut)
                    if response.status_code == 200:
                        break
                    time.sleep(1)
                except Exception as e:
                    if i == 9:
                        raise e
                    time.sleep(1)
                    continue
            html = Selector(response.text)
            # USER_TOKEN = html.xpath('//input[@id="USER_TOKEN"]/@value').extract_first()
            ACTIVE_TOKEN_PARAMETER = html.xpath('//input[@id="ACTIVE_TOKEN_PARAMETER"]/@value').extract_first()
            jsf_tree_64 = html.xpath('//input[@id="jsf_tree_64"]/@value').extract_first()
            jsf_state_64 = html.xpath('//input[@id="jsf_state_64"]/@value').extract_first()
            appKey = html.xpath('//*[@id="cs_captcha"]/@app-key').extract_first()
            token = self.get_container(appKey, sessionKey)
            post_data = {
                'hiddenForm:searchType': 'BL',
                'hiddenForm:pCTTNa': 'pCTTVa',
                'hiddenForm:billOfLadingNumber': bl_no,
                'hiddenForm:supportUtfChars': 'true',
                'hiddenForm:bookingNumber': '',
                'hiddenForm:containerNumber': '',
                'hiddenForm:referenceNumber': '',
                'hiddenForm:referenceType': '',
                'hiddenForm:isFromMobile': 'false',
                'hiddenForm:embededContent': 'false',
                'hiddenForm:selectedDomain': 'PARTY_DOMAIN',
                'hiddenForm:token': token,
                'hiddenForm:timeOutToken': '',
                'hiddenForm:nc_token': '',
                'hiddenForm:csessionid': '',
                'hiddenForm:sig': '',
                'ENTRY': 'MCC',
                'ENTRY_TYPE': 'OOCL',
                'PREFER_LANGUAGE': 'en-US',
                'OPERATOR_USER_ID': '',
                'USER_TOKEN': ACTIVE_TOKEN_PARAMETER,
                'hiddenForm_SUBMIT': '1',
                'hiddenForm:_link_hidden_': 'hiddenForm:goToCargoTrackingBL',
                'jsf_tree_64': jsf_tree_64,
                'jsf_state_64': jsf_state_64,
                'jsf_viewid': '/cargotracking/ct_search_from_other_domain.jsp',
            }
            for i in range(10):
                try:
                    url = f'https://pbservice.moc.oocl.com/party/cargotracking/ct_search_from_other_domain.jsf'
                    response = self.session.post(url=url, params=params, data=post_data, timeout=self.timeOut)
                    self.spider_Data(url, response)  # 新增字段
                    if response.status_code == 200:
                        break
                    time.sleep(1)
                    if 'please provide below incident and event ID' in response.text or 'Looks like access too frequently' in response.text or 'Connection from current IP address is blocked' in response.text:
                        # token = self.get_token()
                        # token = self.get_track_token()
                        post_data['hiddenForm:token'] = ''
                        continue
                    break
                except Exception as e:
                    time.sleep(1)
                    if i == 9:
                        raise e
                    continue
            if "API integration benefits your business, please contact our helpdesk at helpdesk@cargosmart.com for assistance." == response.text:
                return {"status": "success", "message": "fail", "data": [], "spiderData": self.spiderData}

            # logger.info(json.dumps('run_server', ensure_ascii=False))
            if 'No records were found.' in response.text:
                token = ''
                post_data = {
                    'hiddenForm:searchType': 'BC',
                    'hiddenForm:pCTTNa': 'pCTTVa',
                    'hiddenForm:billOfLadingNumber': "",
                    'hiddenForm:supportUtfChars': 'true',
                    'hiddenForm:bookingNumber': self.real_bl,
                    'hiddenForm:containerNumber': '',
                    'hiddenForm:referenceNumber': '',
                    'hiddenForm:referenceType': '',
                    'hiddenForm:isFromMobile': 'false',
                    'hiddenForm:embededContent': 'false',
                    'hiddenForm:selectedDomain': 'PARTY_DOMAIN',
                    'hiddenForm:token': '',
                    'hiddenForm:timeOutToken': '',
                    'hiddenForm:nc_token': '',
                    'hiddenForm:csessionid': '',
                    'hiddenForm:sig': '',
                    # 'USER_TOKEN': USER_TOKEN,
                    'ENTRY': 'MCC',
                    'ENTRY_TYPE': 'OOCL',
                    'PREFER_LANGUAGE': 'en-US',
                    'OPERATOR_USER_ID': '',
                    'USER_TOKEN': ACTIVE_TOKEN_PARAMETER,
                    'hiddenForm_SUBMIT': '1',
                    'hiddenForm:_link_hidden_': "hiddenForm:goToCargoTrackingBC",
                    'jsf_tree_64': jsf_tree_64,
                    'jsf_state_64': jsf_state_64,
                    'jsf_viewid': '/cargotracking/ct_search_from_other_domain.jsp',
                }
                for _ in range(10):
                    try:
                        url = 'https://pbservice.moc.oocl.com/party/cargotracking/ct_search_from_other_domain.jsf'
                        bk_response = self.session.post(url=url, params=params, data=post_data, timeout=self.timeOut)
                        self.spider_Data(url, bk_response)  # 新增字段
                        if bk_response.status_code == 200:
                            break
                        time.sleep(1)
                    except Exception as e:
                        time.sleep(1)
                        if _ == 9:
                            break
                if "No records were found." in bk_response.text:
                    return {"status": "success", "message": "fail", "data": [], "spiderData": self.spiderData}
                else:
                    result_data = self.booking_search(bk_response)
                    if not result_data:
                        pass
                        # self.session.cookies.clear()
                    return result_data
            else:
                result_data = self.blno_search(response, token, sessionKey)
                if not result_data:
                    return {"status": "success", "message": "fail", "data": [], "spiderData": self.spiderData}
                return result_data

    def run_server(self):
        result_data = self.run()
        if result_data:
            if self.pol_pot_pod_list:
                voyage_list = []

                lens = len(self.pol_pot_pod_list)

                for index, data in enumerate(self.pol_pot_pod_list):
                    index += 1

                    if index == 1:
                        voyage_data = {
                            "vessel_name": data.get('vessel_name'),
                            "voyage": data.get('voyage'),
                            "pol": data.get('location_name'),
                            "pol_etd": data.get('e_time'),
                            "pol_atd": data.get('a_time'),
                            "pol_eta": "",
                            "pol_ata": "",
                            "pod_eta": "",
                            "pod_ata": "",
                            "pol_dock_name": "",
                            "pod_dock_name": "",
                            "transport_mode": "",
                            "pod": ""
                        }


                    elif index == lens:

                        voyage_data['pod_ata'] = data.get('a_time')
                        voyage_data['pod_eta'] = data.get('e_time')
                        voyage_data['pod'] = data.get('location_name')
                        voyage_list.append(voyage_data)
                    else:

                        voyage_data['pod_ata'] = data.get('a_time')
                        voyage_data['pod_eta'] = data.get('e_time')
                        voyage_data['pod'] = data.get('location_name')
                        voyage_list.append(voyage_data)

                        voyage_data = {
                            "vessel_name": data.get('vessel_name'),
                            "voyage": data.get('voyage'),
                            "pol": data.get('location_name'),
                            "pol_etd": data.get('e_time'),
                            "pol_atd": data.get('a_time'),
                            "pol_eta": "",
                            "pol_ata": "",
                            "pol_dock_name": "",
                            "pod_dock_name": "",
                            "transport_mode": "",
                            "pod": ""
                        }

                if len(self.pol_pot_pod_list) == 4:
                    del voyage_list[1]
                for index, i in enumerate(voyage_list):
                    index += 1
                    i['sort'] = index

                old_result_data = json.loads(result_data)
                data_list = old_result_data.get('data')
                for data in data_list:
                    data['data']['billInfo']['voyage_list'] = voyage_list
                result_data = json.dumps(
                    {"status": "success", "message": "success", "data": data_list, "spiderData": self.spiderData})

        return result_data

    def parse_container_event(self, response, container_info, bill_item):
        if 'The website you intend to access is treated as hacking and therefore being blocked by the company' in response.text:
            exp_traceback = 'The website you intend to access is treated as hacking and therefore being blocked by the compan'
            exp_str = 'OOCLTracking def parse_container_event ' + exp_traceback
            raise ValueError(exp_str)
        try:
            response = etree.HTML(response.text)
            bl_vessel_voyage_info = response.xpath('//*[@id="Tab1"]//table[@id="eventListTable"]//tr')
            vessel_voyage_list = list()
            for i in bl_vessel_voyage_info[1:]:
                bill_item['discharge'] = clean_str(self.extract_first(i.xpath('./td[6]/span[1]/text()')))
                bill_item['arrive'] = clean_str(self.extract_first(i.xpath('./td[6]/span[1]/text()')))
                ves_voy_item = dict()
                ves_voy_item["port_of_load"] = clean_str(self.extract_first(i.xpath('./td[4]/span[1]/text()')))
                vessel_name = clean_str(self.extract_first(i.xpath('./td[5]/text()')))
                ves_voy_item["vessel_name"] = clean_str(
                    vessel_name.split('  ')[1]) if "  " in vessel_name else clean_str(
                    self.extract_first(i.xpath('./td[5]/text()')))
                span_tab_list = i.xpath('./td[5]/span')
                span_tab_list1 = i.xpath('./td[5]/text()')
                if span_tab_list:
                    voyage = ''
                    if len(span_tab_list) == 1:
                        for span_tab in span_tab_list:  # 航次拼接
                            voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                            voyage = voyage_section if voyage_section else ''
                            ves_voy_item["voyage_no"] = voyage.strip()
                    else:
                        for span_tab in span_tab_list[:-1]:  # 航次拼接
                            voyage_section = clean_str(self.extract_first(span_tab.xpath('./text()')))
                            voyage = voyage + '/' + voyage_section if voyage else voyage_section
                            ves_voy_item["voyage_no"] = voyage.strip()
                elif span_tab_list1:
                    voyage = clean_str(self.extract_first(i.xpath('./td[5]/text()[last()]')))
                    ves_voy_item["voyage_no"] = voyage.strip() if voyage else ""
                ves_voy_item["port_of_discharge"] = clean_str(self.extract_first(i.xpath('./td[6]/span[1]/text()')))
                vessel_voyage_list.append(ves_voy_item)
            # print(vessel_voyage_list)
            event_info_tr_list = response.xpath('//*[@id="Tab2"]//table[@id="eventListTable"]/tr')
            for event_tr in event_info_tr_list[1:]:
                event = tracking_event_item()
                event_name = clean_str(self.extract_first(event_tr.xpath('./td/text()')))
                event['event_name'] = event_name
                location_name = clean_str(self.extract_first(event_tr.xpath('./td[3]/span/text()')))
                if location_name and len(location_name.split(",")) > 1:
                    location_name = ",".join(location_name.split(",")[1:])
                event['location_name'] = location_name.strip()
                transport_mode = clean_str(self.extract_first(event_tr.xpath('./td[4]/text()'))) if event_tr.xpath(
                    './td[4]/text()') else ''
                event['transport_mode'] = transport_mode
                event_time_str = replace_time(self.extract_first(event_tr.xpath('./td[5]/span/text()')))
                event_time = format_date(event_time_str)
                time_stamp = transfor_standard_datetime_to_timestamp(event_time)
                if time_stamp:
                    event['e_time'] = time_stamp[1]
                    event['a_time'] = time_stamp[0]
                # print(json.dumps(vessel_voyage_list))
                # time.sleep(100)
                for i in vessel_voyage_list:
                    port_of_load = i.get('port_of_load').strip().replace(' ', '').upper()
                    port_of_load = port_of_load.strip().replace(' ', '').upper() if port_of_load else ''
                    port_of_discharge = i.get('port_of_discharge').strip().replace(' ', '').upper()
                    if (re.findall(fr'{port_of_load}', location_name.strip().replace(' ', '').upper(), re.S)
                        and re.findall(r'Loaded', event_name, re.S) or
                        re.findall(fr'{port_of_discharge}', location_name.strip().replace(' ', '').upper(), re.S)
                        and re.findall(r'Discharged', event_name, re.S)) and transport_mode == 'Vessel' or (
                            re.findall(fr'{port_of_discharge.split(",")[1]}',
                                       location_name.strip().replace(' ', '').upper(), re.S)
                            and re.findall(r'Discharged', event_name, re.S)) and (
                            transport_mode == 'Vessel' or transport_mode == ''):
                        event['vessel_name'] = i.get('vessel_name').strip() if i.get('vessel_name') else ''
                        event['voyage'] = i.get('voyage_no').strip() if i.get('voyage_no') else ''
                    elif (re.findall(fr'{port_of_load.split(",")[0]}', location_name.strip().replace(' ', '').upper(),
                                     re.S) and re.findall(r'Vessel Departed', event_name, re.S)) or (
                            re.findall(fr'{port_of_discharge.split(",")[0]}',
                                       location_name.strip().replace(' ', '').upper(), re.S) and re.findall(
                            r'Vessel Arrived', event_name, re.S)):
                        event['vessel_name'] = i.get('vessel_name').strip() if i.get('vessel_name') else ''
                        event['voyage'] = i.get('voyage_no').strip() if i.get('voyage_no') else ''
                        event['transport_mode'] = 'Vessel'
                    container_info['event_list'].append(event)
            event_list = []
            for item in container_info['event_list']:
                if item in event_list:
                    continue
                event_list.append(item)
            container_info['event_list'] = event_list
            container_info['event_list'].reverse()
            if self.pol_pot_pod_list:
                for pot in self.pol_pot_pod_list:
                    container_info['event_list'].append(
                        pot
                    )
            return {
                'data': return_tracking_info(receive_task_message=self.message.get_business_data(), bill_item=bill_item,
                                             container_info=container_info)}
        except Exception as err:
            return {'data': {}}


class ErrorException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


if __name__ == '__main__':
    # while True:
    class Message(object):
        def __init__(self, message):
            self.busi_data = message

        def get_business_data(self):
            return self.busi_data

        def get_common_data_task_id(self):
            return '测试ID'

        def get_proxies(self):
            return {"agentDomain": "tunnel5.qg.net:17051", "agentAccount": "75BA4B57",
                    "agentToken": "2A948D1DA56D", "agentId": 19}

            # return {"agentDomain": "http-proxy-t1.dobel.cn:9180", "agentAccount": "QRKJDUOBEIEF7HT2MK5",
            #         "agentToken": "K2P9aQEc", "agentId": 19}

            # return {"agentDomain": "http2-pro.abuyun.com:9010", "agentAccount": "H36419H50ABX64ZP",
            #         "agentToken": "6A7DCAE0B909E4AC", "agentId": 19}

        def to_dict(self):
            return {}


    # OOLU2121886480
    # OOLU4117860120
    # OOLU2705391650
    # OOLU2699080450
    message = {"blNo": "OOLU2716050370", "carrierCode": "OOCL", "realTime": 0, "taskId": 8614686,
               "traceId": "ebca0765d3f24014af06cd1936af7207.21920.16665833437582879", "type": "bl"}
    time1 = time.time()
    message = Message(message)
    spider = OOCLPareseTracking(message)
    data = spider.run_server()
    print(data)