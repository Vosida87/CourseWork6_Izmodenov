from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from mailing.models import Client, MailingLogs, Mailing
from mailing.forms import MailingForm, MailingMassageForm, ClientForm
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache


class DispatchMixin:
    """
    Запрещение тем, кто не владеет рассылкой или клиентом - изменять или удалять их
    """
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner != self.request.user:
            return HttpResponseForbidden(
                "Вы не можете этого сделать"
            )
        return super().dispatch(request, *args, **kwargs)


class Clients(Client):
    """
    Получает список клиентов + кеш
    """
    def get_clients(self):
        if settings.CACHE_ENABLED:
            key = Client.objects.all()
            clients_list = cache.get(key)
            if clients_list in None:
                clients_list = Client.objects.all()
                cache.set(key, clients_list)
        else:
            clients_list = Client.objects.all()

        return clients_list


class MailingListView(LoginRequiredMixin, ListView):
    """
    Отображает список рыссылок
    """
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        return super().get_queryset().all()


class MailingDetailView(LoginRequiredMixin, DetailView):
    """
    Посмотреть всю инфу о рассылке
    """
    model = Mailing
    template_name = 'mailing/mailing_view.html'


class MailingCreateView(LoginRequiredMixin, Clients, CreateView):
    """
    Создать рассылку
    """
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Передаём сразу и сообщение и его настройки

        context['mailing_form'] = MailingForm
        context['mailingmessage_form'] = MailingMassageForm
        return context

    def form_valid(self, form):
        mailing = form.save()
        mailing_massage = MailingMassageForm(self.request.POST).save()

        # Присвайваем полю владелец - пользователя

        mailing_massage.owner = self.request.user
        mailing_massage.save()

        # Присвайваем полю владелец - пользователя

        mailing.owner = self.request.user
        mailing.messages = mailing_massage

        # При выборе одного из mode нужно выключить другие

        mode = self.request.POST.get('mode')
        if mode == 'once_a_day':
            mailing.once_a_day = True
            mailing.once_a_week = False
            mailing.once_a_month = False
        elif mode == 'once_a_week':
            mailing.once_a_day = False
            mailing.once_a_week = True
            mailing.once_a_month = False
        elif mode == 'once_a_month':
            mailing.once_a_day = False
            mailing.once_a_week = False
            mailing.once_a_month = True

        # Создаём лог для записи

        mailing_logs = MailingLogs.objects.create()
        mailing.logs = mailing_logs

        mailing.save()
        return super().form_valid(form)


class MailingDeleteView(DispatchMixin, LoginRequiredMixin, DeleteView):
    """
    Удаляет рассылку
    """
    model = Mailing
    template_name = 'mailing/mailing_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingUpdateView(DispatchMixin, LoginRequiredMixin, Clients, UpdateView):
    """
    Редактирует рассылку
    """
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Передаём сразу и сообщение и его настройки

        context['mailing_form'] = MailingForm
        context['mailingmessage_form'] = MailingMassageForm
        return context

    def form_valid(self, form):
        mailing = form.save()
        mailing_massage = MailingMassageForm(self.request.POST).save()

        # Присвайваем полю владелец - пользователя

        mailing_massage.owner = self.request.user
        mailing_massage.save()

        # Присвайваем полю владелец - пользователя

        mailing.owner = self.request.user
        mailing.messages = mailing_massage

        # При выборе одного из mode нужно выключить другие

        mode = self.request.POST.get('mode')
        if mode == 'once_a_day':
            mailing.once_a_day = True
            mailing.once_a_week = False
            mailing.once_a_month = False
        elif mode == 'once_a_week':
            mailing.once_a_day = False
            mailing.once_a_week = True
            mailing.once_a_month = False
        elif mode == 'once_a_month':
            mailing.once_a_day = False
            mailing.once_a_week = False
            mailing.once_a_month = True

        mailing_logs = MailingLogs.objects.create()
        mailing.logs = mailing_logs

        # Создаём лог для записи

        mailing.save()
        return super().form_valid(form)

    # Проверка отправки рассылки на почту клиентам (Успешно)

    # def form_valid(self, form):
    #     message = form.save()
    #     message.save()
    #
    #     # for client in self.clients:
    #     #     if message.mailing.status:
    #     #         send_mail(f'{message.title}',
    #     #                   f'{message.message}',
    #     #                   settings.EMAIL_HOST_USER,
    #     #                   [client.email],
    #     #                   )
    #     #     else:
    #     #         continue
    #
    #     return super().form_valid(form)


class ClientListView(LoginRequiredMixin, ListView):
    """
    Отображает список клиентов
    """
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        return super().get_queryset().all()


class ClientCreateView(LoginRequiredMixin, CreateView):
    """
    Позволяет создать клиента
    """
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:client_list')

    def form_valid(self, form):
        client = form.save()
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientDetailView(DispatchMixin, LoginRequiredMixin, DetailView):
    """
    Позволяет узнать подробную инфу о клиенте
    """
    model = Client
    template_name = 'mailing/client_view.html'


class ClientDeleteView(DispatchMixin, LoginRequiredMixin, DeleteView):
    """
    Удаляет клиента
    """
    model = Client
    template_name = 'mailing/client_delete.html'
    success_url = reverse_lazy('mailing:client_list')


class ClientUpdateView(DispatchMixin, LoginRequiredMixin, UpdateView):
    """
    Редактирует клиента
    """
    model = Client
    template_name = 'mailing/client_form.html'
    form_class = ClientForm
    success_url = reverse_lazy('mailing:client_list')
