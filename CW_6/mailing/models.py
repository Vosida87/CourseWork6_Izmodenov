from django.db import models
from django.utils import timezone
from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Mailing(models.Model):
    """
    Настройки рассылки
    """
    mailing_date = models.DateTimeField(verbose_name='Время рассылки')
    once_a_day = models.BooleanField(default=False, verbose_name='Периодичность: раз в день')
    once_a_week = models.BooleanField(default=False, verbose_name='Периодичность: раз в неделю')
    once_a_month = models.BooleanField(default=False, verbose_name='Периодичность: раз в  месяц')
    status = models.BooleanField(default=False, verbose_name='Активация рассылки')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)
    messages = models.ForeignKey('MailingMassage', on_delete=models.CASCADE, **NULLABLE)
    clients = models.ForeignKey('Client', on_delete=models.DO_NOTHING, **NULLABLE)
    logs = models.ForeignKey('MailingLogs', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.mailing_date}, {self.status}'

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class Client(models.Model):
    """
    Получатель
    """
    email = models.EmailField(max_length=254, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.email} ({self.first_name})'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class MailingMassage(models.Model):
    """
    Сообщение для рассылки
    """
    title = models.CharField(max_length=100, verbose_name='Тема письма')
    message = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class MailingLogs(models.Model):
    """
    Логи рассылки
    """
    last_mailing_date = models.DateTimeField(verbose_name='Дата и время последней попытки', **NULLABLE)
    status = models.BooleanField(default=False, verbose_name='Статус попытки')

    def __str__(self):
        return f'{self.last_mailing_date}'

    class Meta:
        verbose_name = 'Лог'
        verbose_name_plural = 'Логи'

