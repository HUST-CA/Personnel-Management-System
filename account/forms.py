from django import forms
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import ugettext_lazy

from .models import Member

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit
from crispy_forms.bootstrap import Tab, TabHolder, AppendedText, InlineRadios
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='邮箱(作为用户名)',
        error_messages={
            "required": "邮箱不能为空!",
            "invalid": "不符合邮箱格式!",
            NON_FIELD_ERRORS: {
                'unique': "该邮箱已被注册!",
            },
        },
        required=True,
        max_length=64
    )
    password = forms.CharField(
        label='密码',
        error_messages={
            "required": "密码不能为空!",
            "invalid": "密码不能含有特殊字符!",
            "max_length": "密码过长!",
        },
        widget=forms.PasswordInput(),
        required=True,
        max_length=32
    )
    password2 = forms.CharField(
        label='确认密码',
        error_messages={
            "required": "密码不能为空!"
        },
        widget=forms.PasswordInput(),
        required=True,
        max_length=32
    )
    name = forms.CharField(
        label='真实姓名',
        error_messages={
            "required": "姓名不能为空!",
            "max_length": "姓名过长!",
        },
        required=True,
        max_length=16,
    )
    tel = forms.CharField(
        label='手机号码',
        error_messages={
            "required": "手机号码不能为空!"
        },
        required=True,
        max_length=11,
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_class = 'the_form'
        self.helper.attrs = {'onsubmit': 'disable_button()'}

        self.helper.layout = Layout(
            Fieldset(
                '请填写以下表格',
                TabHolder(
                    Tab(
                        '信息',
                        AppendedText('email', '''<span class="glyphicon glyphicon-envelope"></span>''',
                                     placeholder='请输入您的邮箱'),
                        AppendedText('password', '''<span class="glyphicon glyphicon-arrow-right"></span>''',
                                     placeholder='请输入密码'),
                        AppendedText('password2', '''<span class="glyphicon glyphicon-exclamation-sign"></span>''',
                                     placeholder='请确认密码'),
                        AppendedText('name', '''<span class="glyphicon glyphicon-user"></span>''',
                                     placeholder='请输入您的真实姓名'),
                        AppendedText('tel', '''<span class="glyphicon glyphicon-phone"></span>''',
                                     placeholder='请输入您的手机号码'),
                        Field('captcha'),
                    ),
                ),
            ),
            ButtonHolder(
                Submit('submit', '注册', css_class='button white'),
            )
        )
        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = {}
        kwargs['error_messages'].update({'required': ugettext_lazy('不能为空哦~')})

    def clean_email(self):
        email = self.cleaned_data['email']
        if Member.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被注册!')
        else:
            return email

    def clean_name(self):
        name = self.cleaned_data['name']
        for char in name:
            if char < u'\u4e00' or char > u'\u9fa5':
                raise forms.ValidationError('我读书少,这不是中文吧...')
        return name

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if Member.objects.filter(tel=tel).exists():
            raise forms.ValidationError('该号码已被使用!')
        elif len(tel) != 11:
            raise forms.ValidationError('手机号码应该是11位吧...')
        else:
            return tel

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError("两次密码不一致!")
        else:
            return password


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='邮箱',
        error_messages={
            "required": u"邮箱不能为空!",
        },
        required=True,
        max_length=64
    )
    password = forms.CharField(
        label='密码',
        error_messages={
            "required": u"密码不能为空!",
        },
        widget=forms.PasswordInput(),
        required=True,
        max_length=32
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_class = 'the_form'
        self.helper.attrs = {'onsubmit': 'disable_button()'}

        self.helper.layout = Layout(
            Fieldset(
                '用户登录',
                AppendedText('email', '''<span class="glyphicon glyphicon-envelope"></span>''',
                             placeholder='请输入您的邮箱'),
                AppendedText('password', '''<span class="glyphicon glyphicon-arrow-right"></span>''',
                             placeholder='请输入密码'),
                Field('captcha'),
            ),
            ButtonHolder(
                Submit('submit', '登录', css_class='button white')
            )
        )
        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = {}
        kwargs['error_messages'].update({'required': ugettext_lazy('不能为空哦~')})


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label='原密码',
        error_messages={'required': '请输入原密码'},
        required=True,
        widget=forms.PasswordInput(),
    )
    password = forms.CharField(
        label='新密码',
        error_messages={'required': '请输入新密码'},
        required=True,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label='确认密码',
        error_messages={'required': '请再次输入新密码'},
        required=True,
        widget=forms.PasswordInput(),
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_class = 'the_form'
        self.helper.attrs = {'onsubmit': 'disable_button()'}

        self.helper.layout = Layout(
            Fieldset(
                '密码修改',
                AppendedText('old_password', '''<span class="glyphicon glyphicon-thumbs-down"></span>''',
                             placeholder='请输入原密码'),
                AppendedText('password', '''<span class="glyphicon glyphicon-thumbs-up"></span>''',
                             placeholder='请输入新密码'),
                AppendedText('password', '''<span class="glyphicon glyphicon-exclamation-sign"></span>''',
                             placeholder='请确认新密码'),
                Field('captcha'),
            ),
            ButtonHolder(
                Submit('submit', '确认修改', css_class='button white')
            )
        )
        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = {}
        kwargs['error_messages'].update({'required': ugettext_lazy('不能为空哦~')})

    def clean_password2(self):
        password = self.cleaned_data.get('password', '')
        password2 = self.cleaned_data.get('password2', '')
        if password != password2:
            raise forms.ValidationError("两次密码不一致!")
        else:
            return password


class OwnInfoForm(forms.ModelForm):
    sex = forms.ChoiceField(
        choices=((1, '男'), (0, '女')),
        label='性别',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(OwnInfoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                '个人信息',
                TabHolder(
                    Tab(
                        '个人信息',
                        AppendedText('name', '''<span class="glyphicon glyphicon-user"></span>''',
                                     placeholder='请输入您的真实姓名'),
                        AppendedText('tel', '''<span class="glyphicon glyphicon-phone"></span>''',
                                     placeholder='请输入您的手机号码'),
                        InlineRadios('sex'),
                        Field('department'),
                        Field('grade'),
                    ),
                ),
            ),
            ButtonHolder(
                Submit('submit', '确认修改', css_class='button white')
            )
        )
        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = {}
        kwargs['error_messages'].update({'required': ugettext_lazy('不能为空哦~')})

    def clean_name(self):
        name = self.cleaned_data['name']
        for char in name:
            if char < u'\u4e00' or char > u'\u9fa5':
                raise forms.ValidationError('我读书少,这不是中文吧...')
        return name

    def clean_tel(self):
        tel = self.cleaned_data['tel']
        if Member.objects.filter(tel=tel).exclude(name=self.cleaned_data['name']).exists():
            raise forms.ValidationError('该号码已被使用!')
        elif len(tel) != 11:
            raise forms.ValidationError('手机号码应该是11位吧...')
        else:
            return tel

    class Meta:
        model = Member
        fields = ['name', 'tel', 'sex', 'department', 'grade']


class UserForgotPasswordForm(PasswordResetForm):
    email = forms.EmailField(
        label='您注册的邮箱',
        required=True,
        max_length=64
    )
    name = forms.CharField(
        label='您的真实姓名',
        required=True,
        max_length=16,
    )
    tel = forms.CharField(
        label='您的手机号码',
        required=True,
        max_length=11,
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(UserForgotPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_class = 'the_form'
        self.helper.attrs = {'onsubmit': 'disable_button()'}

        self.helper.layout = Layout(
            Fieldset(
                '请填写您的信息',
                TabHolder(
                    Tab(
                        '必填',
                        AppendedText('email', '''<span class="glyphicon glyphicon-envelope"></span>''',
                                     placeholder='请输入您的邮箱'),
                        AppendedText('name', '''<span class="glyphicon glyphicon-user"></span>''',
                                     placeholder='请输入您的真实姓名'),
                        AppendedText('tel', '''<span class="glyphicon glyphicon-phone"></span>''',
                                     placeholder='请输入您的手机号码'),
                        Field('captcha'),
                    ),
                ),
            ),
            ButtonHolder(
                Submit('submit', '找回密码', css_class='button white')
            )
        )
        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = {}
        kwargs['error_messages'].update({'required': ugettext_lazy('不能为空哦~')})

    def clean(self):
        # this time we will get the value of 3 fields,so we should not use clean_xxx(),or we can only get xxx's value
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        tel = self.cleaned_data['tel']
        if Member.objects.filter(email=email, name=name, tel=tel).exists():
            return self.cleaned_data
        else:
            raise forms.ValidationError('邮箱与姓名，电话不匹配！')

    def get_users(self, email):
        active_users = Member.objects.filter(email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())


class ResetPasswordConfirmForm(SetPasswordForm):
    error_messages = {
        'password_mismatch': "两次密码不匹配!",
    }
    new_password1 = forms.CharField(
        label="新密码",
        widget=forms.PasswordInput,
        required=True,
        strip=False,
    )
    new_password2 = forms.CharField(
        label="密码确认",
        widget=forms.PasswordInput,
        required=True,
        strip=False,
    )
    captcha = CaptchaField(
        label='验证码',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(ResetPasswordConfirmForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.field_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.form_class = 'the_form'
        self.helper.attrs = {'onsubmit': 'disable_button()'}

        self.helper.layout = Layout(
            Fieldset(
                '请填写新的密码',
                TabHolder(
                    Tab(
                        '必填',
                        AppendedText('new_password1', '''<span class="glyphicon glyphicon-thumbs-up"></span>''',
                                     placeholder='新密码'),
                        AppendedText('tel', '''<span class="glyphicon glyphicon-exclamation-sign"></span>''',
                                     placeholder='密码确认'),
                        Field('captcha'),
                    ),
                ),
            ),
            ButtonHolder(
                Submit('submit', '确认重置', css_class='button white')
            )
        )
        if 'error_messages' not in kwargs:
            kwargs['error_messages'] = {}
        kwargs['error_messages'].update({'required': ugettext_lazy('不能为空哦~')})
