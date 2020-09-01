from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time
import traceback
import sys
import os
import json
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# from pandas import DataFrame, Series
# import numpy as np
# import  pandas as pd
import xlwt
from datetime import datetime
import traceback


class Stock(object):
    DRIVER = r'/usr/local/bin/phantomjs'
    # DRIVER = r'C:\Users\Administrator\phantomjs-2.1.1-windows\bin\phantomjs.exe'
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
    TIMEOUT = 10
    data = dict()

    def __init__(self, url):
        self.driver = webdriver.PhantomJS(self.DRIVER, service_args=self.SERVICE_ARGS, desired_capabilities=self.DCAP)
        self._get_source(url)

    def _get_source(self, url, sleep_time=2):
        self.driver.get(url)
        time.sleep(sleep_time)
        print(self.driver.current_url)
        return self.driver

    def _get_element(self, locator):
        WebDriverWait(self.driver, self.TIMEOUT, 0.5).until(EC.presence_of_element_located((By.XPATH, locator)))
        return self.driver.find_element_by_xpath(locator)

    def __del__(self):
        self.close()

    def close(self):
        self.driver.close()
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
    def basic_info(self):
        all_basic = '//*[@id="app"]/div[2]/div[2]/div[5]/table/tbody'
        x_current_price = '//*[@id="app"]/div[2]/div[2]/div[5]/div/div[1]/div[1]/strong'
        x_name = '//*[@id="app"]/div[2]/div[2]/div[1]'
        x_website = '//*[@id="app"]/div[2]/div[3]/div[2]/div[2]/div[1]/div/a'

        self.data['name'] = self._get_element(x_name).text
        self.data['current_price'] = self._get_element(x_current_price).text
        self.data['all_basic'] = self._get_element(all_basic).text
        self.data['website'] = self._get_element(x_website).get_attribute("href")

        for d in self.data['all_basic'].split():
            if "市盈率(TTM)" in d:
                self.data['PE'] = d.split('：')[-1].strip()
            elif "总市值" in d:
                self.data['market_value'] = d.split('：')[-1].strip()
            elif "总股本" in d:
                self.data['total_equity'] = d.split('：')[-1].strip()
            elif "市盈率(静)" in d:
                self.data['PE_static'] = d.split('：')[-1].strip()
            elif "市盈率(动)" in d:
                self.data['PE_dynamic'] = d.split('：')[-1].strip()
            elif "每股收益" in d:
                self.data['EPS'] = d.split('：')[-1].strip()
            elif "每股净资产" in d:
                self.data['BVPS'] = d.split('：')[-1].strip()

            # self.data['market_value'] = self._get_element(x_market_value).text.replace('亿', '')
            # self.data['website'] = self._get_element(x_website).get_attribute("href")
            #
            # self.data['total_equity'] = self._get_element(x_total_equity).text
            # self.data['PE_static'] = self._get_element(x_PE_static).text
            # self.data['PE_dynamic'] = self._get_element(x_PE_dynamic).text
            # self.data['EPS'] = self._get_element(x_EPS).text
            # self.data['BVPS'] = self._get_element(x_BVPS).text

        #print(self.data)
        return self.data

    #财务信息
    def financial(self):

        #net_Profit = '//*[@id="app"]/div[2]/div[2]/div/div[4]/div/table'
        per_year_bt = '//*[@id="app"]/div[2]/div[2]/div/div[2]/div[1]/span[2]'
        per_year = '//*[@id="app"]/div[2]/div[2]/div/div[4]/div/table'
        #all = '//*[@id="app"]/div[2]/div[2]/div/div[2]/div[1]/span[1]'
        tb = '//*[@id="app"]/div[2]/div[2]/div/div[2]/div[2]/label/input'

        continued_growth_in_turnover = '' #营业额持续增长
        continued_growth_in_profit = '' #净利润持续增长
        gross_profit_margin = '' #毛利率
        net_profit_ratio = '' #净利率
        DABR = '' #资产负债率
        cash_flow_ratio = '' #现金流比率
        cash_cycle = '' #现金循环周期
        inventory_turnover_days = '' #存货周转天数
        total_asset_turnover = '' #总资产周转率

        # self._get_element(tb).click()
        # self.data['all'] = self._get_element(net_Profit).text
        self._get_element(per_year_bt).click()
        self.data['per_year'] = self._get_element(per_year).text

        report_years = 0
        financial_datas = self.data['per_year'].split()
        for i in financial_datas[1:6]:
            if "年报" in i:
                report_years += 1
        #index1 = financial_datas.index('营业收入')
        index2 = financial_datas.index('营业收入同比增长')
        turnover_continue = list_sum(financial_datas[index2 + 1: index2 + report_years + 1])
        self.data['continued_growth_rate_in_turnover'] = turnover_continue[0]/report_years
        self.data['continued_growth_rate_in_turnover_without_negative'] = turnover_continue[1]
        index3 = financial_datas.index('净利润')
        profit = financial_datas[index3 + 1: index3 + report_years + 1]

        index4 = financial_datas.index('净利润同比增长')
        profit_continue = list_sum(financial_datas[index4 + 1: index4 + report_years + 1])
        self.data['continued_growth_rate_in_profit'] = profit_continue[0]/report_years
        self.data['continued_growth_rate_in_profit_without_negative'] = profit_continue[1]

        index5 = financial_datas.index('销售毛利率')
        self.data['gross_profit_margin'] = list_sum(financial_datas[index5 + 1: index5 + report_years + 1])[0]/report_years
        index6 = financial_datas.index('销售净利率')
        self.data['net_profit_ratio'] = list_sum(financial_datas[index6 + 1: index6 + report_years + 1])[0]/report_years
        index7 = financial_datas.index('资产负债率')
        self.data['DABR'] = list_sum(financial_datas[index7 + 1: index7 + report_years + 1])[0]/report_years
        index8 = financial_datas.index('现金流量比率')
        self.data['cash_flow_ratio'] = list_sum(financial_datas[index8 + 1: index8 + report_years + 1])[0]/report_years
        index9 = financial_datas.index('存货周转天数')
        self.data['inventory_turnover_days'] = list_sum(financial_datas[index9 + 1: index9 + report_years + 1])[0]/report_years
        index10 = financial_datas.index('现金循环周期')
        self.data['cash_cycle'] = list_sum(financial_datas[index10 + 1: index10 + report_years + 1])[0]/report_years
        index11 = financial_datas.index('总资产周转率')
        self.data['total_asset_turnover'] = list_sum(financial_datas[index11 + 1: index11 + report_years + 1])[0]/report_years
        index12 = financial_datas.index('净资产收益率')
        self.data['ROE'] = list_sum(financial_datas[index12 + 1: index12 + report_years + 1])[0]/report_years

        if '万亿' in self.data['market_value'][:-2]:
            self.data['market_value'] = float(self.data['market_value'][:-2])*10000
            self.data['value_coefficient'] = float(self.data['market_value'])/float(profit[0][:-1])
        else:
            self.data['value_coefficient'] = float(self.data['market_value'][:-2]) / float(profit[0][:-1])
        self.data['write'] = False

        print(self.data['name'] + ' Done!')

        # 股票筛选

        continued_growth_rate_in_turnover = 30
        continued_growth_rate_in_turnover_without_negative =True
        continued_growth_rate_in_profit = 25
        continued_growth_rate_in_profit_without_negative = True
        gross_profit_margin = 30
        net_profit_ratio = 20
        cash_flow_ratio = 0.05
        DABR = 50
        ROE = 20
        value_coefficient = 80

        if self.data['continued_growth_rate_in_turnover'] >= continued_growth_rate_in_turnover \
                and self.data['continued_growth_rate_in_turnover_without_negative'] is True \
                and self.data['continued_growth_rate_in_profit'] > continued_growth_rate_in_profit \
                and self.data['continued_growth_rate_in_profit_without_negative'] is True \
                and self.data['gross_profit_margin'] > gross_profit_margin \
                and self.data['net_profit_ratio'] > net_profit_ratio \
                and self.data['DABR'] < DABR \
                and self.data['cash_flow_ratio'] > cash_flow_ratio \
                and self.data['ROE'] > ROE \
                and self.data['value_coefficient'] < value_coefficient:
            self.data['write'] = True

        return self.data

    #高层管理
    def management(self):
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

