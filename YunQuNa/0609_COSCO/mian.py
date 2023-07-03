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


def bill_info_item():   # 账单信息
    bill_item = {}
    bill_item["bill_no"] = ""  # 必填字段            #
    bill_item["bl_no"] = ""
    bill_item["depart"] = ""   # 出发地
    bill_item["arrive"] = ""   # 目的地
    bill_item["load"] = ""     # 出发地城市
    bill_item["discharge"] = "" # 目的地城市
    bill_item["carrier_id"] = "" #
    bill_item["carrier_code"] = "" #
    bill_item["vessel_name"] = "" # 船名
    bill_item["voyage"] = ""     # 航次
    bill_item["request_url"] = ""
    bill_item["task_id"] = ""   #
    bill_item["booking_no"] = "" # 订舱号/提单号
    bill_item["bl_type"] = ""    # "Original"
    bill_item["bl_surrendered_status"] = "" #
    bill_item["bl_status"] = ""           #
    bill_item["inbound_customs_clearance_status"] = ""  # 入境海关许可状态
    bill_item["inbound_customs_clearance_date"] = ""    # 入境海关许可时间
    bill_item["container_count"] = ""  # 必填字段   # 集装箱的数量
    bill_item["service_mode"] = ""     # 服务模式
    bill_item["service_requirement"] = ""  # 服务要求
    bill_item["vgm_cut_off_date"] = ""   # vgm截止日期
    bill_item["vgm_received"] = ""        # vgm收到
    bill_item["port_cut_off_date"] = ""   # Cargo Cutoff
    bill_item["gross_weight"] = ""        # 总重量
    bill_item["measurement"] = ""        # 长度
    bill_item["eta_at_place_of_delivery"] = ""  # 预计到达提货地时间
    bill_item["manifest_quantity"] = ""       # 货单数量
    bill_item["on_board_date"] = ""           # 上船时间
    bill_item["gis_depart_port_id"] = ""      # 离开id
    bill_item["gis_depart_port_code"] = ""
    bill_item["gis_arrive_port_id"] = ""      # 到达id
    bill_item["gis_arrive_port_code"] = ""
    bill_item["container_list"] = []     # 集装箱号list
    return bill_item


def container_info_item():   # 货物信息
    contaienr_item = {}
    contaienr_item["container_no"] = ""   # 集装箱号
    contaienr_item["seal_no"] = ""
    contaienr_item["bl_no"] = ""         #
    contaienr_item["container_size"] = "" # 40
    contaienr_item["container_type"] = "" # HQ
    contaienr_item["event_list"] = []     # 动态
    contaienr_item["container_weight"] = ""
    contaienr_item["cargo_weight"] = ""  # 货物宽
    contaienr_item["real_cargo_weight"] = ""  # 实际货物宽
    contaienr_item["service_type"] = ""     # 服务类型
    contaienr_item["eta"] = ""            # 预计到达提货地时间
    contaienr_item["ata"] = ""
    contaienr_item["pod"] = ""
    contaienr_item["latest_location_date"] = "" # 最新位置时间
    contaienr_item["latest_event_name"] = ""   #  最新动态名称
    contaienr_item["latest_location"] = ""     # 最新位置
    contaienr_item["remaining_days"] = ""      # 剩余天数
    contaienr_item["laden_return"] = ""       # 满载时间
    contaienr_item["cargo_pickup"] = ""
    contaienr_item["empty_pick_up_date"] = ""
    contaienr_item["empty_return_date"] = ""
    contaienr_item["quantity"] = ""
    return contaienr_item


