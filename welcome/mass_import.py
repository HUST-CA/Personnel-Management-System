'''使用前记得把同级目录下的__init__.py里的内容注释掉,否则会发greet短信和邮件'''
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hustca.settings")
django.setup()
# 在django里面的其他py文件要调用django的内容,必须指定django的settings
# 必须在前面加上面的内容
from welcome.models import NewMember
from account.models import Department


# 此处不可以from . import models,因为它和views的机制不同,必须指定目录,因为是把hustca目录看成包

def create_new_one(line):
    info_dict = {}
    info_list = line.split(',')
    info_dict['name'] = info_list[0]  # 姓名
    info_dict['sex'] = 1 if info_list[1] == '男' else 0  # 性别
    info_dict['birth'] = info_list[2]  # 生日
    info_dict['tel'] = info_list[3]  # 手机号
    info_dict['college'] = info_list[4]  # 专业-年级
    info_dict['qq'] = info_list[5]  # qq
    info_dict['dormitory'] = info_list[6]  # 寝室住址
    info_dict['department'] = info_list[7]  # 部门,填了多个部门请用xxx-xxx-xxx的格式
    info_dict['introduction'] = info_list[8]  # 自我介绍,里面逗号请用中文逗号！切勿英文逗号！
    info_dict['email'] = 'undefined@qq.com'  # 邮箱纸质表上没填,默认‘undefined@qq.com’

    department_object_list = []
    for each in info_dict['department'].split('-'):
        d = Department(name=each)
        d.save()
        # remember we must call the save() method before use add()
        # ps: save() method doesn't return the object
        department_object_list.append(d)
    del info_dict['department']
    new_one = NewMember(**info_dict)
    new_one.save()
    new_one.department.add(*department_object_list)


def run():
    count = 0
    # 信息从文件offline_member_info.csv中读取！
    # csv请注意如下格式
    # 蛤蛤，男，1999.9.9，15927554193，电磁场-15,847731770，韵苑-23-205，义务维修队-权益部-办公室
    # windows默认是gbk,要手动encoding='utf-8'
    with open('offline_member_info.csv', encoding='utf-8') as info:
        for line in info.readlines():
            create_new_one(line)
            print(line)
            count += 1
    print('Done after adding', count, 'numbers!')


if __name__ == '__main__':
    run()
