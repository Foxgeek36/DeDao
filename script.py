# coding=utf-8
import json
import pymongo
from mitmproxy import ctx

# attention mongodb settings +--
client = pymongo.MongoClient('localhost')
db = client['dedao']
collection = db['books']
# ----------------------


def response(flow):
    '''
    使用mitmproxy获取dedao_app数据接口信息的测试操作
    :param flow: HTTPflow对象
    :return:
    '''
    global collection
    # 精简之后的数据接口url
    url = 'https://dedao.igetget.com/v3/discover/bookList'
    if flow.request.url.startswith(url):
        text = flow.response.text
        data = json.loads(text)
        books = data.get('c').get('list')
        for book in books:
            data = {
                'title': book.get('operating_title'),
                'cover': book.get('cover'),
                'summary': book.get('other_share_summary'),
                'price': book.get('price')
            }
            # attention the log setting +--
            ctx.log.info(str(data))
            collection.insert(data)
