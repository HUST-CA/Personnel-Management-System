import hashlib

test_values = {
    'method': 'taobao.item.seller.get',
    'app_key': '12345678',
    'session': 'test',
    'timestamp': '2016-01-01 12:00:00',
    'format': 'json',
    'v': '2.0',
    'sign_method': 'md5',
    'fields': 'num_iid,title,nick,price,num',
    'num_iid': '11223344',
}

test_secret = 'helloworld'


def calc_sign(values, secret):
    li_k_v = []
    for k, v in values.items():
        li_k_v.append((k, v))
    string = ''
    li_k_v.sort()
    for each in li_k_v:
        string += each[0]
        string += each[1]
    string = secret + string + secret
    encoded_string = string.encode('utf-8')
    md5 = hashlib.md5()
    md5.update(encoded_string)
    sign = md5.hexdigest().upper()
    values['sign'] = sign
    return sign


if __name__ == '__main__':
    calc_sign(test_values, test_secret)
