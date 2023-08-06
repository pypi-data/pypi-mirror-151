import pandas as pd
from pandas import DataFrame
import logging
import os
import numpy as np


def code_process(codes, add_market=False):
    '''
    处理股票代码
    :param codes:
    :param add_market:
    :return:
    '''

    def transform(code, add_market):
        if isinstance(code, int) or isinstance(code, float):
            code = str(int(code))
        code = code.zfill(6)
        if add_market:
            if code[0:1] == '6':
                code += '.SH'
            elif code[0:1] == '0' or code[0:1] == '3':
                code += '.SZ'
        return code

    if isinstance(codes, int) or isinstance(codes, float) or isinstance(codes, str):
        return transform(codes, add_market)
    elif isinstance(codes, list):
        return [transform(x, add_market) for x in codes]
    elif isinstance(codes, DataFrame):
        codes['code'] = codes['code'].apply(lambda x: transform(x, add_market))
        return codes


def init(log_file):
    '''
    初始化日志
    :param log_file:
    :return:
    '''
    LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"  # 日志格式化输出
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S %p"  # 日期格式
    if not os.path.exists('log'):
        os.mkdir('./log')
    fp = logging.FileHandler('log/%s' % log_file, encoding='utf-8')
    fs = logging.StreamHandler()
    params = {'level': logging.INFO, 'format': LOG_FORMAT, 'datefmt': DATE_FORMAT, 'handlers': [fp, fs]}
    logging.basicConfig(**params)  # 调用


def get_trade_days():
    '''
    获取交易日列表，trade_dates.txt会不定期更新
    :return:
    '''
    file_dir = os.path.dirname(os.path.abspath(__file__))
    data = np.loadtxt(os.path.join(file_dir, 'trade_dates.txt'), dtype=str).tolist()
    return data


def is_trade_day(date):
    '''
    判断是否交易日
    :param date:
    :return:
    '''
    trade_dates = get_trade_days()
    date = str(date).replace('/', '').replace('-', '')
    return date in trade_dates


def get_trade_day(date, offset):
    '''
    交易日前推或者后推
    :param date:
    :param offset:
    :return:
    '''
    trade_dates = get_trade_days()
    date = str(date).replace('/', '').replace('-', '')
    if date not in trade_dates:
        return -1
    index = trade_dates.index(date)
    if index + offset < 0 or index + offset >= len(trade_dates):
        return None
    return trade_dates[index + offset]


if __name__ == '__main__':
    # print(get_trade_days())
    print(get_trade_day('20220521', 3))
