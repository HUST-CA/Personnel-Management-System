from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect
# from django.urls import reverse

from . import forms
from .models import NewMember


class WelcomeView(generic.View):
    template_name = 'welcome/welcome.html'

    def get(self, request):
        form = forms.WelcomeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.WelcomeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            del cd['captcha']
            department = cd['department']
            del cd['department']
            new_one = NewMember(**cd)
            new_one.save()
            new_one.department.add(*department)
            # NewMember.objects.create(**cd)
            # can not directly create a object with many-to-many field
            # we must invoke save() method before add the many-to-many field
            messages.add_message(request, messages.SUCCESS, '报名成功,请确认收到短信或邮件！')
            if '/?' in request.META['HTTP_REFERER']: # Symbol of portal (ugly)
                return HttpResponseRedirect('http://192.168.1.1:5280/?connect=1&redirect=http%3A%2F%2Fwww.hustca.com%2F')
            # Redirect to the portal of our router.
            else:
                return render(request, self.template_name, {'form': form})

        else:
            messages.add_message(request, messages.WARNING, '报名失败，请查看各项后的错误提示。')
            return render(request, self.template_name, {'form': form})