import json
import random
import re
import time
from copy import deepcopy

import requests


# from parses.BaseParse import BaseParse
# from parses.ParseGateway import LoadOssError


def container_info_item():
    contaienr_item = dict()
    contaienr_item["bl_no"] = ""
    contaienr_item["container_no"] = ""
    contaienr_item["seal_no"] = ""
    contaienr_item["container_size"] = ""
    contaienr_item["container_type"] = ""
    contaienr_item["event_list"] = list()
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
    event_item = dict()
    event_item["vessel_name"] = ""
    event_item["voyage"] = ""
    event_item["transport_mode"] = ""
    event_item["event_name"] = ""
    event_item["a_time"] = ""
    event_item["e_time"] = ""
    event_item["location_name"] = ""
    event_item["location_type"] = ""
    return event_item


def bill_info_item():
    bill_item = dict()
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

def format_time(times):
    # 时间标准化
    if '.' in times:
        new_time = times.replace('T', ' ').split('.')[0]
    elif 'T' in times:
        new_time = times.replace('T', ' ')
    else:
        new_time = ''
    return new_time


def get_time(event_time):
    # 获取事件时间
    if event_time:
        time_array = time.strptime(event_time, "%Y-%m-%d %H:%M:%S")
        time_stamp = int(time.mktime(time_array))
        a_time = ''
        e_time = ''
        if time_stamp < int(time.time()):
            a_time = event_time
        else:
            e_time = event_time
        return a_time, e_time
    else:
        return '', ''



class FESCOParseTracking():
    def __init__(self, codes):
        self.codes = codes
        self.headers = {
            "Connection": "keep-alive",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "sec-ch-ua": "\"Chromium\";v=\"21\", \" Not;A Brand\";v=\"99\"",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "Origin": "https://tracking.fesco.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://tracking.fesco.com/clients/tracking/?codes=FBSF14064",
            "Accept-Language": "zh-CN,zh;q=0.9"
        }
        self.cookies = {
            "cookiesession1": "678A8C417B4C894A2D5E0E46F2F5EA3D"
        }
        self.tracking_url = "https://tracking.fesco.com/api/v1/tracking/get"
        self.event_list = []
        self.message = {
            'blNo': self.codes,
            "carrierCode": "COC",
            "carrierId": 4529,
            "realTime": 0,
            "taskId": 6742986,
            "traceId": "test",
            "type": "bl"
        }
        self.container_list = []

    def parse(self):
        for i in range(3):
            try:
                data = {
                    "codes": [
                        self.codes
                    ],
                    "email": None,
                    "forDate": None,
                    "fromFile": False
                }
                data = json.dumps(data, separators=(',', ':'))
                response = requests.post(self.tracking_url, headers=self.headers, cookies=self.cookies, data=data)
                response.json()
            except Exception as e:
                self.exception = e
                time.sleep(1)
                continue
            else:
                if not response:
                    continue
                return response
        raise ValueError(self.exception)


    def parse_tracking_response(self, response):
        res_item = json.loads(response.text)
        containers = res_item['containers']
        for index, container_text in enumerate(containers):
            container_dict = json.loads(container_text)
            container = container_dict.get('container')
            self.container_list.append(container)
        for index, container_text in enumerate(containers):
            container_dict = json.loads(container_text)
            bill_item = bill_info_item()
            container = container_dict.get('container')
            container_size = re.findall(r'\d+', container_dict.get('containerCTCode'))[0]
            container_type = re.findall(r'[a-zA-Z]+', container_dict.get('containerCTCode'))[0]
            carrier_code = container_dict.get('containerOwner')
            bill_item['carrier_code'] = carrier_code


            locations = container_dict.get('locations')
            if locations:
                for location in locations:
                    if location.get('type') == 'RR':
                        bill_item["depart"] = location.get('textLatin', '') + ', ' + location.get('countryLatin', '')
                        bill_item["load"] = location.get('textLatin', '')
                    if location.get('type') == 'end':
                        bill_item["arrive"] = location.get('textLatin', '') + ', ' + location.get('countryLatin','')
                        bill_item["discharge"] = location.get('textLatin', '')
            bill_item['container_list'] = self.container_list
            bill_item['container_count'] = len(self.container_list)
            bill_item['bl_no'] = self.message['blNo']
            bill_item['carrier_id'] = self.message['carrierId']
            bill_item['task_id'] = self.message['taskId']

            lastEvents = container_dict.get('lastEvents', '')
            contaienr_item = container_info_item()
            event_list = []  # 存放事件
            for lastEvent in lastEvents:
                event_item = tracking_event_item()
                event_item['event_name'] = lastEvent.get('operationName', '')
                event_item['vessel_name'] = lastEvent.get('vessel', '')
                event_item['location_type'] = lastEvent.get('transportType', '')
                event_item['location_name'] = lastEvent.get('locNameLatin', '')
                event_format_time = format_time(lastEvent.get('time'))
                a_time = get_time(event_format_time)[0]
                e_time = get_time(event_format_time)[1]
                event_item['a_time'] = a_time
                event_item['e_time'] = e_time
                event_list.append(event_item)
            contaienr_item['container_no'] = container
            contaienr_item['container_size'] = container_size
            contaienr_item['container_type'] = container_type
            contaienr_item['event_list'] = event_list
            contaienr_item['bl_no'] = self.message['blNo']
            print(json.dumps(return_tracking_info(self.message, bill_item, contaienr_item)))



if __name__ == '__main__':
    F = FESCOParseTracking("FBSF14064")
    tracking_response = F.parse()
    F.parse_tracking_response(tracking_response)