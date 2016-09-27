from django import forms
from django.utils.translation import ugettext_lazy

from account.models import Department

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, ButtonHolder, Submit
from crispy_forms.bootstrap import Tab, TabHolder, AppendedText, InlineCheckboxes, InlineRadios
from captcha.fields import CaptchaField


class WelcomeForm(forms.Form):
    name = forms.CharField(
        label='姓名',
        required=True,
        max_length=16,
    )

    sex = forms.ChoiceField(
        choices=((1, '男'), (0, '女')),
        label='性别',
        required=True,
    )

    tel = forms.CharField(
        label='手机号码',
        required=True,
        max_length=11,
    )

    email = forms.EmailField(
        label='邮箱',
        required=True,
        max_length=64,
    )

    college = forms.CharField(
        label='专业-年级',
        required=True,
        max_length=64,
    )

    dormitory = forms.CharField(
        label='寝室住址',
        required=True,
        max_length=64,
    )

    department = forms.ModelMultipleChoiceField(
        label='部门',
        queryset=Department.objects.all(),
        required=False,
    )

    introduction = forms.CharField(
        label='自我介绍',
        widget=forms.Textarea(),
        required=True,
        max_length=2000,
    )

    captcha = CaptchaField(
        label='验证码',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(WelcomeForm, self).__init__(*args, **kwargs)
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
                        '报名信息',
                        AppendedText('name', '''<span class="glyphicon glyphicon-user"></span>''',
                                     placeholder='填写你的姓名'),
                        InlineRadios('sex'),
                        AppendedText('tel', '''<span class="glyphicon glyphicon-phone"></span>''',
                                     placeholder='填写你的手机号码'),
                        AppendedText('email', '''<span class="glyphicon glyphicon-envelope"></span>''',
                                     placeholder='填写你的邮箱'),
                        AppendedText('college', '''<span class="glyphicon glyphicon-book"></span>''',
                                     placeholder='"专业-年级数字",如"软件工程-15"'),
                        AppendedText('dormitory', '''<span class="glyphicon glyphicon-home"></span>''',
                                     placeholder='"宿舍区-楼栋号-寝室号","韵苑-11-101"'),
                        InlineCheckboxes('department'),
                        Field('introduction', placeholder='介绍一下你自己吧~分享一下你的经历和兴趣爱好咯'),
                        Field('captcha'),
                    )
                ),
            ),
            ButtonHolder(
                Submit('submit', '提交', css_class='button white'),
            ),
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
        try:
            int(tel)
        except ValueError:
            raise forms.ValidationError('你确定这是手机号...')
        if len(tel) != 11:
            raise forms.ValidationError('手机号码应该是11位吧...')
        else:
            return tel
'''
    def clean_college(self):
        college = self.cleaned_data['college']
        try:
            major, grade = college.split('-')
        except ValueError:
            raise forms.ValidationError('你的格式没填对吧?')
        if grade not in ('14', '15', '16'):
            raise forms.ValidationError('你的格式没填对吧?')
        else:
            return college

    def clean_dormitory(self):
        dormitory = self.cleaned_data['dormitory']
        try:
            dor, house, code = dormitory.split('-')
        except ValueError:
            raise forms.ValidationError('你的格式没填对吧?')
        try:
            int(house)
            int(code)
        except ValueError:
            raise forms.ValidationError('按照格式填咯')
        return dormitory
'''
