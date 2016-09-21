from django.shortcuts import render
from django.views import generic
from django.contrib.auth import mixins, authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.conf import settings

import time

from . import forms
from .models import Member


class RegisterView(generic.View):
    template_name = 'account/register.html'

    def get(self, request):
        form = forms.RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email_slug = cd['email'].replace('.', '-')
            user = Member.objects.create_user(cd['email'], cd['name'], cd['tel'], cd['password'])
            login(request, user)  # when someone finishes the register proceedings,we automatic log him in
            messages.add_message(request, messages.SUCCESS, '注册成功！')
            return HttpResponseRedirect(reverse('account:own', kwargs={'email_slug': email_slug}))
        else:
            messages.add_message(request, messages.WARNING, '注册失败，请重试。')
            # do not use form = forms.RegisterForm()，or the faults in the fields may not show
            return render(request, self.template_name, {'form': form})


class LoginView(generic.View):
    template_name = 'account/login.html'

    def get(self, request):
        form = forms.LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, '登录成功！')
                return HttpResponseRedirect(request.GET.get('next', ''))
            else:
                messages.add_message(request, messages.WARNING, '无效的账户!')
                return HttpResponseRedirect(reverse('account:login'))
        else:
            messages.add_message(request, messages.WARNING, '用户名或密码不正确!')
            return HttpResponseRedirect(reverse('account:login'))


class LogoutView(mixins.LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('account:login')

    def get(self, request):
        logout(request)
        messages.add_message(request, messages.SUCCESS, '注销成功！')
        return HttpResponseRedirect(request.GET.get('next', ''))


class PasswordChangeView(mixins.LoginRequiredMixin, generic.View):
    template_name = 'account/password_change.html'
    # do not use reverse，just use reverse_lazy to preclude the bugs
    login_url = reverse_lazy('account:login')

    def get(self, request):
        form = forms.PasswordChangeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.PasswordChangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = request.user.email
            email_slug = email.replace('.', '-')
            old_password = cd['old_password']
            user = authenticate(username=email, password=old_password)
            if user is not None and user.is_active:
                new_password = cd['password']
                user.set_password(new_password)
                user.save()
                messages.add_message(request, messages.SUCCESS, '修改密码成功！')
                # after somebody changes his password,we automatic log him in,or he will not go to the own page
                login(request, authenticate(username=email, password=new_password))
                return HttpResponseRedirect(reverse('account:own', kwargs={'email_slug': email_slug}))
            else:
                messages.add_message(request, messages.WARNING, '修改密码失败,请确认原密码正确。')
                return HttpResponseRedirect(reverse('account:password_change'))
        else:
            messages.add_message(request, messages.WARNING, '修改密码失败,请确认表单填写正确。')
            return render(request, self.template_name, {'form': form})


class Own(mixins.LoginRequiredMixin, generic.edit.UpdateView):
    login_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        if request.user.email_slug == self.kwargs['email_slug']:
            return super(Own, self).get(request)
        else:
            raise PermissionDenied

    def get_object(self, queryset=None):
        email = self.kwargs['email_slug'].replace('-', '.')
        current_member = Member.objects.get(email=email)
        return current_member

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, '修改成功!')
        return reverse_lazy('account:own', args=(self.kwargs['email_slug'],))

    template_name = 'account/own.html'
    form_class = forms.OwnInfoForm


class PasswordResetView(generic.View):
    template_name = 'account/password_reset.html'
    email_blacklist = []
    # domain name can be rewrite if you want
    domain = ''
    from_email = settings.EMAIL_HOST_USER

    def get(self, request):
        if request.user.is_authenticated:
            messages.add_message(request, messages.SUCCESS, '您已登录，可在个人中心直接更换密码!')
        form = forms.UserForgotPasswordForm()
        return render(request, self.template_name, {'form': form, 'user': request.user})

    def post(self, request):
        form = forms.UserForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            if self.function_check_email(email):
                print(self.request.META['REMOTE_ADDR'])
                form.save(
                    domain_override=self.domain,
                    subject_template_name='account/password_reset_subject.txt',
                    email_template_name='account/password_reset_email.html',
                    use_https=True,
                    from_email=self.from_email,
                    request=self.request,
                    extra_email_context={
                        'current_time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())),
                        'ip_address': self.request.META['REMOTE_ADDR'],
                    }
                )
                messages.add_message(request, messages.SUCCESS, '邮件发送成功')
                return render(request, 'account/success.html', {'email': email, 'flag': '邮件发送'})
            else:
                print(email, '在黑名单中!')
                messages.add_message(request, messages.WARNING, email + '在黑名单中!')
                return HttpResponseRedirect(reverse('account:password_reset'))
        else:
            messages.add_message(request, messages.WARNING, '发送邮件失败，请确表单填写正确！')
            return render(request, self.template_name, {'form': form})

    def function_check_email(self, email):
        """check this email address whether it's in blacklist"""
        return email not in self.email_blacklist


class PasswordResetConfirmView(generic.View):
    template_name = 'account/password_reset_confirm.html'

    def get(self, request):
        form = forms.ResetPasswordConfirmForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.ResetPasswordConfirmForm(request.POST)
        # let the form.save() handle the information
        if form.is_valid():
            form.save()
            email = form.user.email
            messages.add_message(request, messages.SUCCESS, '密码重置成功')
            return render(request, 'account/success.html', {'email': email, 'flag': '密码重置'})
        else:
            messages.add_message(request, messages.WARNING, '重置密码失败，请确表单填写正确！')
            return render(request, self.template_name, {'form': form})
