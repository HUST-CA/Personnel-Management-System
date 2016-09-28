from django.db import models

from account.models import Department


class NewMember(models.Model):
    name = models.CharField(verbose_name='姓名', max_length=16)
    sex = models.IntegerField(verbose_name='性别', choices=((1, '男'), (0, '女')))
    tel = models.CharField(verbose_name='电话', max_length=11)
    email = models.EmailField(verbose_name='邮箱', max_length=255)
    college = models.CharField(verbose_name='专业-年级', max_length=64)
    dormitory = models.CharField(verbose_name='寝室住址', max_length=64)
    department = models.ManyToManyField(Department, verbose_name='部门', blank=True)
    introduction = models.TextField(verbose_name='自我介绍')
    birth = models.CharField(verbose_name='生日', max_length=16, blank=True, null=True)
    qq = models.CharField(verbose_name='qq', max_length=16, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def district(self):
        return self.dormitory.split('-')[0]

    class Meta:
        verbose_name = '报名者'
        verbose_name_plural = '报名者'
