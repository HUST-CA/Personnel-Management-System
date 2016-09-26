from models import NewMember
from account.models import Department

def create_new_one(line):
    info_dict = {}
    info_list = line.split(',')
    info_dict['name']=info_list[0]#姓名
    info_dict['sex']=1 if info_list[1]=='男' else 0#性别
    info_dict['birth']=info_list[2]#生日
    info_dict['tel']=info_list[3]#手机号
    info_dict['college']=info_list[4]#专业-年级
    info_dict['qq']=info_list[5]#qq
    info_dict['dormitory']=info_list[6]#寝室住址
    info_dict['department']=info_list[7]#部门,填了多个部门请用xxx-xxx-xxx的格式
    info_dict['introduction']=info_list[8]#自我介绍,里面逗号请用中文逗号！切勿英文逗号！
    info_dict['email']=info_list[9]#邮箱，没有的话用qq邮箱填充或者‘undefined@qq.com’
    
    department_object_list=[]
    for each in info_dict['department'].splite('-'):
            department_object_list.add(Department(name=each))
    del info_dict['department']
    new_one=NewMember(**info_dict)
    new_one.save()
    new_one.department.add(*department_object_list)
        
count=0
#信息从文件offline_member_info.csv中读取！    
with open('offline_member_info.csv','r') as info:
    for line in info.readline():
        create_new_one(line)
        count+=1    
print('Done after adding',count,'numbers!')
