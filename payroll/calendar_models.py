from django.db import models
from django.shortcuts import reverse
from .models import Person
from django.conf import settings

from decimal import Decimal


CURRENCY = settings.CURRENCY
SCHEDULE_CHOICES = (
    ('a', 'Normal Time'),
    ('b', 'Extra time')
)

class PersonSchedule(models.Model):
    date_start = models.DateTimeField(verbose_name='From')
    date_end = models.DateTimeField(verbose_name='Until')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='schedules')
    hours = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    category = models.CharField(choices=SCHEDULE_CHOICES, default='a', max_length=1)
    cost = models.DecimalField(default=0, decimal_places=2, max_length=20, max_digits=20)

    class Meta:
        ordering = ['-date_start']

    def __str__(self):
        return f'Schedule - {self.id}'

    def save(self, *args, **kwargs):
        diff = self.date_end - self.date_start
        days, seconds = diff.days, diff.seconds
        self.hours = Decimal(days * 24) + Decimal(seconds / 3600)

        if self.category == 'a':
            self.cost = self.hours*self.person.value_per_hour
        else:
            self.cost = self.hours * self.person.extra_per_hour
        print('total cost', self.hours, self.cost)
        super().save(*args, **kwargs)

    def get_delete_url(self):
        return reverse('payroll_bills:delete_schedule', kwargs={'pk': self.id})

    def tag_value(self):
        return f'{self.cost} {CURRENCY}'