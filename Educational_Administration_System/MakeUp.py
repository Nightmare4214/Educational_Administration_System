#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# 补课
class MakeUp:
    def __init__(self, parameter=None):
        if parameter:
            [self.id, self.change_type, self.course, self.teacher, self.change_week, self.week, self.course_session,
             self.change_time, self.classroom] = parameter

    # 重载输出
    def __str__(self):
        return '序号:%s，类型:%s，课程班名称:%s，教师：%s，补课周:%s，星期:%s，节次:%s，补课日期:%s，教室：%s' % (
            self.id, self.change_type, self.course, self.teacher, self.change_week, self.week, self.course_session,
            self.change_time, self.classroom)

    # 返回用于json的dict
    def __dict__(self):
        return {
            '序号': self.id,
            '类型': self.change_type,
            '课程班名称': self.course,
            '教师': self.teacher,
            '补课周': self.change_week,
            '星期': self.week,
            '节次': self.course_session,
            '补课日期': self.change_time,
            '教室': self.classroom
        }
