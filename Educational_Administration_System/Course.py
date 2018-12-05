#!/usr/bin/env python
# _*_ coding:utf-8 _*_


# 课程
class Course:
    def __init__(self, parameter=None):
        if parameter:
            [self.id, self.course, self.credit, self.teacher, self.classroom, self.start, self.study_method, self.num] \
                = parameter

    # 重载输出
    def __str__(self):
        return '序号:%s，课程班名称:%s，学分:%s，任课教师：%s，上课时间地点:%s，起止周:%s，修课方式:%s，修课人数:%s' % (
            self.id, self.course, self.credit, self.teacher, self.classroom, self.start, self.study_method, self.num)

    # 返回用于json的dict
    def __dict__(self):
        return {
            '序号': self.id,
            '课程班名称': self.course,
            '学分': self.credit,
            '任课教师': self.teacher,
            '上课时间地点': self.classroom,
            '起止周': self.start,
            '修课方式': self.study_method,
            '修课人数': self.num
        }
