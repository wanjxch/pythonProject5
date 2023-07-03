# -*- coding: utf-8 -*-
# @software: PyCharm
# @time: 2022/1/17 10:13
import json
import time
import re
from copy import deepcopy
import requests
import urllib3

urllib3.disable_warnings()


def format_date(data):
    if data:
        strp_time = time.strptime(data, "%Y-%m-%d %H:%M")
        strf_time = time.strftime("%Y-%m-%d %H:%M:%S", strp_time)
        return strf_time


def clean_str(original_str):
    if original_str:
        cleaned_str = original_str
        cleaned_str = cleaned_str.replace('\r', '')
        cleaned_str = cleaned_str.replace('\t', '')
        cleaned_str = cleaned_str.replace('\n', '')
        cleaned_str = cleaned_str.strip()
        return cleaned_str


def date_to_format_data(orign_datetime_string):
    """ 2018-11-03 22:24 转化为 2018-11-03 22:24:00 """
    if orign_datetime_string:
        datetime_string = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', orign_datetime_string)
        struct_time = time.strptime(datetime_string[0], '%Y-%m-%d %H:%M')
        datetime_string = time.strftime('%Y-%m-%d %H:%M:%S', struct_time)
        return datetime_string  #


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


# 事件时间排序
def quick_sort(seq):
    try:
        if seq[0].get('a_time') or seq[0].get('e_time'):
            pivot = seq[0].get('a_time')
            if pivot == '':
                pivot = seq[0].get('e_time')
                lesser = quick_sort([x for x in seq[1:] if x.get('e_time') < pivot])
                greater = quick_sort([x for x in seq[1:] if x.get('e_time') >= pivot])
            else:
                lesser = quick_sort([x for x in seq[1:] if x.get('a_time') < pivot])
                greater = quick_sort([x for x in seq[1:] if x.get('a_time') >= pivot])
            return lesser + [seq[0]] + greater
    except Exception:
        return []


def bill_info_item():  # 账单信息
    bill_item = {}
    bill_item["bill_no"] = ""  # 必填字段            #
    bill_item["bl_no"] = ""
    bill_item["depart"] = ""  # 出发地
    bill_item["arrive"] = ""  # 目的地
    bill_item["load"] = ""  # 出发地城市
    bill_item["discharge"] = ""  # 目的地城市
    bill_item["carrier_id"] = ""  #
    bill_item["carrier_code"] = ""  #
    bill_item["vessel_name"] = ""  # 船名
    bill_item["voyage"] = ""  # 航次
    bill_item["request_url"] = ""
    bill_item["task_id"] = ""  #
    bill_item["booking_no"] = ""  # 订舱号/提单号
    bill_item["bl_type"] = ""  # "Original"
    bill_item["bl_surrendered_status"] = ""  #
    bill_item["bl_status"] = ""  #
    bill_item["inbound_customs_clearance_status"] = ""  # 入境海关许可状态
    bill_item["inbound_customs_clearance_date"] = ""  # 入境海关许可时间
    bill_item["container_count"] = ""  # 必填字段   # 集装箱的数量
    bill_item["service_mode"] = ""  # 服务模式
    bill_item["service_requirement"] = ""  # 服务要求
    bill_item["vgm_cut_off_date"] = ""  # vgm截止日期
    bill_item["vgm_received"] = ""  # vgm收到
    bill_item["port_cut_off_date"] = ""  # Cargo Cutoff
    bill_item["gross_weight"] = ""  # 总重量
    bill_item["measurement"] = ""  # 长度
    bill_item["eta_at_place_of_delivery"] = ""  # 预计到达提货地时间
    bill_item["manifest_quantity"] = ""  # 货单数量
    bill_item["on_board_date"] = ""  # 上船时间
    bill_item["gis_depart_port_id"] = ""  # 离开id
    bill_item["gis_depart_port_code"] = ""
    bill_item["gis_arrive_port_id"] = ""  # 到达id
    bill_item["gis_arrive_port_code"] = ""
    bill_item["container_list"] = []  # 集装箱号list
    return bill_item


