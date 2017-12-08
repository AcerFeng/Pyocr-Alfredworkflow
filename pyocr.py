# -*- coding: utf-8 -*-
from workflow import web
import sys
import os
import base64

reload(sys)
sys.setdefaultencoding('utf-8')

def get_access_token():
    api_key = os.environ['bce_api_key']
    api_secret = os.environ['bce_api_secret']
    resp = web.post('https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s' %
                    (api_key, api_secret),).json()
    return resp['access_token']

def url_parse(url=''):
    result = web.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                      params={
                          'access_token': get_access_token(),
                      },
                      data={
                          'url': url,
                      }).json()
    output(result)

def screenshots_parse(path=''):
    with open(path, 'rb') as img:
        image_data = img.read()
        base64_data = base64.b64encode(image_data)

    if len(base64_data) > 4 * 1024 * 1024:
        sys.stdout.write('图片必须小于4M')
        return

    result = web.post('https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic',
                      params={
                          'access_token': get_access_token(),
                      },
                      data={
                          'image': base64_data,
                      }).json()

    output(result)

def output(result=None):
    if not result:
        sys.stdout.write('解析失败')
        return

    resultStr = ''
    for item in result['words_result']:
        resultStr += item['words'] + '\n'

    sys.stdout.write(resultStr)

def main():
    query = sys.argv[1]
    if len(query) < 5:
        sys.stdout.write('请检查路径')
        return

    if query[0:4] == 'http':
        url_parse(query)
    elif query[-4:] == '.png' or query[-4:] == '.jpg':
        screenshots_parse(query)
    else:
        sys.stdout.write('不支持的图片类型')

if __name__ == '__main__':
    main()
