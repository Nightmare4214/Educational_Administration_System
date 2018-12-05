#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from Test import Test
from Score import Score
from Course import Course
from Mediation import Mediation
from MakeUp import MakeUp
from Comprehensive import Comprehensive
import requests
from bs4 import BeautifulSoup
from work import get_word
import json
import pickle


class Student:
    # 手动输入验证码
    def get_img_code_by_manual(self):
        return input('please input the valid code: ')

    # 设置cookie
    # @param username 账号
    # @param password 密码
    def set_cookies(self, username, password):
        session = requests.session()
        img_url = 'http://jw.xujc.com/imgcode.php'
        img = session.get(img_url, headers=self.headers)
        with open(username + '_imgcode.jpg', 'wb') as f:
            f.write(img.content)
        # img_code = self.get_img_code_by_manual()
        # 用卷积网络识别
        img_code = get_word(username + '_imgcode.jpg')
        user_lb = '学生'.encode('gb2312')
        data = {
            'username': username,
            'password': password,
            'imgcode': img_code,
            'user_lb': user_lb
        }
        login_url = 'http://jw.xujc.com/index.php?c=Login&a=login'
        session.post(login_url, data=data, headers=self.headers)
        self.cookies = session.cookies
        print(self.cookies.get_dict())
        with open(username + '_cookie.txt', 'wb') as f:
            pickle.dump(self.cookies.get_dict(), f)

    # 获得tbody
    # @param url 要访问的链接
    # @param table_name 网页存放数据的table名字
    def get_tbody(self, url, table_name='data_table'):
        html = requests.get(url, cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(html.text, 'lxml')
        data_table = soup.find('table', attrs={'id': table_name})
        return data_table.find('tbody')

    # 测试一下能不能登入
    def test(self):
        url = 'http://jw.xujc.com/student/index.php?c=Default&a=index'
        html = requests.get(url, cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(html.text, 'lxml')
        return soup.find('div', attrs={'id': 'inf'})

    # @param username 账号
    # @param password 密码
    def __init__(self, username, password):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
        try:
            # 读取cookie文件
            with open(username + '_cookie.txt', 'rb') as f:
                self.cookies = pickle.load(f)
            # 测试一下能不能登入
            if not self.test():
                self.set_cookies(username, password)
        except:
            self.set_cookies(username, password)

    # 考试安排
    def get_tests(self):
        url = 'http://jw.xujc.com/student/index.php?c=Search&a=ksap'
        tbody = self.get_tbody(url)
        all_test = []
        for tr in tbody.find_all('tr'):
            temp = Test([td.text for td in tr.find_all('td')])
            all_test += [temp.__dict__()]
        return all_test

    # 根据学期查询成绩
    # @param tm_id 学期，要求str类型，例如'20172'代表2017-2018第二学期
    def get_score_by_tm_id(self, tm_id=None):
        if tm_id is None:
            return
        url = 'http://jw.xujc.com/student/index.php?c=Search&a=cj&tm_id=' + tm_id
        tbody = self.get_tbody(url)
        all_score = []
        for tr in tbody.find_all('tr'):
            temp = Score([td.text for td in tr.find_all('td') if td.text != ''])
            all_score += [temp.__dict__()]
        return all_score

    # 根据学期查询课程
    # @param tm_id 学期，要求str类型，例如'20172'代表2017-2018第二学期
    def get_Course_by_tm_id(self, tm_id=None):
        if tm_id is None:
            return
        url = 'http://jw.xujc.com/student/index.php?c=Default&a=Wdkc&tm_id=' + tm_id
        tbody = self.get_tbody(url)
        all_course = []
        for index, tr in enumerate(tbody.find_all('tr')):
            # 每条课程后面都有两个没用的
            if index % 3 != 0:
                continue
            # 第9个是查找，前8个才有用
            temp = Course([td.text for index, td in enumerate(tr.find_all('td')) if index < 8])
            all_course += [temp.__dict__()]
        return all_course

    # 调停课
    def get_Course_Mediation(self):
        url = 'http://jw.xujc.com/student/index.php?c=Default&a=tbk'
        tbody = self.get_tbody(url)
        all_mediation = []
        for tr in tbody.find_all('tr'):
            temp = Mediation([td.text for td in tr.find_all('td')])
            all_mediation += [temp.__dict__()]
        return all_mediation

    # 补课
    def get_Course_Make_Up(self):
        url = 'http://jw.xujc.com/student/index.php?c=Default&a=tbk'
        tbody = self.get_tbody(url, 'data_table2')
        all_MakeUp = []
        for tr in tbody.find_all('tr'):
            temp = MakeUp([td.text for td in tr.find_all('td')])
            all_MakeUp += [temp.__dict__()]
        return all_MakeUp

    # 综合测评
    def get_Comprehensive_Score(self):
        url = 'http://jw.xujc.com/student/index.php?c=Search&a=zhcp'
        tbody = self.get_tbody(url)
        all_comprehensive = []
        for tr in tbody.find_all('tr'):
            temp = Comprehensive([td.text.strip() for td in tr.find_all('td')])
            all_comprehensive += [temp.__dict__()]
        return all_comprehensive

    def get_API_Key(self):
        url = 'http://jw.xujc.com/student/index.php?c=Client&a=index'
        html = requests.get(url, cookies=self.cookies, headers=self.headers)
        soup = BeautifulSoup(html.text, 'lxml')
        t = soup.find('td', class_='left')
        return {'API Key': t.text}
