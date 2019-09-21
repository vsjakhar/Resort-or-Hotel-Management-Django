# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.utils import timezone
import datetime
from email_cronjob.models import Email_cron



def my_scheduled_job():
	ram = Email_cron.objects.filter(email_sent=0)
	for i in ram:
		receiver = str(i.email_to)
		sender = str(i.email_from)
		subject1 = str(i.email_subject)
		body = str(i.email_body)
		send_mail(subject1, 'how are you', 'Auragoa <donotreply@auragoa.com>', [receiver], html_message=body, fail_silently=False)
		i.email_sent = 1
		i.save()