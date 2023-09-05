from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import *
from django.views.decorators.cache import cache_page

app_name = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('<int:pk>/', MailingDetailView.as_view(), name='mailing_view'),
    path('create/', MailingCreateView.as_view(), name='mailing_create'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('clients/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_view'),
    path('client_create/', ClientCreateView.as_view(), name='client_create'),
    path('clients_delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('clients_update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
]
