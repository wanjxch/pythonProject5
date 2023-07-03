# -*- coding: utf-8 -*-

import json
import time

import requests
import re



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
    return bill_item

def container_info_item():
    contaienr_item = dict()
    contaienr_item["container_no"] = ""
    contaienr_item["seal_no"] = ""
    contaienr_item["bl_no"] = ""
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


def date_to_format_data(orign_datetime_string):
    """ 2018-11-03 22:24 转化为 2018-11-03 22:24:00 """
    if orign_datetime_string:
        datetime_string = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}', orign_datetime_string)
        struct_time = time.strptime(datetime_string[0], '%Y-%m-%d %H:%M')
        datetime_string = time.strftime('%Y-%m-%d %H:%M:%S', struct_time)
        return datetime_string    #
    else:
        return None
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



def format_date(date_string):
    """ 时间格式标准化 """
    import re
    import time
    if not date_string:    # 31-Oct-2019 11:46
        return None
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
        return None




def clean_top(original_str, head):
    """ 去除提单号前缀 """
    matchs = re.findall(r'(?<={})[\s\S]+'.format(head), original_str, re.S)
    if matchs:
        return matchs[0]
    else:
        return original_str

class JDParseTracking(object):
    def __init__(self,message):
        # 初始化参数
        self.message = message
        self.busi_data = self.message.get_business_data()
        self.taskId = message.get_common_data_task_id()
        self.session = requests.Session()

        self.bl_no = self.busi_data.get('blNo')
        self.real_bl = clean_top(self.bl_no, 'ONEY')
        # self.session.proxies ={'http': 'http://QRKJDUOBEIE5HHT2MK9:7qRfvj0O@http-proxy-t1.dobel.cn:9180', 'https': 'http://QRKJDUOBEIE5HHT2MK9:7qRfvj0O@http-proxy-t1.dobel.cn:9180'}


    @staticmethod
    def extract_first(values):
        for value in values:
            if value is not None or value != '':
                return value.strip()


    def get_pol_pod(self,form_data):
        headers = {
            'authority': 'esvc.djship.co.kr',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4621.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'origin': 'http://esvc.djship.co.kr/gnoss/CUP_HOM_3301GS.do',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'http://esvc.djship.co.kr/gnoss/CUP_HOM_3301GS.do?redir=Y&sessLocale=en',
            'accept-language': 'zh-CN,zh;q=0.9',
        }

        for i in range(5):
            try:
                response = self.session.post('http://esvc.djship.co.kr/gnoss/CUP_HOM_3301GS.do', headers=headers,
                                             data=form_data,
                                             timeout=30)
                return response
            except Exception as e:
                if i == 4:
                    raise e
                continue
    def get_containt(self,info):
        container_lists = info.get('list')
        #空数据时
        if not container_lists:
            return []

        form_data = {
            'f_cmd': '124',
            'bkg_no': self.real_bl,

        }
        response = self.get_pol_pod(form_data)

        pot_datas = response.json()['list']

        pot_count = len(pot_datas)

        pol_pot_pod_list = []
        vessel_Name = ''
        vo_yage = ''
        if pot_count > 1:
            for index, pot_data in enumerate(pot_datas):
                index += 1
                if index == 1:
                    etdFlag = pot_data['etdFlag']
                    if etdFlag == 'A':
                        atd = pot_data['etd']
                        etd = ''
                    else:
                        atd = ''
                        etd = pot_data['etd']



                    vesselName = pot_data.get('vslEngNm')
                    if pot_data.get('skdVoyNo') and pot_data.get('skdDirCd'):
                        voyage = pot_data.get('skdVoyNo') + pot_data.get('skdDirCd')
                    else:
                        voyage = ''
                    vessel_Name = vesselName
                    vo_yage = voyage
                    pol = pot_data.get('polNm')
                    pod = pot_data.get('podNm')
                    pol_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pol,
                        "event_name": "Departure_POL",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    pol_pot_pod_list.append(pol_data)
                    etaFlag = pot_data['etaFlag']
                    if etaFlag == 'A':
                        pot_ata = pot_data['eta']
                        pot_eta = ''
                    else:
                        pot_ata = ''
                        pot_eta = pot_data['eta']
                    potl_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pod,
                        "event_name": "Berth_Transit",
                        "a_time": pot_ata,
                        "e_time": pot_eta,
                    }

                    pol_pot_pod_list.append(potl_data)


                elif index == pot_count:
                    etdFlag = pot_data['etdFlag']
                    if etdFlag == 'A':
                        atd = pot_data['etd']
                        etd = ''
                    else:
                        atd = ''
                        etd = pot_data['etd']




                    vesselName = pot_data.get('vslEngNm')
                    if pot_data.get('skdVoyNo') and pot_data.get('skdDirCd'):
                        voyage = pot_data.get('skdVoyNo') + pot_data.get('skdDirCd')
                    else:
                        voyage = ''
                    pol = pot_data.get('polNm')
                    pod = pot_data.get('podNm')
                    pod_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pol,
                        "event_name": "Departure_Transit",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    pol_pot_pod_list.append(pod_data)
                    etaFlag = pot_data['etaFlag']
                    if etaFlag == 'A':
                        pot_ata = pot_data['eta']
                        pot_eta = ''
                    else:
                        pot_ata = ''
                        pot_eta = pot_data['eta']
                    potd_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pod,
                        "event_name": "Berth_POD",
                        "a_time": pot_ata,
                        "e_time": pot_eta,
                    }
                    pol_pot_pod_list.append(potd_data)
                else:
                    etdFlag = pot_data['etdFlag']
                    if etdFlag == 'A':
                        atd = pot_data['etd']
                        etd = ''
                    else:
                        atd = ''
                        etd = pot_data['etd']




                    vesselName = pot_data.get('vslEngNm')
                    if pot_data.get('skdVoyNo') and pot_data.get('skdDirCd'):
                        voyage = pot_data.get('skdVoyNo') + pot_data.get('skdDirCd')
                    else:
                        voyage = ''
                    pol = pot_data.get('polNm')
                    pod = pot_data.get('podNm')

                    potl_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pol,
                        "event_name": "Berth_Transit",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    pol_pot_pod_list.append(potl_data)
                    etaFlag = pot_data['etaFlag']
                    if etaFlag == 'A':
                        pot_ata = pot_data['eta']
                        pot_eta = ''
                    else:
                        pot_ata = ''
                        pot_eta = pot_data['eta']
                    potd_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pod,
                        "event_name": "Departure_Transit",
                        "a_time": pot_ata,
                        "e_time": pot_eta,
                    }

                    pol_pot_pod_list.append(potd_data)

        else:
            for index, pot_data in enumerate(pot_datas):
                index += 1
                if index == 1:
                    etdFlag = pot_data['etdFlag']
                    if etdFlag == 'A':
                        atd = pot_data['etd']
                        etd = ''
                    else:
                        atd = ''
                        etd = pot_data['etd']



                    vesselName = pot_data.get('vslEngNm')
                    if pot_data.get('skdVoyNo') and pot_data.get('skdDirCd'):
                        voyage = pot_data.get('skdVoyNo') + pot_data.get('skdDirCd')
                    else:
                        voyage = ''
                    vessel_Name = vesselName
                    vo_yage = voyage
                    pol = pot_data.get('polNm')
                    pod = pot_data.get('podNm')
                    pol_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pol,
                        "event_name": "Departure_POL",
                        "a_time": atd,
                        "e_time": etd,
                    }
                    pol_pot_pod_list.append(pol_data)
                    etaFlag = pot_data['etaFlag']
                    if etaFlag == 'A':
                        pot_ata = pot_data['eta']
                        pot_eta = ''
                    else:
                        pot_ata = ''
                        pot_eta = pot_data['eta']
                    potd_data = {
                        "vessel_name": vesselName,
                        "voyage": voyage,
                        "location_name": pod,
                        "event_name": "Berth_POD",
                        "a_time": pot_ata,
                        "e_time": pot_eta,
                    }
                    pol_pot_pod_list.append(potd_data)




        contaienr_count = len(container_lists)
        result_list = []
        for index, container in enumerate(container_lists):
            cntr_no = container.get('cntrNo')
            cop_no = container.get('copNo')
            # 添加起运港,目的港等信息
            form_data = {
                'f_cmd': '128',
                'cntr_no': cntr_no,
                'bkg_no': self.real_bl,
                'cop_no': cop_no,
            }
            response = self.get_pol_pod(form_data)
            data_info = response.json()

            bl_data_list = data_info.get('list')
            if not bl_data_list:
                return []
            bill_item = bill_info_item()
            bill_item['bl_no'] = self.bl_no
            bill_item['carrier_code'] = self.busi_data.get('carrierCode')
            bill_item['carrier_id'] = self.busi_data.get('carrierId')
            bill_item['task_id'] = self.taskId
            bill_item['request_url'] = response.url
            bill_item['vessel_name'] = vessel_Name
            bill_item['voyage'] = vo_yage
            for bl_data in bl_data_list:
                bill_item['depart'] = bl_data.get('firstNod')
                bill_item['arrive'] = bl_data.get('lastNod')
                bill_item['load'] = bl_data.get('firstNod')
                bill_item['discharge'] = bl_data.get('lastNod')
            bill_item['container_count'] = contaienr_count


            container_item = container_info_item()
            cntr_no = container.get('cntrNo')
            cop_no = container.get('copNo')
            container_item['container_no'] = cntr_no
            container_item['bl_no'] = self.real_bl
            container_item['seal_no'] = container.get('sealNo')
            container_item['container_weight'] = container.get('weight')
            if "'" in container.get('cntrTpszNm'):
                container_size_type = container.get('cntrTpszNm').split("'")
                container_size = container_size_type[0]
                container_type = container_size_type[1]
                container_item['container_size'] = container_size
                container_item['container_type'] = container_type
            elif "." in container.get('cntrTpszNm'):
                container_size_type = container.get('cntrTpszNm').split(".")
                container_size = container_size_type[0]
                container_type = container_size_type[1]
                container_item['container_size'] = container_size
                container_item['container_type'] = container_type
            container_item['latest_location'] = container.get('yardNm')
            container_item['latest_location_date'] = container.get('eventDt')
            container_item['latest_event_name'] = container.get('statusNm')
            container_item['event_list'] = list()


            form_data = {
                'f_cmd': '125',
                'cntr_no': cntr_no,
                'bkg_no': self.real_bl,
                'cop_no': cop_no,
            }
            response = self.get_pol_pod(form_data)
            try:
                container_all_event_details = json.loads(response.text)
            except:
                return {}


            for container_per_event_detail in container_all_event_details.get('list'):
                event = tracking_event_item()
                status_um = container_per_event_detail.get('statusNm')
                event['event_name'] = status_um
                if status_um and "(" in status_um:
                    event_name = clean_str(
                        status_um.replace(re.findall(r'(\(.*?\))', status_um, re.S)[0], "").replace("  ", " "))
                    event['event_name'] = event_name
                    vvd = container_per_event_detail.get('vvd')
                    if vvd:
                        vessel_voyage = vvd.split(' ')
                        voyage = vessel_voyage[-1]
                        vessel_voyage.remove(voyage)
                        vessel = ' '.join(vessel_voyage)
                        event['vessel_name'] = clean_str(vessel)
                        event['voyage'] = clean_str(voyage)
                else:
                    vvd = container_per_event_detail.get('vvd')
                    if vvd:
                        vessel_voyage = vvd.split(' ')
                        voyage = vessel_voyage[-1]
                        vessel_voyage.remove(voyage)
                        vessel = ' '.join(vessel_voyage)
                        event['vessel_name'] = clean_str(vessel)
                        event['voyage'] = clean_str(voyage)

                if re.findall(r"('.*')", status_um):
                    status_vessel_voyage = re.findall("('.*?')", status_um)
                    vessel_voyage = eval(status_vessel_voyage[0]).split(' ')
                    voyage = vessel_voyage[-1]
                    vessel_voyage.remove(voyage)
                    vessel = ' '.join(vessel_voyage)
                    event_name = status_um.replace(status_vessel_voyage[0], '')
                    event['event_name'] = clean_str(event_name)  # 将事件描述的船名航次删除
                    event['vessel_name'] = clean_str(vessel)
                    event['voyage'] = clean_str(voyage)
                    event['transport_mode'] = 'Vessel'
                else:
                    event['transport_mode'] = 'Truck'
                event_date = container_per_event_detail.get('eventDt')
                event_date_act_or_exp = container_per_event_detail.get('actTpCd')  # 事件发生的时间是实际还是预计

                if event_date and event_date_act_or_exp == 'A':
                    event['a_time'] = date_to_format_data(event_date)
                elif event_date and event_date_act_or_exp == 'E':
                    event['e_time'] = date_to_format_data(event_date)
                # 事件位置
                event['location_name'] = container_per_event_detail.get('placeNm')
                container_item['event_list'].append(event)
            if pol_pot_pod_list:
                for pot in pol_pot_pod_list:
                    container_item['event_list'].append(
                        pot
                    )

            result_list.append(return_tracking_info(receive_task_message=self.busi_data,bill_item=bill_item,container_info=container_item))
        return result_list

    def get_bl_data(self):
        headers = {
            'authority': 'esvc.djship.co.kr',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua': '"Chromium";v="21", " Not;A Brand";v="99"',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4621.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'http://esvc.djship.co.kr/gnoss/CUP_HOM_3301GS.do?redir=Y&sessLocale=en',
            'accept-language': 'zh-CN,zh;q=0.9',
            }
        request_time = str(int(time.time() * 1000))

        params = {
            '_search': 'false',
            'nd': request_time,
            'rows': '10000',
            'page': '1',
            'sidx': '',
            'sord': 'asc',
            'f_cmd': '121',
            'search_type': 'B',
            'search_name': self.real_bl,
            'cust_cd': '',
        }
        for i in range(5):
            try:
                response = self.session.get('http://esvc.djship.co.kr/gnoss/CUP_HOM_3301GS.do', params=params, headers=headers,timeout=30)
                info = response.json()
                return info
            except Exception as e:
                if i == 4:
                    raise e
                continue

    def run(self):
        info = self.get_bl_data()
        if not info:
            return {}

        data = self.get_containt(info)

        return data


    def run_server(self):

        data = self.run()
        if data:
            result = {"status": "success","message":"success" ,"data": data}
        else:
            result = {"status": "success", "message":"fail" ,"data": ""}
        return json.dumps(result, ensure_ascii=False)

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

            return {"agentDomain": "http-proxy-t1.dobel.cn:9180", "agentAccount": "QRKJDUOBEIE5HH9MMK0",
                    "agentToken": "BvOU6RLG", "agentId": 19}

        def to_dict(self):
            return {}

    message = {"blNo":"DJSCTXG220010159","carrierCode":"JD","carrierId":"4540","realTime":"0","taskId":"3826624","traceId":"43002-c0a8bb5f-449722-21487","type":"bl"}
    # message = {"blNo": "026A519005", "carrierCode": "WHL", "carrierId": 4575, "realTime": 0, "taskId": 2042864, "traceId": "30015-c0a80ccb-446025-10311", "type": "bl"}
    message = Message(message)
    spider = JDParseTracking(message)
    data = spider.run_server()
    print(data)