def stock_filter(stock_list):
    excel = Excel()
    basic = excel.add_sheet('Basic info')
    excel.write_head(basic)
    index = 1
    NOT_PROCSSED = []

    for i in stock_list:
        if i.startswith('30') or i.startswith('00'):
            stock_code = 'SZ' + str(i)
        elif i.startswith('68') or i.startswith('60'):
            stock_code = 'SH' + str(i)
        else:
            exit("Stock Code was not correct!")
        XQ = 'https://xueqiu.com/S/{}'.format(stock_code)
        CW = "https://xueqiu.com/snowman/S/{}/detail#/ZYCWZB".format(stock_code)
        glc = 'https://xueqiu.com/snowman/S/{}/detail#/GSGG'.format(stock_code)

        try:
            b = Stock(XQ)
            b.basic_info()

            f = Stock(CW)
            financial_data = f.financial()

        except Exception as e:
            print(e)
            exc_type, exc_value, exc_obj = sys.exc_info()
            traceback.print_tb(exc_obj)
            NOT_PROCSSED.append(i)
            continue
        excel.write_to_excel(basic, financial_data, index, financial_data['write'])
        if financial_data['write']:
            index += 1
    excel.save("result_{}.xls".format(time.time()))

if __name__ == '__main__':

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
    # s = Stock(code)
    #
    # sh = '//*[@id="nav_sh_a_board"]/a'
    # sz = '//*[@id="nav_sz_a_board"]/a'
    # cyb = '//*[@id="nav_gem_board"]/a'
    # kcb = '//*[@id="nav_kcb_board"]/a'
    #
    # s.get_codes(sh, '上证')
    # print('###############上证结束###############')
    # s.get_codes(sz, '深证')
    # print('###############深证结束###############')
    # s.get_codes(cyb, '创业板')
    # print('###############创业板结束###############')
    # s.get_codes(kcb, '科创板')
    # print('###############科创板结束###############')
    # exit(1)


    #从文件中读取股票代码
    # sh = get_code_list('上证.json')
    # sz = get_code_list('深证.json')
    kcb = get_code_list('科创板.json')
    # cyb = get_code_list('创业板.json')

    stock_filter(kcb)
    # stock_filter(sz)
    # stock_filter(kcb)
    # stock_filter(cyb)




