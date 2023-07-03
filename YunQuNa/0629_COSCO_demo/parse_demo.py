# -*- coding: utf-8 -*-
# @Time : ${DATE} ${TIME}
# @Author : housongcheng
# @Email : housongcheng@yunquna.com
# @File : ${NAME}.py
# @Software: ${PRODUCT_NAME}
# @Desc : OOCL tracking

import json
from COSCO_DMEO import Message
from COSCO_DMEO import COSCOParseTracking



class OOCLParseTracking():
    event_type = 'OOCLParseTracking'

    def parse(self, response):
        if not response:
            yield {'ms_type': 'data', 'data': {}}
        info = json.loads(response)

        if not info.get('data'):  # 判断此处为空list
            yield {'ms_type': 'data', 'data': {}}
        for container in info.get('data'):
            if not container:
                yield {'ms_type': 'data', 'data': {}}
            else:
                yield {'ms_type': 'data', 'data': container}


if __name__ == '__main__':
    message = {"blNo": "COSU6357693840", "carrierCode": "COSCO", "carrierId": 4528, "realTime": 0, "taskId": 6742985,
               "traceId": "test", "type": "bl"}
    message = Message(message)
    spider = COSCOParseTracking(message)
    result = spider.run_server()
    OOCL = OOCLParseTracking()
    generator_data = OOCL.parse(result)
    for data in generator_data:
        print(data)
    # result_list = list(generator_data)
    # print(result_list)
