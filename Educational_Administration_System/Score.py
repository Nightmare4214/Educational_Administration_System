#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# 成绩
class Score:
    def __init__(self, parameter=None):
        self.id, self.course, self.credit, self.score, self.study_method = parameter

    # 重载输出
    def __str__(self):
        return '序号:%s，课程名称:%s，学分:%s，成绩：%s，修课方式:%s' % (
            self.id, self.course, self.credit, self.score, self.study_method)

    # 返回用于json的dict
    def __dict__(self):
        return {
            '序号': self.id,
            '课程名称': self.course,
            '学分': self.credit,
            '成绩': self.score,
            '修课方式': self.study_method
        }
