from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager


class Department(models.Model):
    name = models.CharField(verbose_name='部门名称', max_length=64)
    description = models.TextField(verbose_name='部门介绍', blank=True, null=True)
    leader = models.CharField(verbose_name='组长', max_length=64)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '部门'
        verbose_name_plural = '部门'


class MemberManager(BaseUserManager):
    def create_user(self, email, name, tel, password=None, **kwargs):
        """Creates and saves a User with the given email, name, tel, and password."""
        if not email:
            raise ValueError('用户必须有一个邮箱!')
        user = self.model(email=self.normalize_email(email), name=name, tel=tel, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, tel, password=None, **kwargs):
        """Creates and saves a SuperUser with the given email, name, tel, and password."""
        superuser = self.create_user(email, name, tel, password=password, **kwargs)
        superuser.is_superuser = True
        superuser.is_admin = True
        superuser.save(using=self._db)
        return superuser


class Member(AbstractBaseUser):
    email = models.EmailField(verbose_name='邮箱', max_length=255, unique=True)
    name = models.CharField(verbose_name='姓名', max_length=16)
    tel = models.CharField(verbose_name='电话', max_length=11, unique=True)
    sex = models.IntegerField(verbose_name='性别', choices=((1, '男'), (0, '女')), blank=True, null=True)
    department = models.ForeignKey(Department, verbose_name='所在部门', null=True, blank=True)
    GRADE = (
        (1, '大一'),
        (2, '大二'),
        (3, '大三'),
        (4, '大四'),
    )
    grade = models.IntegerField(verbose_name='年级', choices=GRADE, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(verbose_name='员工', default=False)
    is_superuser = models.BooleanField(verbose_name='超级用户', default=False)

    objects = MemberManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'tel']

    def get_full_name(self):
        """Return the real name of a member."""
        return self.name

    def get_short_name(self):
        """Return the email(or say,username) of a member."""
        return self.email

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # we can easily rewrite this method when we want the permission function
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app 'app_label'?"""
        # we can easily rewrite this method when we want the permission function
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # the difference between superuser and admin can be changed
        return self.is_admin or self.is_superuser

    @property
    def email_slug(self):
        """slug the email on account of the url pattern"""
        return self.email.replace('.', '-')

    class Meta:
        verbose_name = '成员'
        verbose_name_plural = '成员'
