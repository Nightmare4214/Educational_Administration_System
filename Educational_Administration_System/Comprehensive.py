#!/usr/bin/env python
# _*_ coding:utf-8 _*_


class Comprehensive:
    def __init__(self, parameter=None):
        if parameter:
            [self.id, self.comprehensive_name, self.comprehensive_class, self.miu, self.performance, self.quality,
             self.score,
             self.failed, self.credit_ratio, self.comprehensive_score, self.grade_rank] = parameter

    # 重载输出
    def __str__(self):
        return '序号:%s，测评名称:%s，班级:%s，miu：%s，表现得分:%s，素质测评得分:%s，成绩测评得分:%s，' \
               '不及格门数:%s，学分比率：%s，综合测评得分：%s，专业年级排名：%s' % (self.id, self.comprehensive_name,
                                                         self.comprehensive_class, self.miu, self.performance,
                                                         self.quality, self.score, self.failed,
                                                         self.credit_ratio, self.comprehensive_score, self.grade_rank)

    # 返回用于json的dict
    def __dict__(self):
        return {
            '序号': self.id,
            '测评名称': self.comprehensive_name,
            '班级': self.comprehensive_class,
            'miu': self.miu,
            '表现得分': self.performance,
            '素质测评得分': self.quality,
            '成绩测评得分': self.score,
            '不及格门数': self.failed,
            '学分比率': self.credit_ratio,
            '综合测评得分': self.comprehensive_score,
            '专业年级排名': self.grade_rank
        }