def container_info_item():  # 货物信息
    contaienr_item = {}
    contaienr_item["container_no"] = ""  # 集装箱号
    contaienr_item["seal_no"] = ""
    contaienr_item["bl_no"] = ""  #
    contaienr_item["container_size"] = ""  # 40
    contaienr_item["container_type"] = ""  # HQ
    contaienr_item["event_list"] = []  # 动态
    contaienr_item["container_weight"] = ""
    contaienr_item["cargo_weight"] = ""  # 货物宽
    contaienr_item["real_cargo_weight"] = ""  # 实际货物宽
    contaienr_item["service_type"] = ""  # 服务类型
    contaienr_item["eta"] = ""  # 预计到达提货地时间
    contaienr_item["ata"] = ""
    contaienr_item["pod"] = ""
    contaienr_item["latest_location_date"] = ""  # 最新位置时间
    contaienr_item["latest_event_name"] = ""  # 最新动态名称
    contaienr_item["latest_location"] = ""  # 最新位置
    contaienr_item["remaining_days"] = ""  # 剩余天数
    contaienr_item["laden_return"] = ""  # 满载时间
    contaienr_item["cargo_pickup"] = ""
    contaienr_item["empty_pick_up_date"] = ""
    contaienr_item["empty_return_date"] = ""
    contaienr_item["quantity"] = ""
    return contaienr_item


def tracking_event_item():  # 跟踪事件信息
    event_item = {}
    event_item["vessel_name"] = ""
    event_item["voyage"] = ""
    event_item["transport_mode"] = ""  # 运输方式
    event_item["event_name"] = ""
    event_item["a_time"] = ""
    event_item["e_time"] = ""
    event_item["location_name"] = ""
    event_item["location_type"] = ""
    # dock_name:码头
    return event_item


def return_tracking_info(receive_task_message: dict = None, bill_item: dict = None, container_info: dict = None):
    """
    返回的提单基本信息数据结构报文
    :param receive_task_message: 接受的任务消息报文
    :param bill_item: 爬取的提单信息报文
    :param container_info: 爬取的集装箱信息报文
    :return:
    """
    return_data = {"receiveTaskMessage": receive_task_message, "billInfo": bill_item, "containerInfo": container_info}
    return return_data


