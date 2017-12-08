# -*- coding: utf-8 -*-
import sys
from PIL import Image
import zbarlight

reload(sys)
sys.setdefaultencoding('utf-8')

def main():
    query = sys.argv[1]
    if len(query) < 5:
        sys.stdout.write('请检查路径')
        return
    
    if query[-4:] != '.png' and query[-4:] != '.jpg':
        sys.stdout.write('不支持的图片类型')
        return
    
    with open(query, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()

    codes = zbarlight.scan_codes('qrcode', image)
    codesStr = ''
    for code in codes:
        codesStr += code + '\n'
    sys.stdout.write(codesStr)

if __name__ == '__main__':
    main()