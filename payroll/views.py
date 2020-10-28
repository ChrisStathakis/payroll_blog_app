from django.shortcuts import render, reverse, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import ListView, UpdateView, CreateView, TemplateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.conf import settings

from payroll.models import Payroll, Occupation, Person, PAYROLL_CHOICES
from payroll.forms import PayrollForm, PersonForm, OccupationForm, PayrollPersonForm, PersonSheduleForm, PersonSchedule
from payroll.calendar_models import PersonSchedule



CURRENCY = settings.CURRENCY