class COSCOParseTracking(object):

    def __init__(self, message):
        # 初始化参数
        self.message = message
        self.origin_task_message = deepcopy(self.message.get_business_data())
        self.busi_data = self.message.get_business_data()
        self.taskId = self.message.get_common_data_task_id()
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
        self.bl_no = self.busi_data.get('blNo')
        self.blno = re.findall(r'\d+', self.bl_no)[0]
        self.timeOut = 20
        self.spiderData = {}  # 存放接口爬取原始数据
        self.data = []  # 最后的存放位置
        self.tracking_info = {}  # 存放bill_info
        self.containerInfo_info = {}  # 存放contaienr_item
        self.exception = None  # 最后一次错误
        self.bill_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'elines.coscoshipping.com',
            'language': 'zh_CN',
            'Pragma': 'no-cache',
            'sys': 'eb',
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/74.0.3729.169 Safari/537.36"
        }
        self.bill_url = 'https://elines.coscoshipping.com/ebtracking/public/bill/{0}?timestamp={1}'
        self.booking_url = 'https://elines.coscoshipping.com/ebtracking/public/booking/{0}?timestamp={1}'
        self.bill_containers = 'https://elines.coscoshipping.com/ebtracking/public/bill/containers/{0}?timestamp={1}'
        self.bookingNumber_url = 'https://elines.coscoshipping.com/ebtracking/public/container/status/{0}?bookingNumber={1}&timestamp={2}'

    def spider_Data(self, url, response):
        try:
            self.spiderData[url] = response.text
        except Exception as e:
            pass

    def parse(self):
        bill_url = self.bill_url.format(self.blno, int(time.time() * 1000))
        for i in range(3):
            try:
                response = requests.get(url=bill_url, headers=self.bill_headers, proxies=self.proxies,
                                        timeout=self.timeOut, verify=False)
                self.spider_Data(bill_url, response)  # 新增字段
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

    def parse_bill_response(self, response):
        bill_text = response.text
        if '无数据' in bill_text:
            booking_url = self.booking_url.format(self.blno, int(time.time() * 1000))
            for i in range(3):
                try:
                    response = requests.get(url=booking_url, headers=self.bill_headers, proxies=self.proxies,
                                            timeout=self.timeOut, verify=False)
                    self.spider_Data(booking_url, response)  # 新增字段
                    response.json()
                except Exception as e:
                    self.exception = e
                    time.sleep(1)
                    continue
                bill_text = response.text
        b_info_dict = json.loads(bill_text)['data']['content']
        bill_info = bill_info_item()
        bill_info['bl_no'] = self.bl_no
        bill_info['carrier_id'] = self.busi_data.get('carrierId')
        bill_info['carrier_code'] = self.busi_data.get('carrierCode')
        bill_info['task_id'] = self.busi_data.get('taskId')
        # 详细信息
        trackingPath = b_info_dict.get('trackingPath')
        cargoCutOff = b_info_dict.get('cargoCutOff')  #
        cargoTrackingContainer = b_info_dict.get('cargoTrackingContainer')  # 集装箱最新动态
        actualShipment = b_info_dict.get('actualShipment')  # 实时船期

        bill_info['depart'] = trackingPath.get('fromCity')
        bill_info['arrive'] = trackingPath.get('toCity')
        bill_info['eta_at_place_of_delivery'] = date_to_format_data(trackingPath.get('cgoAvailTm'))
        bill_info['port_cut_off_date'] = date_to_format_data(cargoCutOff)
        bill_info['load'] = trackingPath.get('fromCity').split(',')[0]
        bill_info['discharge'] = trackingPath.get('toCity').split(',')[0]
        bill_info['vessel_name'] = trackingPath.get('vslNme')
        bill_info['voyage'] = trackingPath.get('voyNumber')
        bill_info['booking_no'] = trackingPath.get('billOfladingRefCode')
        bill_info['bl_type'] = trackingPath.get('blType')
        bill_info['bl_surrendered_status'] = trackingPath.get('blRealStatus')

        bill_info['container_count'] = len(cargoTrackingContainer)
        bill_info['container_list'] = [container['cntrNum'] for container in cargoTrackingContainer]

        voyage_list = []
        for index, voyage in enumerate(actualShipment):
            index += 1
            voyage_item = {
                "vessel_name": voyage.get('vesselName'),
                "voyage": voyage.get('voyageNo'),
                "pol": voyage.get('portOfLoading'),
                "pol_etd": voyage.get('expectedDateOfDeparture', ''),
                "pol_atd": voyage.get('actualDepartureDate', ''),
                "pol_eta": "",
                "pol_ata": "",
                "pod_eta": voyage.get('estimatedDateOfArrival', ''),
                "pod_ata": voyage.get('actualArrivalDate', ''),
                "pol_dock_name": "",
                "pod_dock_name": "",
                "transport_mode": "",
                "pod": voyage.get('portOfDischarge'),
                "sort": index
            }
            voyage_list.append(voyage_item)
        bill_info['voyage_list'] = voyage_list
        self.tracking_info['billInfo'] = bill_info

        bill_containers = self.bill_containers.format(self.blno, int(time.time() * 1000))
        for i in range(3):
            try:
                response = requests.get(url=bill_containers, headers=self.bill_headers, proxies=self.proxies,
                                        timeout=self.timeOut, verify=False)
                self.spider_Data(bill_containers, response)  # 新增字段
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

    def parse_bill_containers_response(self, response, containerNumber):
        bill_containers_item = response.json()
        if bill_containers_item['code'] != "200":
            raise ValueError('response error')
        bill_containers_list = bill_containers_item['data']['content']
        for bill_containers in bill_containers_list:
            contaienr_item = container_info_item()
            contaienr_item['container_no'] = bill_containers.get('containerNumber')
            contaienr_item['seal_no'] = bill_containers.get('sealNumber')
            contaienr_item['bl_no'] = self.bl_no
            contaienr_item['container_size'] = re.findall(r'\d+', bill_containers.get('containerType'))[0]
            contaienr_item['container_type'] = re.findall(r'[a-zA-Z]+', bill_containers.get('containerType'))[0]
            contaienr_item['container_weight'] = bill_containers.get('grossWeight')
            contaienr_item['eta'] = self.tracking_info['billInfo']['eta_at_place_of_delivery']
            contaienr_item['latest_location_date'] = bill_containers.get('locationDateTime')
            contaienr_item['latest_event_name'] = bill_containers.get('label')
            contaienr_item['latest_location'] = bill_containers.get('location')
            contaienr_item['quantity'] = bill_containers.get('piecesNumber')
            self.containerInfo_info[contaienr_item['container_no']] = contaienr_item
        bookingNumber_url = self.bookingNumber_url.format(containerNumber, self.blno, int(time.time() * 1000))
        for i in range(3):
            try:
                response = requests.get(url=bookingNumber_url, headers=self.bill_headers, proxies=self.proxies,
                                        timeout=self.timeOut, verify=False)
                self.spider_Data(bookingNumber_url, response)  # 新增字段
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

    def parse_bookingNumber_response(self, response):
        event_list = []
        event_item = tracking_event_item()
        bookingNumber_event_list = response.json()['data']['content']
        for event in bookingNumber_event_list:
            event_item['transport_mode'] = event.get('transportation', '')
            event_item['event_name'] = event.get('containerNumberStatus', '')
            event_item['a_time'] = event.get('timeOfIssue', '')
            event_item['location_name'] = event.get('location', '')
            event_item['dock_name'] = event.get('location').split(',')[0]
            event_list.append(event_item)
        return event_list

    def run(self):
        response = self.parse()
        bill_response = self.parse_bill_response(response)

        for containerNumber in self.tracking_info['billInfo']['container_list']:
            bill_containers_response = self.parse_bill_containers_response(bill_response, containerNumber)
            event_list = self.parse_bookingNumber_response(bill_containers_response)
            laden_return = event_list[1]['a_time']
            empty_pick_up_date = event_list[0]['a_time']
            for containerInfo in self.containerInfo_info:
                if containerNumber == containerInfo:
                    self.containerInfo_info[containerNumber]['laden_return'] = laden_return
                    self.containerInfo_info[containerNumber]['empty_pick_up_date'] = empty_pick_up_date
                    self.containerInfo_info[containerNumber]['event_list'] = event_list

                    return_data = return_tracking_info(self.origin_task_message, self.tracking_info['billInfo'],
                                                       self.containerInfo_info[containerNumber])
                    self.data.append(return_data)
        return json.dumps({"status": 'success', "data": self.data, "spiderData": self.spiderData})

    def run_server(self):
        for i in range(5):  # 尝试5次
            try:
                result_list = self.run()
                return result_list
            except Exception as e:
                if i == 4:
                    return json.dumps({"status": "success", "data": {}, "spiderData": self.spiderData}, ensure_ascii=False)
                continue



class Message(object):
    def __init__(self, message):
        self.busi_data = message

    def get_business_data(self):
        return self.busi_data

    def get_common_data_task_id(self):
        return '测试ID'

    def get_proxies(self):
        # return {"agentDomain": "http-proxy-t1.dobel.cn:9180", "agentAccount": "SPIDERTESTJ4AJ2MNO0",
        #         "agentToken": "AKQhot1e", "agentId": 19}

        return {'agentDomain': 'http-proxy-t1.dobel.cn:9180', 'agentAccount': 'QRKJDUOBEIEFH7TM2K7',
                'agentToken': 'POFhPzAq', 'agentId': 64}

    def to_dict(self):
        return {}


if __name__ == '__main__':
    message = {"blNo": "COSU6357693840", "carrierCode": "COSCO", "carrierId": 4528, "realTime": 0, "taskId": 6742985,
               "traceId": "test", "type": "bl"}
    start = int(time.time())
    message = Message(message)
    spider = COSCOParseTracking(message)
    print(spider.run_server())
    stop = int(time.time())
    print("程序总耗时：", stop-start, "秒")
