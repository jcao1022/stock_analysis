from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import traceback
import sys
import os
import json
import re
import sqlite3
import sqlalchemy
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import xlwt
from datetime import datetime
import traceback
# from pandas import DataFrame, Series
# import numpy as np
# import  pandas as pd

# db_connection = sqlite3.connect('stock.db')
# db_connection.execute('CREATE  TABLE  table_name(line_name text)')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///my_stock.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
from sqlalchemy import Column, Integer, String, Float, DateTime, Date


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    code = Column(String(60))
    date = Column(DateTime)
    #股价
    price = Column(String(20) )
    #股价变化
    stock_change = Column(String(60) )
    # 成交量
    turnover = Column(String(60) )
    #换手率
    change_hands = Column(String(60) )
    #成交额
    volume_of_transaction = Column(String(60) )
    #量比
    quantity_relative_ratio = Column(String(60) )
    #总市值
    total_value = Column(String(60) )
    #振幅
    amplitude = Column(String(60) )
    #委比
    weibi = Column(String(60) )
    #流通值
    circulation_value = Column(String(60) )
    #市盈率动态
    pe_dynamic = Column(String(60) )
    #市盈率TTM
    pe_ttm = Column(String(60) )
    #每股收益
    earnings_per_share = Column(String(60) )
    #股息
    dividend_ttm = Column(String(60) )
    #市盈率静态
    pe_static = Column(String(60) )
    #市净率
    pb = Column(String(60) )
    # 每股净资产
    net_asset_value_per_share = Column(String(60) )
    # 盈利情况
    profitable = Column(String(60) )
    #营业收入
    operation_revenue = Column(String(60) )
    #营业收入同比增长
    operating_income_increased_y_on_y = Column(String(60) )
    #净利润
    net_profits = Column(String(60) )
    # 净利润同比增长
    net_profit_growth = Column(String(60) )
    # 扣非净利润
    non_net_profit_withheld = Column(String(60) )
    #扣非净利润同比增长
    non_net_profit_growth_y_on_y = Column(String(60) )
    # # 每股收益
    # earnings_per_share = Column(String(60) )
    #每股净资产
    # net_asset_value_per_share = Column(String(60) )
    #每股资本公积金
    capital_reserve_per_share = Column(String(60) )
    #每股未分配利润
    undistributed_profit_per_share = Column(String(60) )
    # 每股经营现金流
    operating_cash_flow_per_share= Column(String(60) )
    # 净资产收益率
    net_assets_income_rate= Column(String(60) )
    # 净资产收益率-摊薄
    return_on_equity_diluted= Column(String(60) )
    # 总资产报酬率\
    rate_of_return_on_total_assets= Column(String(60) )
    # 人力投入回报率 \
    rate_of_return_on_manpower_input= Column(String(60) )
    # 销售毛利率 \
    gross_margin= Column(String(60) )
    # 销售净利率 \
    net_profit_margin_on_sales= Column(String(60) )
    # 资产负债率 \
    debt_to_assets_ratio= Column(String(60) )
    # 流动比率 \
    liquidity_ratio= Column(String(60) )
    # '速动比率' \
    quick_ratio= Column(String(60) )
    #权益乘数
    equity_multiplier= Column(String(60) )
    #产权比率
    equity_ratio= Column(String(60) )
    # 股东权益比率
    investor_ratio= Column(String(60) )
    # 现金流量比率
    cash_flow_ratio= Column(String(60) )
    # 存货周转天数
    days_sales_of_inventory= Column(String(60) )
    # 应收账款周转天数
    days_sales_outstanding= Column(String(60) )
    # 应付账款周转天数
    days_of_turnover_of_accounts_payable= Column(String(60) )
    # 现金循环周期
    cash_cycle= Column(String(60) )
    # 营业周期
    operating_cycle= Column(String(60) )
    # 总资产周转率
    total_assets_turnover= Column(String(60) )
    # 存货周转率
    inventory_turnover_ratio= Column(String(60) )
    # 应收账款周转率
    turnover_of_account_receivable= Column(String(60) )
    # 应付账款周转率
    turnover_ratio_of_account_payable= Column(String(60) )
    # 流动资产周转率
    velocity_of_liquid_assets= Column(String(60) )
    # 固定资产周转率
    turnover_of_fixed_assets= Column(String(60) )

    def __repr__(self):
        return f'<Stock {self.name}>'

