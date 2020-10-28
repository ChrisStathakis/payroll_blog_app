from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
import uuid
CURRENCY = settings.CURRENCY

import datetime
from dateutil.relativedelta import relativedelta


def initial_date(request, months=12):
    #  gets the initial last three months or the session date
    date_now = datetime.datetime.today()
    current_year = f'01/01/{datetime.date.today().year} - 12/31/{datetime.date.today().year}'
    date_range = request.GET.get('date_range', current_year)
    date_start, date_end = None, None

    if date_range:
        try:
            date_range = date_range.split('-')
            date_range[0] = date_range[0].replace(' ','')
            date_range[1] = date_range[1].replace(' ','')
            date_start = datetime.datetime.strptime(date_range[0], '%m/%d/%Y')
            date_end = datetime.datetime.strptime(date_range[1],'%m/%d/%Y')
        except:
            print('except hitted')
            date_three_months_ago = date_now - relativedelta(months=months)
            date_start = date_three_months_ago
            date_end = date_now
            date_range = '%s - %s' % (str(date_three_months_ago).split(' ')[0].replace('-','/'),str(date_now).split(' ')[0].replace('-','/'))
            request.session['date_range'] = '%s - %s'%(str(date_three_months_ago).split(' ')[0].replace('-','/'),str(date_now).split(' ')[0].replace('-','/'))
    return [date_start, date_end, date_range]



class DefaultOrderModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    date_expired = models.DateField(default=timezone.now)
    value = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    taxes = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    paid_value = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    final_value = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    discount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    is_paid = models.BooleanField(default=True)
    printed = models.BooleanField(default=False)
    objects = models.Manager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.uid

    def tag_is_paid(self):
        return 'Is Paid' if self.is_paid else 'Not Paid'

    def tag_value(self):
        return f'{self.value} {CURRENCY}'
    tag_value.short_description = 'Αρχική Αξία'

    def tag_final_value(self):
        return f'{self.final_value} {CURRENCY}'
    tag_final_value.short_description = 'Αξία'

    def tag_paid_value(self):
        return f'{self.paid_value} {CURRENCY}'

    def get_remaining_value(self):
        return self.final_value - self.paid_value

    def tag_payment_method(self):
        return f'{self.payment_method} {CURRENCY}'