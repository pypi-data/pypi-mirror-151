import requests


def wx_send(token, text, desp):
    '''
    发送信息到微信(虾推啥)
    :param text:
    :param desp: 支持html格式
    :return:
    '''
    mydata = {
        'text': text,
        'desp': desp
    }

    resp = requests.post('http://wx.xtuis.cn/%s.send' % token, data=mydata)
    return resp