def tracking_event_item():  # 跟踪事件信息
    event_item = {}
    event_item["vessel_name"] = ""
    event_item["voyage"] = ""
    event_item["transport_mode"] = ""   # 运输方式
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
    event_type = 'COSCOParseTracking'
    # 提单号查询 URL
    GET_BL_URL = 'https://elines.coscoshipping.com/ebtracking/public/bill/{}?timestamp={}'

    GET_BL_CONTAINER_LIST_URL = 'https://elines.coscoshipping.com/ebtracking/public/bill/containers/{}?timestamp={}'
    GET_BL_CONTAINER_DETAIL_URL = 'https://elines.coscoshipping.com/ebtracking/public/container/status/{}?billNumber={}&timestamp={}'
    # 订舱号查询 URL
    GET_BK_URL = 'https://elines.coscoshipping.com/ebtracking/public/booking/{}?timestamp={}'
    GET_BK_CONTAINER_LIST_URL = 'https://elines.coscoshipping.com/ebtracking/public/booking/containers/{}?timestamp={}'
    GET_BK_CONTAINER_DETAIL_URL = 'https://elines.coscoshipping.com/ebtracking/public/container/status/{}?bookingNumber={}&timestamp={}'
    headers = {
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
        self.timeOut = 20
        self.spiderData = {}  # 存放接口爬取原始数据
        self.exception = None  # 最后一次错误
        self.pol_pot_pod_list = []

    def spider_Data(self, url, response):
        try:
            self.spiderData[url] = response.text
        except Exception as e:
            pass

    def parse(self, bl_no):
        meta = self.message.get_business_data()
        real_bl = re.findall(r'([\d]+)', bl_no, re.S)
        real_bl = real_bl[0].strip() if real_bl else bl_no
        meta['parentData'] = real_bl
        meta['originTaskMessage'] = self.origin_task_message
        request_time = int(time.time() * 1000)
        url = self.GET_BL_URL.format(real_bl, request_time)
        for i in range(3):  # 重试3次
            try:
                response = requests.get(url=url, headers=self.headers, proxies=self.proxies, verify=False, timeout=self.timeOut)
                self.spider_Data(url, response)  # 新增字段
                response.json()
            except Exception as e:
                self.exception = e
                time.sleep(1)
                continue
            else:
                if not response:
                    continue
                return response, meta
        raise ValueError(self.exception)

    def bl_get_container_list(self, response, meta):
        real_bl = meta.get('parentData')

        # 提单基本信息
        bill_item = bill_info_item()
        bill_item['bl_no'] = self.busi_data.get('blNo')
        bill_item['carrier_id'] = self.busi_data.get('carrierId')
        bill_item['carrier_code'] = self.busi_data.get('carrierCode')
        bill_item['task_id'] = self.busi_data.get('taskId')

        bl_info = response.json()       # booking

        # 请求成功，但是没有数据， 改用订舱号的url查询
        if '无数据' in response.text:
            request_time = int(time.time() * 1000)
            bk_url = self.GET_BK_URL.format(real_bl, request_time)
            meta['parentData'] = real_bl
            for _ in range(3):
                try:
                    child_request = requests.get(url=bk_url, headers=self.headers, proxies=self.proxies, verify=False, timeout=self.timeOut)
                    self.spider_Data(bk_url, child_request)  # 新增字段
                    child_request.json()
                    break
                except Exception as err:
                    if _ == 2:
                        raise err
                    time.sleep(1)
                    continue
            return 1, child_request, meta

        if not bl_info.get('data') or not bl_info.get('data').get('content'):
            return 3, {}, {}
        # 请求成功，并且有数据
        else:
            self.pol_pot_pod_list = []
            pot_datas = bl_info.get('data').get('content')['actualShipment']

            pot_count = len(pot_datas)


            if pot_count > 1:

                for index, pot_data in enumerate(pot_datas):
                    index += 1

                    if index == 1:
                        etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                        atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                        pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                        pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get(
                            'estimatedDateOfArrival') else ''

                        vesselName = pot_data.get('vesselName')
                        voyage = pot_data.get('voyageNo')
                        pol = pot_data.get('portOfLoading')
                        pod = pot_data.get('portOfDischarge')
                        pol_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pol,
                            "event_name": "Departure_POL",
                            "a_time": atd,
                            "e_time": etd,
                        }
                        self.pol_pot_pod_list.append(pol_data)

                        potl_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pod,
                            "event_name": "Berth_Transit",
                            "a_time": pot_ata,
                            "e_time": pot_eta,
                        }

                        self.pol_pot_pod_list.append(potl_data)


                    elif index == pot_count:

                        etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                        atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                        pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                        pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get(
                            'estimatedDateOfArrival') else ''

                        vesselName = pot_data.get('vesselName')

                        voyage = pot_data.get('voyageNo')

                        pol = pot_data.get('portOfLoading')
                        pod = pot_data.get('portOfDischarge')

                        pod_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pol,
                            "event_name": "Departure_Transit",
                            "a_time": atd,
                            "e_time": etd,
                        }
                        self.pol_pot_pod_list.append(pod_data)

                        potd_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pod,
                            "event_name": "Berth_POD",
                            "a_time": pot_ata,
                            "e_time": pot_eta
                        }
                        self.pol_pot_pod_list.append(potd_data)
                    else:

                        etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                        atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                        pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                        pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get(
                            'estimatedDateOfArrival') else ''

                        vesselName = pot_data.get('vesselName')
                        voyage = pot_data.get('voyageNo')
                        pol = pot_data.get('portOfLoading')
                        pod = pot_data.get('portOfDischarge')

                        pod_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pol,
                            "event_name": "Departure_Transit",
                            "a_time": atd,
                            "e_time": etd,
                        }
                        self.pol_pot_pod_list.append(pod_data)
                        potd_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pod,
                            "event_name": "Berth_Transit",
                            "a_time": pot_ata,
                            "e_time": pot_eta,
                        }

                        self.pol_pot_pod_list.append(potd_data)
            elif pot_count == 1:
                for pot_data in pot_datas:
                    etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                    atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                    pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                    pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get('estimatedDateOfArrival') else ''

                    vesselName = pot_data.get('vesselName')
                    voyage = pot_data.get('voyageNo')
                    pol = pot_data.get('portOfLoading')
                    pod = pot_data.get('portOfDischarge')
                    pol_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pol,
                        "event_name": "Departure_POL",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(pol_data)

                    potl_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pod,
                        "event_name": "Berth_POD",
                        "a_time": pot_ata,
                        "e_time": pot_eta,
                    }

                    self.pol_pot_pod_list.append(potl_data)

            content = bl_info['data'].get('content')
            cgo_avail_tm = ""
            if content is not None:
                cargo_tracking_container_list = content.get('cargoTrackingContainer')
                container_count = len(cargo_tracking_container_list)
                bill_item['container_count'] = container_count  # 获取箱子的数量
                bill_item['bl_status'] = content.get('blRealStatus')  # content 下的 blRealStatus
                bill_item['port_cut_off_date'] = format_date(content.get('cargoCutOff'))
                tracking_path = content.get('trackingPath')
                if tracking_path is not None:
                    if tracking_path.get('trackingGroupReferenceCode'):
                        bill_item['booking_no'] = re.findall(r'[\d]+', tracking_path.get('trackingGroupReferenceCode'))[
                            0]
                    if tracking_path.get('blType'):
                        bill_item['bl_type'] = clean_str(tracking_path['blType'])
                    if tracking_path.get('blRealStatus'):
                        bill_item['bl_surrendered_status'] = clean_str(tracking_path['blRealStatus'])
                    if tracking_path.get('fromCity'):
                        bill_item['depart'] = clean_str(tracking_path['fromCity'])
                    if tracking_path.get('pol'):
                        bill_item['load'] = clean_str(tracking_path['pol']).split('-')[0].strip()
                    if tracking_path.get('toCity'):
                        bill_item['arrive'] = clean_str(tracking_path['toCity'])
                    if tracking_path.get('pod'):
                        bill_item['discharge'] = clean_str(tracking_path['pod']).split('-')[0].strip()
                    if tracking_path.get('vslNme'):
                        bill_item['vessel_name'] = clean_str(tracking_path['vslNme'])
                    if tracking_path.get('voyNumber'):
                        bill_item['voyage'] = clean_str(tracking_path['voyNumber'])
                    if tracking_path.get('cgoAvailTm'):
                        cgo_avail_tm = time.strptime(tracking_path.get('cgoAvailTm'), "%Y-%m-%d %H:%M")
                        cgo_avail_tm = time.strftime("%Y-%m-%d %H:%M:%S", cgo_avail_tm)
                        bill_item['eta_at_place_of_delivery'] = cgo_avail_tm

                # 船名航次列表
                vessel_voyage_list = []
                actual_shipment = content.get('actualShipment')
                if actual_shipment:
                    for i in actual_shipment:
                        ves_voy_item = {}
                        ves_voy_item["port_of_loading"] = i.get('portOfLoading')
                        ves_voy_item["port_of_discharge"] = i.get('portOfDischarge')
                        ves_voy_item["vessel_name"] = i.get('vesselName')
                        ves_voy_item["voyage_no"] = i.get('voyageNo')
                        ves_voy_item["rownum"] = i.get("rownum")
                        ves_voy_item["actual_departure_date"] = i.get("actualDepartureDate")
                        ves_voy_item["expected_date_of_departure"] = i.get("expectedDateOfDeparture")
                        ves_voy_item["actual_arrival_date"] = i.get("actualArrivalDate")
                        ves_voy_item["estimated_date_of_arrival"] = i.get("estimatedDateOfArrival")
                        bill_item["actual_arrival_date"] = date_to_format_data(
                            i.get("actualArrivalDate"))  # 新增提单信息实际到港时间
                        vessel_voyage_list.append(ves_voy_item)
                request_time = int(time.time() * 1000)
                bl_url = self.GET_BL_CONTAINER_LIST_URL.format(real_bl, request_time)
                meta['parentData'] = {"bill_item": bill_item, "real_bl": real_bl, "content": content,
                                      "vessel_voyage_list": vessel_voyage_list, 'eta': cgo_avail_tm
                                      }
                for _ in range(3):
                    try:
                        child_request = requests.get(url=bl_url, headers=self.headers, proxies=self.proxies, timeout=self.timeOut, verify=False)
                        self.spider_Data(bl_url, child_request)  # 新增字段
                        child_request.json()
                        break
                    except Exception as err:
                        if _ == 2:
                            raise err
                        time.sleep(1)
                        continue
                return 2, child_request, meta
            else:
                return 3, {}, {}

    def bl_parse_container_list(self, response, meta):
        origin_task_message = self.origin_task_message
        parent_data = meta.get('parentData')
        real_bl = parent_data['real_bl']
        content = parent_data['content']
        bill_item = parent_data['bill_item']
        eta = parent_data['eta']
        vessel_voyage_list = parent_data['vessel_voyage_list']
        cargo_tracking_container = content.get('cargoTrackingContainer')

        # 箱列表
        container_list = []
        container_list_rep = response.json()
        try:
            # 获取箱子信息列表
            container_content_list = container_list_rep['data']['content']
        except:
            container_content_list = ''

        if container_content_list:
            for container_item in container_content_list:
                container_dict = container_info_item()
                if cargo_tracking_container:
                    for container_num in cargo_tracking_container:
                        if container_num.get('cntrNum') in container_item.get('containerNumber') \
                                or container_item.get('containerNumber') in container_num.get('cntrNum'):
                            laden_return = None
                            if container_num.get('ladenReturnDt'):
                                laden_return_dt = time.strptime(container_num['ladenReturnDt'], '%Y-%m-%d %H:%M')
                                laden_return = time.strftime('%Y-%m-%d %H:%M:%S', laden_return_dt)
                            cargo_pickup = None
                            if container_num.get('ladenPickUpDt'):
                                laden_pick_up_dt = time.strptime(container_num['ladenPickUpDt'], '%Y-%m-%d %H:%M')
                                cargo_pickup = time.strftime('%Y-%m-%d %H:%M:%S', laden_pick_up_dt)
                            empty_pick_up_dt = None
                            if container_num.get('emptyPickUpDt'):
                                empty_pick_up_dt = time.strptime(container_num['emptyPickUpDt'], '%Y-%m-%d %H:%M')
                                empty_pick_up_dt = time.strftime('%Y-%m-%d %H:%M:%S', empty_pick_up_dt)
                            empty_return_dt = None
                            if container_num.get('emptyReturnDt'):
                                empty_return_dt = time.strptime(container_num['emptyReturnDt'], '%Y-%m-%d %H:%M')
                                empty_return_dt = time.strftime('%Y-%m-%d %H:%M:%S', empty_return_dt)
                            container_number = clean_str(container_item['containerNumber'])
                            container_size_type = clean_str(container_item['containerType'])
                            if container_size_type:
                                container_size = re.findall(r'([\d]+)', container_size_type)[0]
                                container_type = re.findall(r'([a-zA-Z]+)', container_size_type)[0]
                                container_dict['container_type'] = container_type
                                container_dict['container_size'] = container_size

                            container_seal_no = clean_str(container_item['sealNumber'])
                            container_dict['container_no'] = container_number
                            bill_item['container_list'].append(container_number)  # 新增字段
                            container_dict['bl_no'] = meta.get('blNo')
                            container_dict['seal_no'] = container_seal_no
                            container_dict['laden_return'] = laden_return
                            container_dict['cargo_pickup'] = cargo_pickup
                            container_dict['empty_pick_up_date'] = empty_pick_up_dt
                            container_dict['empty_return_date'] = empty_return_dt
                            container_dict['eta'] = eta
                            container_list.append(container_dict)
                else:
                    container_number = clean_str(container_item['containerNumber'])
                    container_size_type = clean_str(container_item['containerType'])
                    container_type = None
                    container_size = None
                    if container_size_type:
                        container_size = re.findall(r'([\d]+)', container_size_type)[0]
                        container_type = re.findall(r'([a-zA-Z]+)', container_size_type)[0]
                    container_seal_no = clean_str(container_item['sealNumber'])
                    container_dict['container_no'] = container_number
                    bill_item['container_list'].append(container_number)  # 新增字段
                    container_dict['container_type'] = container_type
                    container_dict['container_size'] = container_size
                    container_dict['seal_no'] = container_seal_no
                    container_dict['eta'] = eta
                    container_list.append(container_dict)

            # 补充箱事件
            add_event = []
            if len(vessel_voyage_list) == 1:
                for i in vessel_voyage_list:
                    container_event = tracking_event_item()
                    container_event['vessel_name'] = i.get('vessel_name')
                    container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                    container_event['event_name'] = "Sail Pol"  # 事件名称  type: string
                    container_event['a_time'] = date_to_format_data(
                        i.get('actual_departure_date'))  # 事件实际时间  type: string
                    container_event['e_time'] = date_to_format_data(
                        i.get('expected_date_of_departure'))  # 事件预计时间  type: string
                    container_event['location_name'] = bill_item['load']  # 位置名称  type: string
                    add_event.append(container_event)
                    container_event = tracking_event_item()
                    container_event['vessel_name'] = i.get('vessel_name')
                    container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                    container_event['event_name'] = "Arrive Pod"  # 事件名称  type: string
                    container_event['a_time'] = date_to_format_data(
                        i.get('actual_arrival_date'))  # 事件实际时间  type: string
                    container_event['e_time'] = date_to_format_data(
                        i.get('estimated_date_of_arrival'))  # 事件预计时间  type: string
                    container_event['location_name'] = bill_item['discharge']  # 位置名称  type: string
                    add_event.append(container_event)
            else:
                for i in vessel_voyage_list:
                    if i.get("rownum") == "1":
                        container_event = tracking_event_item()
                        container_event['vessel_name'] = i.get('vessel_name')
                        container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                        container_event['event_name'] = "Sail Pol"  # 事件名称  type: string
                        container_event['a_time'] = date_to_format_data(
                            i.get('actual_departure_date'))  # 事件实际时间  type: string
                        container_event['e_time'] = date_to_format_data(
                            i.get('expected_date_of_departure'))  # 事件预计时间  type: string
                        container_event['location_name'] = bill_item['load']  # 位置名称  type: string
                        add_event.append(container_event)
                    if int(i.get("rownum")) == len(vessel_voyage_list):
                        container_event = tracking_event_item()
                        container_event['vessel_name'] = i.get('vessel_name')
                        container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                        container_event['transport_mode'] = 'Vessel'  # 交通工具  type: string
                        container_event['event_name'] = "Arrive Pod"  # 事件名称  type: string
                        container_event['a_time'] = date_to_format_data(
                            i.get('actual_arrival_date'))  # 事件实际时间  type: string
                        container_event['e_time'] = date_to_format_data(
                            i.get('estimated_date_of_arrival'))  # 事件预计时间  type: string
                        container_event['location_name'] = bill_item['discharge']  # 位置名称  type: string
                        add_event.append(container_event)
            if cargo_tracking_container:
                laden_return_dt_list = []
                laden_pick_up_dt_list = []
                for x in cargo_tracking_container:
                    if x.get("ladenReturnDt"):
                        laden_return_dt_list.append(x)
                for x in cargo_tracking_container:
                    if x.get("ladenPickUpDt"):
                        laden_pick_up_dt_list.append(x)
                if laden_return_dt_list:
                    laden_return_dt_list = sorted(laden_return_dt_list, key=lambda x: x.get("ladenReturnDt"))
                if laden_pick_up_dt_list:
                    laden_pick_up_dt_list = sorted(laden_pick_up_dt_list, key=lambda x: x.get("ladenPickUpDt"))
                container_event = tracking_event_item()
                if laden_return_dt_list:
                    transport_mode = [i.get("transportation") for i in container_content_list if
                                      laden_return_dt_list[-1].get("cntrNum") == i.get("containerNumber")]
                    if transport_mode:
                        container_event['transport_mode'] = transport_mode[0]  # 交通工具  type: string
                container_event['event_name'] = "Pol Return"  # 事件名称  type: string
                if laden_return_dt_list:
                    container_event['a_time'] = date_to_format_data(
                        laden_return_dt_list[-1].get("ladenReturnDt"))  # 事件实际时间  type: string
                container_event['location_name'] = bill_item['depart']  # 位置名称  type: string
                add_event.append(container_event)
                container_event = tracking_event_item()
                if laden_pick_up_dt_list:
                    transport_mode = [i.get("transportation") for i in container_content_list if
                                      laden_pick_up_dt_list[0].get("cntrNum") == i.get("containerNumber")]
                    if transport_mode:
                        container_event['transport_mode'] = transport_mode[0]  # 交通工具  type: string
                container_event['event_name'] = "Take Goods Pod"  # 事件名称  type: string
                container_event['location_name'] = bill_item['discharge']  # 位置名称  type: string
                container_event['e_time'] = None
                container_event['a_time'] = None
                if bill_item.get('eta_at_place_of_delivery'):
                    if transfor_standard_datetime_to_timestamp(bill_item.get('eta_at_place_of_delivery'))[1]:
                        container_event['e_time'] = bill_item['eta_at_place_of_delivery']  # 事件实际时间  type: string
                    else:
                        if laden_pick_up_dt_list:
                            container_event['a_time'] = date_to_format_data(
                                laden_pick_up_dt_list[0].get("ladenPickUpDt"))  # 事件实际时间  type: string
                if container_event['e_time'] or container_event['a_time']:
                    add_event.append(container_event)
            if container_list:
                for container in container_list:
                    request_time = int(time.time() * 1000)
                    bl_url = self.GET_BL_CONTAINER_DETAIL_URL.format(container['container_no'], real_bl, request_time)
                    meta['parentData'] = {'container': container, "add_event": add_event, "real_bl": real_bl,
                                          "vessel_voyage_list": vessel_voyage_list, 'bill_item': bill_item}
                    for _ in range(3):
                        try:
                            child_request = requests.get(url=bl_url, headers=self.headers, proxies=self.proxies, timeout=self.timeOut, verify=False)
                            self.spider_Data(bl_url, child_request)  # 新增字段
                            child_request.json()
                            break
                        except Exception as err:
                            if _ == 2:
                                raise err
                            time.sleep(1)
                            continue
                    yield child_request, meta
            # yield False, {'ms_type': 'data', 'data': {}}
        else:
            yield False, {'ms_type': 'data', 'data': return_tracking_info(receive_task_message=origin_task_message, bill_item=bill_item)}

    def bl_parse_container_info(self, response, meta):
        parent_data = meta.get('parentData')
        real_bl = parent_data['real_bl']
        container = parent_data['container']
        add_event = parent_data['add_event']
        vessel_voyage_list = parent_data['vessel_voyage_list']

        try:
            container_info = response.json()
        except:
            container_info = {}
        if container_info.get('data'):
            container_event_list = container_info['data']['content']
        else:
            return False, {'ms_type': 'data', 'data': {}, 'isReturn': 0}
        for container_event_item in container_event_list:
            container_event = tracking_event_item()
            location_name = container_event_item.get('location')
            container_event['location_name'] = location_name
            container_event['transport_mode'] = container_event_item.get('transportation')
            event_name = container_event_item.get('containerNumberStatus')
            if ',' in location_name:
                dock = location_name.split(',')[0]
                container_event['dock_name'] = dock
            container_event['event_name'] = event_name
            if container_event_item.get('transportation') == 'Vessel' or \
                    container_event_item.get('transportation') == " ":
                for i in vessel_voyage_list:
                    port_of_load = i.get('port_of_loading').strip().replace(' ', '').upper()
                    port_of_discharge = i.get('port_of_discharge').strip().replace(' ', '').upper()
                    if (re.findall(r'{}'.format(port_of_load),
                                   location_name.strip().replace(' ', '').upper(), re.S) and re.findall(
                        r'Loaded', event_name, re.S)) or (re.findall(r'{}'.format(port_of_discharge),
                                                                     location_name.strip().replace(' ', '').upper(),
                                                                     re.S) and re.findall(r'Discharged', event_name,
                                                                                          re.S)):
                        container_event['vessel_name'] = i.get('vessel_name')
                        container_event['voyage'] = i.get('voyage_no')
                        container_event['transport_mode'] = 'Vessel'

            if container_event_item.get('timeOfIssue'):
                event_time = time.strptime(container_event_item.get('timeOfIssue'), "%Y-%m-%d %H:%M")
                event_date = time.strftime("%Y-%m-%d %H:%M:%S", event_time)
                time_struct = int(time.mktime(time.strptime(event_date, "%Y-%m-%d %H:%M:%S")))
                if time_struct < int(time.time()):
                    container_event['a_time'] = event_date
                else:
                    container_event['e_time'] = event_date
            else:
                container_event['a_time'] = ''
                container_event['e_time'] = ''


            container['event_list'].append(container_event)

        """ 箱事件排序 """
        container['event_list'] = quick_sort(container['event_list'])
        if self.pol_pot_pod_list:
            for pot in self.pol_pot_pod_list:
                container['event_list'].append(
                    pot
                )
        # if add_event and container['event_list']:
        #     container['event_list'] += add_event
        # Latest Container Status
        request_time = int(time.time() * 1000)
        latest_container_status_url = 'https://elines.coscoshipping.com/ebtracking/public/bill/containers/{}?timestamp={}'.format(
            real_bl, request_time)
        for _ in range(3):
            try:
                child_request = requests.get(url=latest_container_status_url, headers=self.headers, proxies=self.proxies, timeout=self.timeOut, verify=False)
                self.spider_Data(latest_container_status_url, child_request)  # 新增字段
                child_request.json()
                break
            except Exception as err:
                if _ == 2:
                    raise err
                time.sleep(1)
                continue
        return child_request, meta

    def bl_parse_latest_container_status_data(self, response, meta):
        origin_task_message = self.origin_task_message
        parent_data = meta['parentData']
        container = parent_data['container']
        bill_item = parent_data['bill_item']
        try:
            latest_container_status_data = response.json()             # booking/containers
        except:
            latest_container_status_data = {}
        if latest_container_status_data.get('data'):
            latest_data_list = latest_container_status_data['data']['content']
        else:
            return {'ms_type': 'data', 'data': {}, 'isReturn': 0}

        latest_container_status_item_list = []
        for latest_data in latest_data_list:
            latest_container_status_item = {}
            latest_container_status_item["container_no"] = latest_data['containerNumber']
            latest_container_status_item["container_type"] = latest_data['containerType']
            latest_container_status_item["gross_weight"] = latest_data['grossWeight']
            latest_container_status_item["pieces_number"] = latest_data['piecesNumber']
            latest_container_status_item["latest_location"] = latest_data['location']
            latest_container_status_item["seal_no"] = latest_data['sealNumber']
            latest_container_status_item["event_name"] = latest_data['label']
            latest_container_status_item["date_time"] = latest_data['locationDateTime']
            latest_container_status_item["transportation"] = latest_data['transportation']
            latest_container_status_item_list.append(latest_container_status_item)

        for latest_container_status in latest_container_status_item_list:
            if container['container_no'] == latest_container_status['container_no']:
                container['container_weight'] = latest_container_status['gross_weight']
                container['quantity'] = str(latest_container_status['pieces_number']) if latest_container_status[
                    'pieces_number'] else None
                container['latest_location'] = latest_container_status["latest_location"]
                container['latest_event_name'] = latest_container_status["event_name"]
                container['latest_location_date'] = latest_container_status['date_time']
                return {'ms_type': 'data',
                       'data': return_tracking_info(receive_task_message=origin_task_message, bill_item=bill_item,
                                                    container_info=container)}
        return {'ms_type': 'data', 'data': {}, 'isReturn': 0}

    ### 订舱号查询 ###
    def bk_get_container_list(self, response, meta):
        real_bl = meta.get('parentData')
        # 提单基本信息
        bill_item = bill_info_item()
        bill_item['bl_no'] = self.busi_data.get('blNo')
        bill_item['carrier_id'] = self.busi_data.get('carrierId')
        bill_item['carrier_code'] = self.busi_data.get('carrierCode')
        bill_item['task_id'] = self.busi_data.get('taskId')


        bl_info = response.json()                  # booking

        # 请求成功，但是没有数据
        if bl_info.get('message') == '无数据':
            return False, {'ms_type': 'data', 'data': {}}

        if not bl_info.get('data') or not bl_info.get('data').get('content'):
            return False, {'ms_type': 'data', 'data': {}}
        # 请求成功，并且有数据
        else:
            pot_datas = bl_info.get('data').get('content')['actualShipment']

            pot_count = len(pot_datas)


            if pot_count > 1:

                for index, pot_data in enumerate(pot_datas):
                    index += 1

                    if index == 1:
                        etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                        atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                        pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                        pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get(
                            'estimatedDateOfArrival') else ''

                        vesselName = pot_data.get('vesselName')
                        voyage = pot_data.get('voyageNo')
                        pol = pot_data.get('portOfLoading')
                        pod = pot_data.get('portOfDischarge')
                        pol_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pol,
                            "event_name": "Departure_POL",
                            "a_time": atd,
                            "e_time": etd,
                        }
                        self.pol_pot_pod_list.append(pol_data)

                        potl_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pod,
                            "event_name": "Berth_Transit",
                            "a_time": pot_ata,
                            "e_time": pot_eta,
                        }

                        self.pol_pot_pod_list.append(potl_data)


                    elif index == pot_count:

                        etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                        atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                        pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                        pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get(
                            'estimatedDateOfArrival') else ''

                        vesselName = pot_data.get('vesselName')

                        voyage = pot_data.get('voyageNo')

                        pol = pot_data.get('portOfLoading')
                        pod = pot_data.get('portOfDischarge')

                        pod_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pol,
                            "event_name": "Departure_Transit",
                            "a_time": atd,
                            "e_time": etd,
                        }
                        self.pol_pot_pod_list.append(pod_data)

                        potd_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pod,
                            "event_name": "Berth_POD",
                            "a_time": pot_ata,
                            "e_time": pot_eta
                        }
                        self.pol_pot_pod_list.append(potd_data)
                    else:

                        etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                        atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                        pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                        pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get(
                            'estimatedDateOfArrival') else ''

                        vesselName = pot_data.get('vesselName')
                        voyage = pot_data.get('voyageNo')
                        pol = pot_data.get('portOfLoading')
                        pod = pot_data.get('portOfDischarge')

                        pod_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pol,
                            "event_name": "Departure_Transit",
                            "a_time": atd,
                            "e_time": etd,
                        }
                        self.pol_pot_pod_list.append(pod_data)
                        potd_data = {
                            "vessel_name": vesselName,
                            "voyage": voyage,
                            "location_name": pod,
                            "event_name": "Berth_Transit",
                            "a_time": pot_ata,
                            "e_time": pot_eta,
                        }

                        self.pol_pot_pod_list.append(potd_data)
            elif pot_count == 1:
                for pot_data in pot_datas:
                    etd = pot_data.get('expectedDateOfDeparture') if pot_data.get('expectedDateOfDeparture') else ''

                    atd = pot_data.get('actualDepartureDate') if pot_data.get('actualDepartureDate') else ''

                    pot_ata = pot_data.get('actualArrivalDate') if pot_data.get('actualArrivalDate') else ''

                    pot_eta = pot_data.get('estimatedDateOfArrival') if pot_data.get('estimatedDateOfArrival') else ''

                    vesselName = pot_data.get('vesselName')
                    voyage = pot_data.get('voyageNo')
                    pol = pot_data.get('portOfLoading')
                    pod = pot_data.get('portOfDischarge')
                    pol_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pol,
                        "event_name": "Departure_POL",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    self.pol_pot_pod_list.append(pol_data)

                    potl_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pod,
                        "event_name": "Berth_POD",
                        "a_time": pot_ata,
                        "e_time": pot_eta,
                    }

                    self.pol_pot_pod_list.append(potl_data)

            content = bl_info['data'].get('content')
            cgo_avail_tm = ""
            if content is not None:
                bl_no_stauts = content.get('blRealStatus')
                bill_item['bl_status'] = bl_no_stauts if bl_no_stauts else None
                try:
                    port_cut_off_date = time.strptime(content.get('cargoCutOff'), "%Y-%m-%d %H:%M")
                    port_cut_off_date = time.strftime("%Y-%m-%d %H:%M:%S", port_cut_off_date)
                except:
                    port_cut_off_date = ''
                bill_item['port_cut_off_date'] = port_cut_off_date
                bill_item['container_count'] = len(content.get('cargoTrackingContainer'))
                tracking_path = content.get('trackingPath')
                if tracking_path:
                    if tracking_path.get('trackingGroupReferenceCode'):
                        bill_item['booking_no'] = \
                            re.findall(r'[\d]+', tracking_path.get('trackingGroupReferenceCode'))[0]
                    if tracking_path.get('blType'):
                        bill_item['bl_type'] = clean_str(tracking_path['blType'])
                    if tracking_path.get('blRealStatus'):
                        bill_item['bl_surrendered_status'] = clean_str(tracking_path['blRealStatus'])
                    if tracking_path.get('fromCity'):
                        bill_item['depart'] = clean_str(tracking_path['fromCity'])
                    if tracking_path.get('pol'):
                        bill_item['load'] = clean_str(tracking_path['pol']).split('-')[0].strip()
                    if tracking_path.get('toCity'):
                        bill_item['arrive'] = clean_str(tracking_path['toCity'])
                    if tracking_path.get('pod'):
                        bill_item['discharge'] = clean_str(tracking_path['pod']).split('-')[0].strip()
                    if tracking_path.get('vslNme'):
                        bill_item['vessel_name'] = clean_str(tracking_path['vslNme'])
                    if tracking_path.get('voyNumber'):
                        bill_item['voyage'] = clean_str(tracking_path['voyNumber'])
                    if tracking_path.get('cgoAvailTm'):
                        cgo_avail_tm = time.strptime(tracking_path.get('cgoAvailTm'), "%Y-%m-%d %H:%M")
                        cgo_avail_tm = time.strftime("%Y-%m-%d %H:%M:%S", cgo_avail_tm)
                        bill_item['eta_at_place_of_delivery'] = cgo_avail_tm

                # 船名航次列表
                vessel_voyage_list = []
                actual_shipment = content.get('actualShipment')
                if actual_shipment:
                    for i in actual_shipment:
                        ves_voy_item = {}
                        ves_voy_item["port_of_loading"] = i.get('portOfLoading')
                        ves_voy_item["port_of_discharge"] = i.get('portOfDischarge')
                        ves_voy_item["vessel_name"] = i.get('vesselName')
                        ves_voy_item["voyage_no"] = i.get('voyageNo')
                        vessel_voyage_list.append(ves_voy_item)
                request_time = int(time.time() * 1000)
                bk_url = self.GET_BK_CONTAINER_LIST_URL.format(real_bl, request_time)
                meta['parentData'] = {"bill_item": bill_item, "real_bl": real_bl, "content": content,
                                      "vessel_voyage_list": vessel_voyage_list, 'eta': cgo_avail_tm
                                      }
                for _ in range(3):
                    try:
                        child_request = requests.get(url=bk_url, headers=self.headers, proxies=self.proxies, timeout=self.timeOut, verify=False)
                        self.spider_Data(bk_url, child_request)  # 新增字段
                        child_request.json()
                        break
                    except Exception as err:
                        if _ == 2:
                            raise err
                        time.sleep(1)
                        continue
                return child_request, meta
            else:
                return False, {'ms_type': 'data', 'data': {}, 'isReturn': 0}

    def bk_parse_container_list(self, response, meta):

        origin_task_message = self.origin_task_message
        parent_data = meta.get('parentData')
        real_bl = parent_data['real_bl']
        content = parent_data['content']
        bill_item = parent_data['bill_item']
        eta = parent_data['eta']
        self.pol_pot_pod_list = parent_data['vessel_voyage_list']
        vessel_voyage_list = parent_data['vessel_voyage_list']
        cargo_tracking_container = content.get('cargoTrackingContainer')  # 返回 list 类型

        # 箱列表
        container_list = []

        container_list_rep = response.json()

        try:
            # 获取箱子信息列表
            container_content_list = container_list_rep['data']['content']
        except:
            container_content_list = ''

        if container_content_list:
            for container_item in container_content_list:
                container_dict = container_info_item()
                container_dict['event_list'] = []
                container_dict['bl_no'] = meta.get('blNo')
                if cargo_tracking_container:
                    for container_num in cargo_tracking_container:
                        if container_num.get('cntrNum') in container_item.get('containerNumber') or \
                                container_item.get('containerNumber') in container_num.get('cntrNum'):
                            laden_return = None
                            if container_num.get('ladenReturnDt'):
                                laden_return_dt = time.strptime(container_num['ladenReturnDt'], '%Y-%m-%d %H:%M')
                                laden_return = time.strftime('%Y-%m-%d %H:%M:%S', laden_return_dt)
                            cargo_pickup = None
                            if container_num.get('ladenPickUpDt'):
                                laden_pick_up_dt = time.strptime(container_num['ladenPickUpDt'], '%Y-%m-%d %H:%M')
                                cargo_pickup = time.strftime('%Y-%m-%d %H:%M:%S', laden_pick_up_dt)
                            empty_pick_up_dt = None
                            if container_num.get('emptyPickUpDt'):
                                empty_pick_up_dt = time.strptime(container_num['emptyPickUpDt'], '%Y-%m-%d %H:%M')
                                empty_pick_up_dt = time.strftime('%Y-%m-%d %H:%M:%S', empty_pick_up_dt)
                            empty_return_dt = None
                            if container_num.get('emptyReturnDt'):
                                empty_return_dt = time.strptime(container_num['emptyReturnDt'], '%Y-%m-%d %H:%M')
                                empty_return_dt = time.strftime('%Y-%m-%d %H:%M:%S', empty_return_dt)
                            container_number = clean_str(container_item['containerNumber'])
                            container_size_type = clean_str(container_item['containerType'])
                            container_type = None
                            container_size = None
                            if container_size_type:
                                container_size = re.findall(r'([\d]+)', container_size_type)[0]
                                container_type = re.findall(r'([a-zA-Z]+)', container_size_type)[0]
                            container_seal_no = clean_str(container_item['sealNumber'])
                            container_dict['container_no'] = container_number
                            bill_item['container_list'].append(container_number)  # 新增字段
                            container_dict['container_type'] = container_type
                            container_dict['container_size'] = container_size
                            container_dict['seal_no'] = container_seal_no
                            container_dict['laden_return'] = laden_return
                            container_dict['cargo_pickup'] = cargo_pickup
                            container_dict['empty_pick_up_date'] = empty_pick_up_dt
                            container_dict['empty_return_date'] = empty_return_dt
                            container_dict['eta'] = eta
                            container_list.append(container_dict)
                else:
                    container_number = clean_str(container_item['containerNumber'])
                    container_size_type = clean_str(container_item['containerType'])
                    container_type = None
                    container_size = None
                    if container_size_type:
                        container_size = re.findall(r'([\d]+)', container_size_type)[0]
                        container_type = re.findall(r'([a-zA-Z]+)', container_size_type)[0]
                    container_seal_no = clean_str(container_item['sealNumber'])
                    container_dict['container_no'] = container_number
                    bill_item['container_list'].append(container_number)  # 新增字段
                    container_dict['container_type'] = container_type
                    container_dict['container_size'] = container_size
                    container_dict['seal_no'] = container_seal_no
                    container_dict['eta'] = eta
                    container_list.append(container_dict)
            # 补充箱事件
            add_event = []
            if len(vessel_voyage_list) == 1:
                for i in vessel_voyage_list:
                    container_event = tracking_event_item()
                    container_event['vessel_name'] = i.get('vessel_name')
                    container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                    container_event['event_name'] = "Sail Pol"  # 事件名称  type: string
                    container_event['a_time'] = date_to_format_data(
                        i.get('actual_departure_date'))  # 事件实际时间  type: string
                    container_event['e_time'] = date_to_format_data(
                        i.get('expected_date_of_departure'))  # 事件预计时间  type: string
                    container_event['location_name'] = bill_item['load']  # 位置名称  type: string
                    add_event.append(container_event)
                    container_event = tracking_event_item()
                    container_event['vessel_name'] = i.get('vessel_name')
                    container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                    container_event['event_name'] = "Arrive Pod"  # 事件名称  type: string
                    container_event['a_time'] = date_to_format_data(
                        i.get('actual_arrival_date'))  # 事件实际时间  type: string
                    container_event['e_time'] = date_to_format_data(
                        i.get('estimated_date_of_arrival'))  # 事件预计时间  type: string
                    container_event['location_name'] = bill_item['discharge']  # 位置名称  type: string
                    add_event.append(container_event)
            else:
                for i in vessel_voyage_list:
                    if i.get("rownum") == "1":
                        container_event = tracking_event_item()
                        container_event['vessel_name'] = i.get('vessel_name')
                        container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                        container_event['event_name'] = "Sail Pol"  # 事件名称  type: string
                        container_event['a_time'] = date_to_format_data(
                            i.get('actual_departure_date'))  # 事件实际时间  type: string
                        container_event['e_time'] = date_to_format_data(
                            i.get('expected_date_of_departure'))  # 事件预计时间  type: string
                        container_event['location_name'] = bill_item['load']  # 位置名称  type: string
                        add_event.append(container_event)
                    if i.get("rownum"):
                        if int(i.get("rownum")) == len(vessel_voyage_list):
                            container_event = tracking_event_item()
                            container_event['vessel_name'] = i.get('vessel_name')
                            container_event['voyage'] = i.get('voyage_no')  # 航次  type: string
                            container_event['transport_mode'] = 'Vessel'  # 交通工具  type: string
                            container_event['event_name'] = "Arrive Pod"  # 事件名称  type: string
                            container_event['a_time'] = date_to_format_data(
                                i.get('actual_arrival_date'))  # 事件实际时间  type: string
                            container_event['e_time'] = date_to_format_data(
                                i.get('estimated_date_of_arrival'))  # 事件预计时间  type: string
                            container_event['location_name'] = bill_item['discharge']  # 位置名称  type: string
                            add_event.append(container_event)
            if cargo_tracking_container:
                ladenReturnDt_list = []
                ladenPickUpDt_list = []
                for x in cargo_tracking_container:
                    if x.get("ladenReturnDt"):
                        ladenReturnDt_list.append(x)
                for x in cargo_tracking_container:
                    if x.get("ladenPickUpDt"):
                        ladenPickUpDt_list.append(x)
                if ladenReturnDt_list:
                    ladenReturnDt_list = sorted(ladenReturnDt_list, key=lambda x: x.get("ladenReturnDt"))
                if ladenPickUpDt_list:
                    ladenPickUpDt_list = sorted(ladenPickUpDt_list, key=lambda x: x.get("ladenPickUpDt"))
                container_event = tracking_event_item()
                if ladenReturnDt_list:
                    transport_mode = [i.get("transportation") for i in container_content_list if
                                      ladenReturnDt_list[-1].get("cntrNum") == i.get("containerNumber")]
                    if transport_mode:
                        container_event['transport_mode'] = transport_mode[0]  # 交通工具  type: string
                container_event['event_name'] = "Pol Return"  # 事件名称  type: string
                if ladenReturnDt_list:
                    container_event['a_time'] = date_to_format_data(
                        ladenReturnDt_list[-1].get("ladenReturnDt"))  # 事件实际时间  type: string
                container_event['location_name'] = bill_item['depart']  # 位置名称  type: string
                add_event.append(container_event)
                container_event = tracking_event_item()
                if ladenPickUpDt_list:
                    transport_mode = [i.get("transportation") for i in container_content_list if
                                      ladenPickUpDt_list[0].get("cntrNum") == i.get("containerNumber")]
                    container_event['transport_mode'] = transport_mode[0]  # 交通工具  type: string
                container_event['event_name'] = "Take Goods Pod"  # 事件名称  type: string
                container_event['location_name'] = bill_item['discharge']  # 位置名称  type: string
                container_event['e_time'] = None
                container_event['a_time'] = None
                if bill_item['eta_at_place_of_delivery']:
                    if transfor_standard_datetime_to_timestamp(bill_item['eta_at_place_of_delivery'])[1]:
                        container_event['e_time'] = bill_item['eta_at_place_of_delivery']  # 事件实际时间  type: string
                    else:
                        if ladenPickUpDt_list:
                            container_event['a_time'] = date_to_format_data(
                                ladenPickUpDt_list[0].get("ladenPickUpDt"))  # 事件实际时间  type: string
                if container_event['e_time'] or container_event['a_time']:
                    add_event.append(container_event)

            if container_list:
                for container in container_list:
                    request_time = int(time.time() * 1000)
                    bk_url = self.GET_BK_CONTAINER_DETAIL_URL.format(container['container_no'], real_bl, request_time)
                    meta['parentData'] = {'container': container, 'add_event': add_event, 'real_bl': real_bl,
                                          'vessel_voyage_list': vessel_voyage_list, 'bill_item': bill_item}
                    for _ in range(3):
                        try:
                            child_request = requests.get(url=bk_url, headers=self.headers, proxies=self.proxies, timeout=self.timeOut, verify=False)
                            self.spider_Data(bk_url, child_request)  # 新增字段
                            child_request.json()
                            break
                        except Exception as err:
                            if _ == 2:
                                raise err
                            time.sleep(1)
                            continue
                    yield child_request, meta

            else:
                origin_task_message = self.origin_task_message
                yield False, {'ms_type': 'data',
                       'data': return_tracking_info(receive_task_message=origin_task_message, bill_item=bill_item)}
        else:

            yield False, {'ms_type': 'data',
                   'data': return_tracking_info(receive_task_message=origin_task_message, bill_item=bill_item)}

    def bk_parse_container_info(self, response, meta):
        # meta = self.message.busiData
        parent_data = meta.get('parentData')
        real_bl = parent_data['real_bl']
        container = parent_data['container']
        add_event = parent_data['add_event']

        vessel_voyage_list = parent_data['vessel_voyage_list']

        container_info = response.json()

        if container_info.get('data'):
            container_event_list = container_info['data']['content']
        else:
            return False, {'ms_type': 'data', 'data': {}, 'isReturn': 0}

        for container_event_item in container_event_list:
            container_event = tracking_event_item()
            location_name = container_event_item.get('location')
            container_event['location_name'] = location_name
            container_event['transport_mode'] = container_event_item.get('transportation')
            event_name = container_event_item.get('containerNumberStatus')
            if ',' in location_name:
                dock = location_name.split(',')[0]
                container_event['dock_name'] = dock

            container_event['event_name'] = event_name
            if container_event_item.get('transportation') == 'Vessel' or \
                    container_event_item.get('transportation') == " ":
                for i in vessel_voyage_list:
                    port_of_load = i.get('port_of_loading').strip().replace(' ', '').upper()
                    port_of_discharge = i.get('port_of_discharge').strip().replace(' ', '').upper()
                    if re.findall(r'{}'.format(port_of_load),
                                  location_name.strip().replace(' ', '').upper(), re.S) and \
                            re.findall(r'Loaded', event_name, re.S):
                        container_event['vessel_name'] = i.get('vessel_name')
                        container_event['voyage'] = i.get('voyage_no')
                        container_event['transport_mode'] = 'Vessel'
                    elif re.findall(r'{}'.format(port_of_discharge),
                                    location_name.strip().replace(' ', '').upper(), re.S) and \
                            re.findall(r'Discharged', event_name, re.S):
                        container_event['vessel_name'] = i.get('vessel_name')
                        container_event['voyage'] = i.get('voyage_no')
                        container_event['transport_mode'] = 'Vessel'
            event_time = time.strptime(container_event_item.get('timeOfIssue'), "%Y-%m-%d %H:%M")
            event_date = time.strftime("%Y-%m-%d %H:%M:%S", event_time)
            time_struct = int(time.mktime(time.strptime(event_date, "%Y-%m-%d %H:%M:%S")))
            if time_struct < int(time.time()):
                container_event['a_time'] = event_date
            else:
                container_event['e_time'] = event_date
            container['event_list'].append(container_event)

        """ 箱事件排序 """
        container['event_list'] = quick_sort(container['event_list'])
        if self.pol_pot_pod_list:
            for pot in self.pol_pot_pod_list:
                container['event_list'].append(
                    pot
                )
        request_time = int(time.time() * 1000)
        latest_container_status_url = 'https://elines.coscoshipping.com/ebtracking/public/booking/containers/{}?timestamp={}'.format(
            real_bl, request_time)
        for _ in range(3):
            try:
                child_request = requests.get(url=latest_container_status_url, headers=self.headers, proxies=self.proxies, timeout=self.timeOut, verify=False)
                self.spider_Data(latest_container_status_url, child_request)  # 新增字段
                child_request.json()
                break
            except Exception as err:
                if _ == 2:
                    raise err
                time.sleep(1)
                continue
        return child_request, meta

    def bk_parse_latest_container_status_data(self, response, meta):
        origin_task_message = self.origin_task_message
        parent_data = meta['parentData']
        container = parent_data['container']
        bill_item = parent_data['bill_item']

        latest_container_status_data = json.loads(response.text)

        try:
            if latest_container_status_data.get('data'):
                latest_data_list = latest_container_status_data['data']['content']
            else:
                return {'ms_type': 'data', 'data': {}, 'isReturn': 0}
        except:
            return {'ms_type': 'data', 'data': {}, 'isReturn': 0}


        latest_container_status_item_list = []
        for latest_data in latest_data_list:
            latest_container_status_item = {}
            latest_container_status_item["container_no"] = latest_data['containerNumber']
            latest_container_status_item["container_type"] = latest_data['containerType']
            latest_container_status_item["gross_weight"] = latest_data['grossWeight']
            latest_container_status_item["pieces_number"] = latest_data['piecesNumber']
            latest_container_status_item["latest_location"] = latest_data['location']
            latest_container_status_item["seal_no"] = latest_data['sealNumber']
            latest_container_status_item["event_name"] = latest_data['label']
            latest_container_status_item["date_time"] = latest_data['locationDateTime']
            latest_container_status_item["transportation"] = latest_data['transportation']
            latest_container_status_item_list.append(latest_container_status_item)

        for latest_container_status in latest_container_status_item_list:
            if container['container_no'] == latest_container_status['container_no']:
                container['container_weight'] = latest_container_status['gross_weight']
                container['quantity'] = str(latest_container_status['pieces_number']) if latest_container_status[
                    'pieces_number'] else None
                container['latest_location'] = latest_container_status["latest_location"]
                container['latest_event_name'] = latest_container_status["event_name"]
                container['latest_location_date'] = latest_container_status['date_time']
                return {'ms_type': 'data',
                       'data': return_tracking_info(receive_task_message=origin_task_message, bill_item=bill_item,
                                                    container_info=container)}
            else:
                continue
        return {'ms_type': 'data',
                'data': return_tracking_info(receive_task_message=origin_task_message, bill_item=bill_item)}


    def run(self):
        # 1.判断订阅参数,如果没有提单号就直接返回
        if not self.bl_no:
            return
        response, meta = self.parse(self.bl_no)
        # if not response:
        #     raise ValueError(self.exception)
        # 2.解析响应
        num, response, meta = self.bl_get_container_list(response, meta)
        if num == 2:
            result_list = []
            response = self.bl_parse_container_list(response, meta)
            for res, met in response:
                if not res:
                    result_list.append(meta.get('data'))
                    return result_list
                response, meta = self.bl_parse_container_info(res, met)
                if not response:
                    result_list.append(meta.get('data'))
                    return result_list
                result = self.bl_parse_latest_container_status_data(response, meta)
                result_list.append(result.get('data'))
            return result_list
        elif num == 1:
            result_list = []
            response, meta = self.bk_get_container_list(response, meta)
            if not response:
                result_list.append(meta.get('data'))
                return result_list
            response = self.bk_parse_container_list(response, meta)
            for res, met in response:
                if not res:
                    result_list.append(met.get('data'))
                    return result_list
                response, meta = self.bk_parse_container_info(res, met)
                if not response:
                    result_list.append(met.get('data'))
                    return result_list
                result = self.bk_parse_latest_container_status_data(response, meta)
                result_list.append(result.get('data'))
            return result_list
        else:
            return []


    def run_server(self):
        for i in range(5):  # 尝试5次
            try:
                result_list = self.run()
            except Exception as e:
                if i == 4:
                    return json.dumps({"status": "success", "data": {}, "spiderData": self.spiderData}, ensure_ascii=False)
                continue
            else:
                if result_list:
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

                        if len(voyage_list) >=5:
                            del voyage_list[1]
                            del voyage_list[2]

                        for index, i in enumerate(voyage_list):
                            index += 1
                            i['sort'] = index

                        for data in result_list:
                            data['billInfo']['voyage_list'] = voyage_list
                    return_data = {"status": "success", "data": result_list, "spiderData": self.spiderData}
                else:
                    return_data = {"status": "success", "data": {}, "spiderData": self.spiderData}
                return json.dumps(return_data, ensure_ascii=False)
        return json.dumps({"status": "success", "data": {}, "spiderData": self.spiderData}, ensure_ascii=False)


if __name__ == '__main__':
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

            return {'agentDomain': 'http-proxy-t1.dobel.cn:9180', 'agentAccount': 'QRKJDUOBEIEFH7TM2K7', 'agentToken': 'POFhPzAq', 'agentId': 64}

        def to_dict(self):
            return {}


    # "COSU6881599870"
    # "COSU6334634480"
    # "7232001550"
    # 6343032820
    # 6888906620
    # 6342851160
    # 6888902800
    # 6342836540  时间匹配错误
    message = {"blNo": "COSU6357693840","carrierCode":"COSCO","carrierId":4528,"realTime":0,"taskId":6742985,"traceId":"test","type":"bl"}
    message = Message(message)
    start = int(time.time())
    spider = COSCOParseTracking(message)
    data = spider.run_server()
    print(data)
    stop = int(time.time())
    print("程序总耗时：", stop - start, "秒")