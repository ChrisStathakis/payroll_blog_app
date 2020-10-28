from django.contrib import admin
from django.urls import path

from frontend.views import (HomepageView, create_occupation_view, create_person_view, delete_person_view,
                            occupation_delete_view, PersonCardView, OccupationUpdateView,
                            handle_payroll_view, handle_schedule_view
                            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomepageView.as_view(), name='homepage'),
    path('create-peron/', create_person_view, name='create_person'),
    path('create-occupation/', create_occupation_view, name='create_occupation'),
    path('update-occupation/<int:pk>/', OccupationUpdateView.as_view(), name='update_occup'),
    path('delete-occupation/<int:pk>/', occupation_delete_view, name='delete_occup'),
    path('person-card/<int:pk>/', PersonCardView.as_view(), name='person_card'),
    path('person/create-payroll/<int:pk>/<slug:type_>/', handle_payroll_view, name='handle_payroll'),
    path('person/create-schedule/<int:pk>/<slug:type_>/', handle_schedule_view, name='handle_schedule'),
    path('person/delete/<int:pk>/', delete_person_view, name='person_delete')
]