# 创建表
Base.metadata.create_all(engine)

class SnowBall(object):
    # DRIVER = r'/usr/local/bin/phantomjs'
    DRIVER = r'phantomjs-2.1.1-windows\bin\phantomjs.exe'
    SERVICE_ARGS = ['--load-images=false', '--proxy-type=None', '--ignore-ssl-errors=true', '--ssl-protocol=tlsv1']
    USER_AGENTS = [
        # "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        # "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        # "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        # "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        # "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        # "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        # "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        # "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        # "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        # "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        # "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        # "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        # "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:57.0) Gecko/20100101 Firefox/57.0',
        # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
    ]
    DCAP = dict(webdriver.DesiredCapabilities.PHANTOMJS)
    DCAP["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
    TIMEOUT = 15
    data = dict()

    def __init__(self, url, browser='p'):
        if browser == 'p':
            self.driver = webdriver.PhantomJS(self.DRIVER, service_args=self.SERVICE_ARGS, desired_capabilities=self.DCAP)
        if browser == 'c':
            self.driver = webdriver.Chrome()
        self._get_source(url)

    def _get_source(self, url, sleep_time=2):
        self.driver.get(url)
        time.sleep(sleep_time)
        print('Driver: {}'.format(self.driver))
        print('Current URL: ' + self.driver.current_url)
        # return self.driver

    def _get_element(self, locator):
        print("Current Locator: {}".format(locator))
        print('Time out: {}'.format(self.TIMEOUT))
        WebDriverWait(self.driver, self.TIMEOUT).until(EC.presence_of_element_located((By.XPATH, locator)))
        return self.driver.find_element_by_xpath(locator)

    # def __del__(self):
        # self.close()

    def close(self):
        # self.driver.close()
        self.driver.quit()

    def get_codes(self, lable, filename):
        self.stock = {}
        self.codes = []
        self._get_element(lable).click()
        time.sleep(.5)
        while True:
            sh = '//*[@id="table_wrapper-table"]/tbody'
            self.stock = self._get_element(sh).text
            time.sleep(.5)
            lines = self.stock.splitlines()
            for i in lines:
                self.codes.append(re.search('\s(\d{6}\s)', i).group(0).strip())
            print("{} Stock numbers：{}".format(filename, len(set(self.codes))))
            if len(lines) < 20:
                break
            self.next_page()
        self.write_to_json(filename)
        return set(self.codes)

    def write_to_json(self, filename):
        with open(filename + '.json', 'w') as f:
            json.dump(self.codes, f)

    def next_page(self):
        next = '//*[@id="main-table_paginate"]/a[2]'
        self._get_element(next).click()
        time.sleep(.5)
    #基本信息
    def list2dict(self, listarg):
        dict_data = dict()
        for item in listarg:
            key, value = item.split('：')
            try:
                value = float(value[:-1]) if value.endswith('%') else float(value[1:]) if value.startswith(
                    ('+', '-')) else float(value)
            except ValueError:
                raise Exception('Failed to convert a list to Dict')
            dict_data[key] = value
        return dict_data

    def _get_stock_info(self, xpath):
        print("getting basic info")
        data = self._get_element(xpath).text
        return data

    def _click_link(self, xpath, wait=2):
        self._get_element(xpath).click() # 进入利润表
        time.sleep(wait)

    #basic info
    def basic_info(self, code):
        basic = '//*[@id="app"]/div[2]/div[2]/div[3]'
        dict_data = dict()
        data = self._get_stock_info(basic)
        dict_data['code'] = code
        dict_data['name'] = self._get_element('//*[@id="app"]/div[2]/div[2]/h1').text.split('(')[0]
        dict_data['price'] = data.splitlines()[0]
        dict_data['stock_change'] = data.splitlines()[1]
        # 成交量
        dict_data['turnover'] = re.search(r'成交量：(\S+)\s', data).group(1)
        # 换手
        dict_data['change_hands'] = re.search(r'换手：(\S+)\s', data).group(1)
        # 成交额
        dict_data['volume_of_transaction'] = re.search(r'成交额：(\S+)\s', data).group(1)
        # 量比
        dict_data['quantity_relative_ratio'] = re.search(r'量比：(\S+)\s', data).group(1)
        # 总市值
        dict_data['total_value'] = re.search(r'总市值：(\d+.?\d+万?亿?)', data).group(1)
        # 振幅
        dict_data['amplitude'] = re.search(r'振幅：(\S+)\s', data).group(1)
        # 委比
        dict_data['weibi'] = re.search(r'委比：(-?\d+.?\d+%)', data).group(1)
        # 流通值
        dict_data['circulation_value'] = re.search(r'流通值：(\d+.?\d+万?亿?)', data).group(1)
        # 市盈率(动)
        dict_data['pe_dynamic'] = re.search(r'市盈率\(动\)：(\S+)\s', data).group(1)
        # 市盈率(TTM)
        dict_data['pe_ttm'] = re.search(r'市盈率\(TTM\)：(\S+)\s', data).group(1)
        # 每股收益
        dict_data['earnings_per_share'] = re.search(r'每股收益：(\S+)\s', data).group(1)
        # 股息(TTM)
        dict_data['dividend_ttm'] = re.search(r'股息\(TTM\)：(\S+)\s', data).group(1)
        # 市盈率(静)
        dict_data['pe_static'] = re.search(r'市盈率\(静\)：(\S+)\s', data).group(1)
        # 市净率
        dict_data['pb'] = re.search(r'市净率：(\d+.?\d+)', data).group(1)
        # 每股净资产
        dict_data['net_asset_value_per_share'] = re.search(r'每股净资产：(\d+.?\d+)', data).group(1)
        # 盈利情况
        try:
            dict_data['profitable'] = re.search(r'盈利情况：(\S+)\s', data).group(1)
        except:
            dict_data['profitable'] = '--'
        print(dict_data)

        return dict_data

    def finance_data_proc(self, data):
        finance_data = dict()
        for i in range(3, 39, 6):
            finance_data[data[i]] = str([data[i + 1]][0] + "||" + [data[i + 2]][0] + "||" + [data[i + 3]][0] + "||" + [data[i + 4]][0])
            if data[i].__contains__('0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9'):
                raise Exception("Finance data is incorrect!")
        for i in range(40, 70, 6):
            finance_data[data[i]] = str([data[i + 1]][0] + "||" + [data[i + 2]][0] + "||" + [data[i + 3]][0] + "||" + [data[i + 4]][0])
            if data[i].__contains__('0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9'):
                raise Exception("Finance data is incorrect!")
        for i in range(71, 107, 6):
            finance_data[data[i]] = str([data[i + 1]][0] + "||" + [data[i + 2]][0] + "||" + [data[i + 3]][0] + "||" + [data[i + 4]][0])
            if data[i].__contains__('0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9'):
                raise Exception("Finance data is incorrect!")
        for i in range(108, 150, 6):
            finance_data[data[i]] = str([data[i + 1]][0] + "||" + [data[i + 2]][0] + "||" + [data[i + 3]][0] + "||" + [data[i + 4]][0])
            if data[i].__contains__('0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9'):
                raise Exception("Finance data is incorrect!")
        for i in range(151, 217, 6):
            finance_data[data[i]] = str([data[i + 1]][0] + "||" + [data[i + 2]][0] + "||" + [data[i + 3]][0] + "||" + [data[i + 4]][0])
            if data[i].__contains__('0' or '1' or '2' or '3' or '4' or '5' or '6' or '7' or '8' or '9'):
                raise Exception("Finance data is incorrect!")
        print(finance_data)
        return finance_data


    #财务信息
    def financial(self, code):
        print("getting finance info...")
        # self.driver.get_screenshot_as_file("after.png")
        table = '//*[@id="app"]/div[2]/div[2]/div/div[4]/div/table'
        self.driver.get_screenshot_as_file("after.png")
        data = self._get_element(table).text.splitlines()
        print(data)
        new_data = self.finance_data_proc(data)
        # print(new_data)
        return new_data


    #高层管理
    def management(self):
        print("getting management info")
        gc = '//*[@id="app"]/div[2]/div[2]/div/table'
        self.data['management'] = self._get_element(gc).text
        return self.data

class Excel(object):
    style_font_bold = xlwt.easyxf('font: name Times New Roman, color-index black, bold on', num_format_str='#,##0.00')
    style_font_normal = xlwt.easyxf('font: name Times New Roman, color-index black, bold off', num_format_str='#,##0.00')
    style_time = xlwt.easyxf(num_format_str='D-MMM-YY')

    def __init__(self):
        self.workbook = xlwt.Workbook()

    def add_sheet(self, name):
        self.sheet = self.workbook.add_sheet(name)
        return self.sheet

    def write_head(self, sheet):
        sheet.write(0, 0, '股票名称', self.style_font_bold)
        sheet.write(0, 1, '市值', self.style_font_bold)
        sheet.write(0, 2, '总股本', self.style_font_bold)
        sheet.write(0, 3, '当前价格', self.style_font_bold)
        sheet.write(0, 4, '网址', self.style_font_bold)
        sheet.write(0, 5, '动态市盈率', self.style_font_bold)
        sheet.write(0, 6, '静态市盈率', self.style_font_bold)
        sheet.write(0, 7, '市盈率', self.style_font_bold)
        sheet.write(0, 8, '每股收益', self.style_font_bold)
        sheet.write(0, 9, '每股净资产', self.style_font_bold)
        sheet.write(0, 10, '营业额增长率', self.style_font_bold)
        sheet.write(0, 11, '营业额持续增长', self.style_font_bold)
        sheet.write(0, 12, '利润增长率', self.style_font_bold)
        sheet.write(0, 13, '利润持续增长', self.style_font_bold)
        sheet.write(0, 14, '毛利率', self.style_font_bold)
        sheet.write(0, 15, '净利率', self.style_font_bold)
        sheet.write(0, 16, '资产负债率', self.style_font_bold)
        sheet.write(0, 17, '现金流比值', self.style_font_bold)
        sheet.write(0, 18, '现金循环周期', self.style_font_bold)
        sheet.write(0, 19, '存货周转天数', self.style_font_bold)
        sheet.write(0, 20, '总资产周转率', self.style_font_bold)
        sheet.write(0, 21, '净资产收益率', self.style_font_bold)
        sheet.write(0, 22, '估值系数', self.style_font_bold)

    def write_to_excel(self, sheet, data, index, if_write):
        if not if_write:
            return
        sheet.write(index, 0, data['name'], self.style_font_normal)
        sheet.write(index, 1, data['market_value'], self.style_font_normal)
        sheet.write(index, 2, data['total_equity'], self.style_font_normal)
        sheet.write(index, 3, data['current_price'], self.style_font_normal)
        sheet.write(index, 4, data['website'], self.style_font_normal)
        sheet.write(index, 5, data['PE_dynamic'], self.style_font_normal)
        sheet.write(index, 6, data['PE_static'], self.style_font_normal)
        sheet.write(index, 7, data['PE'], self.style_font_normal)
        sheet.write(index, 8, data['EPS'], self.style_font_normal)
        sheet.write(index, 9, data['BVPS'], self.style_font_normal)
        sheet.write(index, 10, data['continued_growth_rate_in_turnover'], self.style_font_normal)
        sheet.write(index, 11, data['continued_growth_rate_in_turnover_without_negative'], self.style_font_normal)
        sheet.write(index, 12, data['continued_growth_rate_in_profit'], self.style_font_normal)
        sheet.write(index, 13, data['continued_growth_rate_in_profit_without_negative'], self.style_font_normal)
        sheet.write(index, 14, data['gross_profit_margin'], self.style_font_normal)
        sheet.write(index, 15, data['net_profit_ratio'], self.style_font_normal)
        sheet.write(index, 16, data['DABR'], self.style_font_normal)
        sheet.write(index, 17, data['cash_flow_ratio'], self.style_font_normal)
        sheet.write(index, 18, data['cash_cycle'], self.style_font_normal)
        sheet.write(index, 19, data['inventory_turnover_days'], self.style_font_normal)
        sheet.write(index, 20, data['total_asset_turnover'], self.style_font_normal)
        sheet.write(index, 21, data['ROE'], self.style_font_normal)
        sheet.write(index, 22, data['value_coefficient'], self.style_font_normal)

    def save(self, filename):
        self.workbook.save(filename)

def list_sum(L):
    sum = 0
    continue_increase = True
    for i in L:
        if '%' in i:
            #i.replace('%', '')
            i = i[:-1]
            if '万' in i:
                i = i[:-1]
        if '万亿' in i:
            i = i[:-2] * 10000
        elif '亿' in i:
            i = i[:-1] * 10000
        elif '万' in i:
            i = i[:-1]
        elif '元' in i:
            i = i[:-1]
        elif '天' in i:
            i = i[:-1]
        elif '次' in i:
            i = i[:-1]
        if i == '-':
            i = 0
        elif float(i) < 0:
            continue_increase = False
        sum += float(i)
    return (sum, continue_increase)

def get_code_list(filename):
    for root, dirs, files in os.walk(os.path.dirname(__file__)):
        for file in files:
            if str(file) == filename:
                with open(filename) as f:
                    stock_codes = json.load(f)
    return stock_codes

def _stock_code(code):
        if code.startswith('30') or code.startswith('00'):
            stock_code = 'SZ' + str(code)
            return stock_code
        elif code.startswith('68') or code.startswith('60'):
            stock_code = 'SH' + str(code)
            return stock_code
        else:
            raise Exception("Stock Code was not correct!")

def main(stock_list):

    NOT_PROCSSED = []
    flag = 0
    if isinstance(stock_list, str) and len(stock_list) == 6:
        stock_list = list([stock_list])
        print(stock_list)
    for i in stock_list:
        stock_code = _stock_code(i)
        XQ = 'https://xueqiu.com/S/{}'.format(stock_code)
        CW = "https://xueqiu.com/snowman/S/{}/detail#/ZYCWZB".format(stock_code)
        glc = 'https://xueqiu.com/snowman/S/{}/detail#/GSGG'.format(stock_code)
        flag += 1
        print(XQ)
        print('There are/is {} left!'.format(len(stock_list) - flag))
        print("Driver init...")

        try:
            basic = SnowBall(XQ, 'p')
            print(XQ)
            basic_data = basic.basic_info(stock_code)
            basic.close()

            finance = SnowBall(CW, 'c')
            print(CW)
            financial_data = finance.financial(stock_code)
            finance.close()

            new_data_add_to_db = Stock(
                name = basic_data['name'],
                code = basic_data['code'],
                date = datetime.today(),
                price = basic_data['price'],
                # 股价变化
                stock_change = basic_data['stock_change'],
                # 成交量
                turnover = basic_data['turnover'],
                # 换手率
                change_hands = basic_data['change_hands'],
                # 成交额
                volume_of_transaction = basic_data['volume_of_transaction'],
                # 量比
                quantity_relative_ratio = basic_data['quantity_relative_ratio'],
                # 总市值
                total_value = basic_data['total_value'],
                # 振幅
                amplitude = basic_data['amplitude'],
                # 委比
                weibi = basic_data['weibi'],
                # 流通值
                circulation_value = basic_data['circulation_value'],
                # 市盈率动态
                pe_dynamic = basic_data['pe_dynamic'],
                # 市盈率TTM
                pe_ttm = basic_data['pe_ttm'],
                # 每股收益
                earnings_per_share = basic_data['earnings_per_share'],
                # 股息
                dividend_ttm = basic_data['dividend_ttm'],
                # 市盈率静态
                pe_static = basic_data['pe_static'],
                # 市净率
                pb = basic_data['pb'],
                # 每股净资产
                net_asset_value_per_share = basic_data['net_asset_value_per_share'],
                # 盈利情况
                profitable=basic_data['profitable'],
                # 营业收入
                operation_revenue = financial_data['营业收入'],
                # 营业收入同比增长
                operating_income_increased_y_on_y = financial_data['营业收入同比增长'],
                # 净利润
                net_profits = financial_data['净利润'],
                # 净利润同比增长
                net_profit_growth = financial_data['净利润同比增长'],
                # 扣非净利润
                non_net_profit_withheld = financial_data['扣非净利润'],
                # 扣非净利润同比增长
                non_net_profit_growth_y_on_y = financial_data['扣非净利润同比增长'],
                # # 每股收益
                # earnings_per_share = financial_data['每股收益'],
                # 每股净资产
                # net_asset_value_per_share = financial_data['每股净资产'],
                # 每股资本公积金
                capital_reserve_per_share = financial_data['每股资本公积金'],
                # 每股未分配利润
                undistributed_profit_per_share = financial_data['每股未分配利润'],
                # 每股经营现金流
                operating_cash_flow_per_share = financial_data['每股经营现金流'],
                # 净资产收益率
                net_assets_income_rate = financial_data['净资产收益率'],
                # 净资产收益率-摊薄
                return_on_equity_diluted = financial_data['净资产收益率-摊薄'],
                # 总资产报酬率\
                rate_of_return_on_total_assets = financial_data['总资产报酬率'],
                # 人力投入回报率 \
                rate_of_return_on_manpower_input = financial_data['人力投入回报率'],
                # 销售毛利率 \
                gross_margin = financial_data['销售毛利率'],
                # 销售净利率 \
                net_profit_margin_on_sales = financial_data['销售净利率'],
                # 资产负债率 \
                debt_to_assets_ratio = financial_data['资产负债率'],
                # 流动比率 \
                liquidity_ratio = financial_data['流动比率'],
                # '速动比率' \
                quick_ratio = financial_data['速动比率'],
                # 权益乘数
                equity_multiplier = financial_data['权益乘数'],
                # 产权比率
                equity_ratio = financial_data['产权比率'],
                # 股东权益比率
                investor_ratio = financial_data['股东权益比率'],
                # 现金流量比率
                cash_flow_ratio = financial_data['现金流量比率'],
                # 存货周转天数
                days_sales_of_inventory = financial_data['存货周转天数'],
                # 应收账款周转天数
                days_sales_outstanding = financial_data['应收账款周转天数'],
                # 应付账款周转天数
                days_of_turnover_of_accounts_payable = financial_data['应付账款周转天数'],
                # 现金循环周期
                cash_cycle = financial_data['现金循环周期'],
                # 营业周期
                operating_cycle = financial_data['营业周期'],
                # 总资产周转率
                total_assets_turnover = financial_data['总资产周转率'],
                # 存货周转率
                inventory_turnover_ratio = financial_data['存货周转率'],
                # 应收账款周转率
                turnover_of_account_receivable = financial_data['应收账款周转率'],
                # 应付账款周转率
                turnover_ratio_of_account_payable = financial_data['应付账款周转率'],
                # 流动资产周转率
                velocity_of_liquid_assets = financial_data['流动资产周转率'],
                # 固定资产周转率
                turnover_of_fixed_assets = financial_data['固定资产周转率'],
            )
            session.add(new_data_add_to_db)
            session.commit()

        except Exception as e:
            print(e)
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_tb(exc_obj)
            NOT_PROCSSED.append(i)
            continue



if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore')

    # my_list = ['688981', '300783', '000725', '600588', '300454', '002415', '000333', '300327',
    #            '002352', '002262', '002422', '300750', '603160', '002223', '300206', '300003',
    #            '002007', '603986', '002157', '688096', '002507', '603288', '688310', '688036',
    #            '000541', '601318', '688033', '688015', '688399', '688199', '688169', '688599',
    #            '688298', '688128', '688099', '688186', '688288', '688178', '688256', '688379',
    #            '688101', '688466', '688196', '002980', '300246', '603988', '002838', '002950',
    #            '600603', '300059', '002623', '600989', '600183', '600030', '002191', '600502',
    #            '002921', '002030', '002540', '002008', '601231', '002593', '002126', '002023',
    #            '002322', '603368', '000950', '000411', '601788', '000738', '601003', '000837',
    #            '605123', '000576', '603010', '002034', '002493', '300879', '002993', '300531',
    #            '300882', '002997', '002998', '002999', '002825', '002489', '002409', '002669',
    #            '002810', '300315', '601615', '002241', '000529', '002232', '002932', '002097',
    #            '002475', '002382', '002487', '000487', '000541', '603288', '002507', '002157',
    #            '603986', '688185', '002007', '300015', '688088'
    #            ]

    #获取所有股票代码并存json文件
    # code = 'http://quote.eastmoney.com/center/gridlist.html#sh_a_board'
    #
    # s = SnowBall(code)
    # #
    # sh = '//*[@id="nav_sh_a_board"]/a'
    # sz = '//*[@id="nav_sz_a_board"]/a'
    # cyb = '//*[@id="nav_gem_board"]/a'
    # kcb = '//*[@id="nav_kcb_board"]/a'
    # #
    # s.get_codes(sh, '上证')
    # print('###############上证结束###############')
    # s.get_codes(sz, '深证')
    # print('###############深证结束###############')
    # s.get_codes(cyb, '创业板')
    # print('###############创业板结束###############')
    # s.get_codes(kcb, '科创板')
    # print('###############科创板结束###############')
    # exit(1)

    l = ['688399', '300206', '605123', '002352', '300853', '688289',
         '002007', '300482', '688096', '002223', '688178', '002262',
         '688088', '300487', '300136', '300628', '000333', '002415',
         '300003', '688039', '601318', '688033',
         ]
    # l = ['688088', '300487', '300136', '300628', '000333', '002415',]
    # stock_filter(l)
    main(l)
    # exit(1)

