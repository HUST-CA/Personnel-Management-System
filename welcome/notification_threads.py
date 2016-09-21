from django.core.mail import send_mass_mail
from django.conf import settings
from welcome import calc_sign
from welcome import send_sms

import threading
import json

'''
Takes a tuple of messages and send them

A message is a tuple containing these four elements:
(subject, message, from_email, recipient_list)
'''


class MassEmailSenderThread(threading.Thread):
    def __init__(self, messages):
        '''
        messages[0] -> first message(the greet message)
                   [3] -> recipient_list in first message
                      [0] -> first address in recipient_list
        '''
        first_receiver_name = messages[0][3][0].split("@", 1)[0]
        super(MassEmailSenderThread, self).__init__(name="EmailSenderThread-" + first_receiver_name, daemon=False)
        self.messages = messages

    def run(self):
        send_mass_mail(self.messages)


'''
Takes REST service API URL and SMS params to send a short message

For AliDayu. Read its documentation for the params.
The "sign" parameter will be calculated here. No need to add in the params.
'''


class SMSSenderThread(threading.Thread):
    def __init__(self, url, params):
        first_receiver_name = json.loads(params['sms_param'])['name']
        super(SMSSenderThread, self).__init__(name="SMSSenderThread-" + first_receiver_name, daemon=False)
        self.url = url
        self.params = params

    def run(self):
        sign = calc_sign.calc_sign(self.params, settings.SECRET)
        self.params['sign'] = sign
        send_sms.send_sms(self.url, self.params)
