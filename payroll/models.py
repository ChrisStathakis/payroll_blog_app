from .abstract_models import *

from django.shortcuts import reverse
from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

User = get_user_model()

CURRENCY = settings.CURRENCY
PAYROLL_CHOICES = (
    ('1', 'Salary'),
    ('2', 'Extra'),
    )


class Occupation(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=64)
    notes = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)

    objects = models.Manager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.balance = self.person_set.all().aggregate(Sum('balance'))['balance__sum'] \
            if self.person_set.all().exists() else 0
        super().save(*args, *kwargs)

    def tag_balance(self):
        return '%s %s' % (self.balance, CURRENCY)

    tag_balance.short_description = 'Remaining'



class Person(models.Model):
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=64, unique=True)
    phone = models.CharField(max_length=10, blank=True)
    phone1 = models.CharField(max_length=10, blank=True)
    occupation = models.ForeignKey(Occupation, null=True, blank=True, verbose_name='Απασχόληση', on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=50, decimal_places=2, default=0)
    value_per_hour = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    extra_per_hour = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    monthly_salary = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    objects = models.Manager()



    def save(self, *args, **kwargs):
        self.balance = self.update_balance()
        super().save(*args, **kwargs)
        self.occupation.save() if self.occupation else ''

    def update_balance(self):
        queryset = self.person_invoices.all()
        value = queryset.aggregate(Sum('final_value'))['final_value__sum'] if queryset else 0
        paid_value = queryset.aggregate(Sum('paid_value'))['paid_value__sum'] if queryset else 0
        diff = value - paid_value
        return diff


    def __str__(self):
        return self.title

    def tag_balance(self):
        return '%s %s' % (self.balance, CURRENCY)

    def tag_occupation(self):
        return f'{self.occupation.title}' if self.occupation else 'No data'

    def get_card_url(self):
        return reverse('person_card', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('person_delete', kwargs={'pk': self.id})

    @staticmethod
    def filters_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        occup_name = request.GET.getlist('occup_name', None)
        queryset = queryset.filter(title__icontains=search_name) if search_name else queryset
        queryset = queryset.filter(occupation__id__in=occup_name) if occup_name else queryset

        return queryset



class PayrollInvoiceManager(models.Manager):
    def invoice_per_person(self, instance):
        return super(PayrollInvoiceManager, self).filter(person=instance)

    def not_paid(self):
        return super(PayrollInvoiceManager, self).filter(is_paid=False)


class Payroll(DefaultOrderModel):
    title = models.CharField(max_length=150, blank=True)
    person = models.ForeignKey(Person, on_delete=models.PROTECT,
                               related_name='person_invoices')
    category = models.CharField(max_length=1, choices=PAYROLL_CHOICES, default='1')
    objects = models.Manager()

    class Meta:
        ordering = ['is_paid', '-date_expired', ]

    def __str__(self):
        return '%s %s' % (self.date_expired, self.person.title)


    def __str__(self):
        return '%s %s' % (self.date_expired, self.person.title)

    def save(self, *args, **kwargs):
        self.final_value = self.value
        self.paid_value = self.final_value if self.is_paid else 0
        if self.id:
            self.title = f'Μισθοδοσια {self.id}' if not self.title else self.title
        super(Payroll, self).save(*args, **kwargs)
        self.person.save()