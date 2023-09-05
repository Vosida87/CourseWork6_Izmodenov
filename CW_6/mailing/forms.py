from django import forms
from mailing.models import MailingMassage, Mailing, Client
from users.models import User


class MailingMassageForm(forms.ModelForm):
    """
    Форма для писем
    """
    class Meta:
        model = MailingMassage
        fields = ('title', 'message',)


class MailingForm(forms.ModelForm):
    """
    Форма для настрок
    """
    class Meta:
        model = Mailing
        fields = ('mailing_date', 'once_a_day', 'once_a_week', 'once_a_month', 'status', 'clients')
        # clients = forms.MultipleChoiceField(choices=User.client_set, widget=forms.CheckboxSelectMultiple)


class ClientForm(forms.ModelForm):
    """
    Форма для клиентов
    """
    class Meta:
        model = Client
        fields = ['email', 'first_name', 'middle_name', 'last_name']
