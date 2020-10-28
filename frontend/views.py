from django.shortcuts import reverse, get_object_or_404, redirect, HttpResponseRedirect
from django.contrib import messages
from django.views.generic import  UpdateView, TemplateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings

from payroll.models import Payroll, Occupation, Person
from payroll.forms import PayrollForm, PersonForm, OccupationForm, PayrollPersonForm, PersonScheduleForm
from payroll.calendar_models import PersonSchedule


CURRENCY = settings.CURRENCY


@method_decorator(staff_member_required, name='dispatch')
class HomepageView(TemplateView):
    template_name = 'homepage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["create_form"] = PersonForm()
        context['create_occup'] = OccupationForm()
        context['persons'] = Person.objects.all()
        context['occupations'] = Occupation.objects.all()
        return context


@staff_member_required
def create_occupation_view(request):
    form = OccupationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New Occupation added!')
    return redirect(reverse('homepage'))


@staff_member_required
def create_person_view(request):
    form = PersonForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'New Person added!')
    else:
        print('error')
        messages.warning(request, form.errors)
    return redirect(reverse('homepage'))



@method_decorator(staff_member_required, name='dispatch')
class OccupationUpdateView(UpdateView):
    template_name = 'form.html'
    model = Occupation
    form_class = OccupationForm

    def get_context_data(self, **kwargs):
        context = super(OccupationUpdateView, self).get_context_data(**kwargs)
        context['form_title'] = f'Update {self.object}'
        context['back_url'] = reverse('homepage')
        context['delete_url'] = reverse('')
        return context
    
    def form_valid(self, form):
        form.save()
        return self.form_valid(form)


@staff_member_required
def occupation_delete_view(request, pk):
    obj = get_object_or_404(Occupation, id=pk)
    obj.delete()
    return redirect(reverse('homepage'))


@method_decorator(staff_member_required, name='dispatch')
class PersonCardView(UpdateView):
    model = Person
    template_name = 'person_view.html'
    form_class = PersonForm

    def get_success_url(self):
        return reverse('person_card', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = True
        context['page_title'] = self.object
        context['payment_form'] = PayrollPersonForm(initial={'person': self.object})
        context['calendar_form'] = PersonScheduleForm(initial={'person': self.object})
        context['payments'] = self.object.person_invoices.all()
        context['schedules'] = self.object.schedules.all()
        return context

    def form_valid(self, form):
        form.save()
        return super(PersonCardView, self).form_valid(form)


@staff_member_required
def handle_payroll_view(request, pk, type_):
    if type_ == 'delete':
        obj = get_object_or_404(Payroll, id=pk)
        obj.delete()
    elif type_ == 'create':
        form = PayrollForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'New Payroll Added')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@staff_member_required
def handle_schedule_view(request, pk, type_):
    if type_ == 'delete':
        obj = get_object_or_404(PersonSchedule, id=pk)
        obj.delete()
    elif type_ == 'create':
        print('create')
        form = PersonScheduleForm(request.POST or None)
        print(form.errors)
        if form.is_valid():
            print('form valid')
            form.save()
            messages.success(request, 'New Payroll Added')
        else:
            print(form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def delete_person_view(request, pk):
    person = get_object_or_404(Person, id=pk)
    person.delete()
    return redirect(reverse('homepage'))