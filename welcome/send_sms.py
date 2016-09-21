import urllib.request, urllib.parse
from urllib.error import URLError, HTTPError

defalt_url = 'http://gw.api.taobao.com/router/rest'
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
    'sign': '66987cb115214e59e6ec978214934fb8'
}
test_secret = 'helloworld'


def send_sms(url, values):
    url_values = urllib.parse.urlencode(values).encode(encoding='UTF8')
    full_url = urllib.request.Request(url, url_values)
    full_url.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=utf-8')
    try:
        response = urllib.request.urlopen(full_url)
    except HTTPError as e:
        print('Error code:', e.code)
    except URLError as e:
        print('Reason', e.reason)
    the_page = response.read()
    print(the_page)


if __name__ == '__main__':
    send_sms(defalt_url, test_values)
