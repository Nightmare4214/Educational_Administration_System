#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# 考试时间安排
class Test:
    def __init__(self, parameter=None):
        if parameter:
            [self.id, self.test_name, self.date, self.week, self.period, self.test_time, self.location, self.course,
             self.test_method, self.test_state] = parameter

    # 重载输出
    def __str__(self):
        return '序号:%s，考试名称:%s，考试日期:%s，星期：%s，考试时段:%s，考试时间:%s，考试地点:%s，考试课程:%s，考试方式：%s，考试状态:%s' % (
            self.id, self.test_name, self.date, self.week, self.period, self.test_time, self.location, self.course,
            self.test_method, self.test_state)

    # 返回用于json的dict
    def __dict__(self):
        return {
            '序号': self.id,
            '考试名称': self.test_name,
            '考试日期': self.date,
            '星期': self.week,
            '考试时段': self.period,
            '考试时间': self.test_time,
            '考试地点': self.location,
            '考试课程': self.course,
            '考试方式': self.test_method,
            '考试状态': self.test_state
        }
