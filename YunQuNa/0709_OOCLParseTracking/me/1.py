# import random
#
# random_number = random.uniform(0.123456789123456, 0.123456789123457)
# print(random_number)

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


print(AES_Encryption(text='[{"x":13.436532507739939,"y":326,"timestamp":1688349638059},{"x":13.436532507739939,"y":326,"timestamp":1688349638066},{"x":13.436532507739939,"y":327,"timestamp":1688349638074},{"x":13.436532507739939,"y":327,"timestamp":1688349638082},{"x":13.436532507739939,"y":327,"timestamp":1688349638090},{"x":13.436532507739939,"y":327,"timestamp":1688349638098},{"x":16.31578947368421,"y":327,"timestamp":1688349638106},{"x":19.195046439628484,"y":327,"timestamp":1688349638114},{"x":23.993808049535605,"y":327,"timestamp":1688349638122},{"x":27.8328173374613,"y":327,"timestamp":1688349638130},{"x":32.63157894736842,"y":327,"timestamp":1688349638138},{"x":38.39009287925697,"y":327,"timestamp":1688349638146},{"x":42.22910216718266,"y":327,"timestamp":1688349638154},{"x":46.06811145510836,"y":327,"timestamp":1688349638162},{"x":49.907120743034056,"y":327,"timestamp":1688349638170},{"x":53.746130030959755,"y":327,"timestamp":1688349638179},{"x":56.62538699690403,"y":327,"timestamp":1688349638186},{"x":58.54489164086687,"y":327,"timestamp":1688349638195},{"x":61.424148606811144,"y":327,"timestamp":1688349638202},{"x":63.343653250774,"y":327,"timestamp":1688349638210},{"x":65.26315789473684,"y":327,"timestamp":1688349638218},{"x":67.18266253869969,"y":327,"timestamp":1688349638226},{"x":69.10216718266254,"y":327,"timestamp":1688349638234},{"x":72.94117647058823,"y":328,"timestamp":1688349638242},{"x":75.82043343653251,"y":328,"timestamp":1688349638250},{"x":80.61919504643963,"y":328,"timestamp":1688349638258},{"x":83.49845201238391,"y":328,"timestamp":1688349638266},{"x":87.3374613003096,"y":328,"timestamp":1688349638274},{"x":91.17647058823529,"y":328,"timestamp":1688349638282},{"x":95.015479876161,"y":328,"timestamp":1688349638290},{"x":99.81424148606811,"y":328,"timestamp":1688349638298},{"x":103.6532507739938,"y":328,"timestamp":1688349638306},{"x":107.49226006191951,"y":328,"timestamp":1688349638314},{"x":112.29102167182663,"y":328,"timestamp":1688349638322},{"x":119.96904024767802,"y":328,"timestamp":1688349638330},{"x":129.56656346749227,"y":328,"timestamp":1688349638338},{"x":136.28482972136223,"y":328,"timestamp":1688349638346},{"x":143.9628482972136,"y":329,"timestamp":1688349638354},{"x":148.76160990712074,"y":329,"timestamp":1688349638362},{"x":155.4798761609907,"y":329,"timestamp":1688349638370},{"x":162.19814241486068,"y":329,"timestamp":1688349638378},{"x":166.99690402476782,"y":329,"timestamp":1688349638386},{"x":170.8359133126935,"y":329,"timestamp":1688349638395},{"x":176.59442724458205,"y":328,"timestamp":1688349638402},{"x":180.43343653250773,"y":328,"timestamp":1688349638410},{"x":181.39318885448915,"y":328,"timestamp":1688349638418},{"x":183.312693498452,"y":328,"timestamp":1688349638426},{"x":186.19195046439629,"y":327,"timestamp":1688349638434},{"x":187.1517027863777,"y":327,"timestamp":1688349638458},{"x":188.11145510835914,"y":327,"timestamp":1688349638491},{"x":188.11145510835914,"y":326,"timestamp":1688349638498},{"x":189.07120743034056,"y":326,"timestamp":1688349638579}]', secret_key="47m21jpLQnDu6AXF"))