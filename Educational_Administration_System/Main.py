#!/usr/bin/env python
# _*_ coding:utf-8 _*_
from Student import Student
import json
if __name__ == '__main__':
    username = 'SWE16004'
    password = ''
    test = Student(username, password)
    print(json.dumps(test.get_tests(), ensure_ascii=False))
    print(json.dumps(test.get_score_by_tm_id('20172'), ensure_ascii=False))
    print(json.dumps(test.get_Course_by_tm_id('20161'), ensure_ascii=False))
    print(json.dumps(test.get_Course_Mediation(), ensure_ascii=False))
    print(json.dumps(test.get_Course_Make_Up(), ensure_ascii=False))
    print(json.dumps(test.get_Comprehensive_Score(), ensure_ascii=False))
    print(json.dumps(test.get_API_Key(), ensure_ascii=False))
