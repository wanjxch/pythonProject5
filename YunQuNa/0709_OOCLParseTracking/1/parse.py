# -*- coding: utf-8 -*-
# @Time : ${DATE} ${TIME}
# @Author : housongcheng
# @Email : housongcheng@yunquna.com
# @File : ${NAME}.py
# @Software: ${PRODUCT_NAME}
# @Desc : OOCL tracking

import json
from parses.BaseParse import BaseParse


class OOCLParseTracking(BaseParse):
    event_type = 'OOCLParseTracking'

    def parse(self, response):

        if not response:
            yield {'ms_type': 'data', 'data': {}}
        info = json.loads(response)

        if not info.get('data'):  # 判断此处为空list
            yield {'ms_type': 'data', 'data': {}}
        for container in info.get('data'):
            if not container.get('data'):
                yield {'ms_type': 'data', 'data': {}}
            else:
                yield {'ms_type': 'data', 'data': container.get('data')}