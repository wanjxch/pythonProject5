import json
from parses.BaseParse import BaseParse


class COSCOParseTracking(BaseParse):
    event_type = 'COSCOParseTracking'

    def parse(self, response):
        return_data = json.loads(response)
        data = return_data.get('data')
        if data:
            for i in data:
                yield {'ms_type': 'data', 'data': i}
        else:
            yield {'ms_type': 'data', 'data': {}}