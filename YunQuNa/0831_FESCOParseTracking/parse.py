# -*- coding: utf-8 -*-
# @Time : ${DATE} ${TIME}
# @Author : housongcheng
# @Email : housongcheng@yunquna.com
# @File : ${NAME}.py
# @Software: ${PRODUCT_NAME}
# @Desc : FESCO tracking
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

    def parse(self):
        # meta = self.message.busiData
        # bl_no = meta.get('blNo')
        bl_no = "FBSF14064"

        headers = {
            'Pragma': 'no-cache',
            'Origin': 'https://tracking.fesco.com',
            'Host': 'tracking.fesco.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            # 'Referer': response.url,
            'Connection': 'keep-alive',
        }
        payload = {
            'codes': [bl_no],
            'email': None,
            'forDate': None,
            'fromFile': False
        }
        url = f'https://tracking.fesco.com/api/v1/tracking/get'
        # meta['callBack'] = 'parse_tracking_data'
        child_reqeust = requests.post(url=url, headers=headers, json=json.dumps(payload), timeout=30)
        return child_reqeust.text
        # yield {'ms_type': 'request', 'data': child_reqeust}
        # yield {'ms_type': 'data', 'data': {}, 'isReturn': 0}

    def parse_tracking_data(self, response):
        meta = self.message.busiData
        bl_no = meta.get('blNo')
        origin_task_message = deepcopy(self.message.busiData)
        meta['parentData'] = {'origin_task_message': origin_task_message}
        # 提单信息
        bill_item = bill_info_item()
        bill_item["bl_no"] = bl_no
        bill_item["carrier_id"] = meta.get('carrierId')
        bill_item["carrier_code"] = meta.get('carrierCode')

        bill_item["task_id"] = meta.get('taskId')
        try:
            result = json.loads(response.text)
        except:
            yield {'ms_type': 'data', 'data': {}, 'isReturn': 1}
            return
        containers = result.get('containers')
        if not containers:
            yield {'ms_type': 'data', 'data': {}, 'isReturn': 1}
            return

        bill_item["container_count"] = len(containers)
        containers_number_set = set()
        # 获取箱号列表
        for container_j in containers:
            container = json.loads(container_j)
            container_no = container.get('container')
            containers_number_set.add(container_no)
        bill_item["container_list"] = list(containers_number_set)
        for index_, container in enumerate(containers):
            container = json.loads(container)
            if container.get('locations'):
                locations = container.get('locations')
                if locations:
                    bill_item["depart"] = locations[0].get('textLatin', '') + ', ' + locations[0].get('countryLatin', '')
                    bill_item["load"] = locations[0].get('textLatin', '') + ', ' + locations[0].get('countryLatin', '')
                    for bl_info in locations:
                        if bl_info.get('type') == 'end':
                            bill_item["arrive"] = bl_info.get('textLatin', '') + ', ' + bl_info.get('countryLatin', '')
                            bill_item["discharge"] = bl_info.get('textLatin', '') + ', ' + bl_info.get('countryLatin', '')

            # container 箱基础信息
            container_item = container_info_item()
            container_item["bl_no"] = bl_no
            container_item["container_no"] = container.get('container')

            if container.get('container') == bl_no:
                yield {'ms_type': 'data', 'data': {}, 'isReturn': 1}
                return
            container_type_size = container.get('containerCTCode')
            if not container_type_size:
                yield {'ms_type': 'data', 'data': {}, 'isReturn': 1}
                return

            container_size = re.findall('\d+', container_type_size)[0]
            container_item["container_size"] = container_size
            container_item["container_type"] = container_type_size.replace(container_size, '')
            container_item["event_list"] = list()
            container_events = container.get('lastEvents')

            for events in container_events:
                # 箱事件信息
                event_item = tracking_event_item()
                event_item["vessel_name"] = events.get("vessel") if events.get("vessel") else ""
                event_item["voyage"] = ""
                event_item["transport_mode"] = events.get("transportType")
                event_item["event_name"] = events.get("operationNameLatin")
                event_times = events.get("time")
                event_time = format_time(event_times)
                event_item["a_time"] = get_time(event_time)[0]
                event_item["e_time"] = get_time(event_time)[1]
                event_item["location_name"] = events.get("locNameLatin")
                event_item["location_type"] = ""
                container_item["event_list"].append(event_item)
            yield {'ms_type': 'data', 'data': return_tracking_info(origin_task_message, bill_item, container_item)}


if __name__ == '__main__':
    F = FESCOParseTracking()
    print(F.parse())
