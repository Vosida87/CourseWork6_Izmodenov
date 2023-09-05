import os
from datetime import datetime, timedelta, timezone
from django.core.mail import send_mail
from django.conf import settings
import schedule
import time
import django
from CW_6.settings import EMAIL_HOST_USER

PROJECT_NAME = 'CW_6'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')
django.setup()

from mailing.models import Mailing

# Сделал переменную now чтобы не было конфликта subtract offset-naive and offset-aware datetimes
now = datetime.now(timezone.utc)


def main():
    """
    Основная функция
    """

    def send_by_email():
        """
        Функция проходится по рассылкам и отправляет их исходя из настроек даты
        """

        # Проверка на активацию, остаются только активированные

        mailings = Mailing.objects.filter(status=True)

        for mailing in mailings:

            # При условии, что отправка идёт каждый день, разница между временем сейчас
            # и временем прошлой отправки должна быть больше или равно 1 дню
            # или же лог отсутствует

            if mailing.once_a_day:
                if (now - mailing.logs.last_mailing_date) >= timedelta(
                        days=1):

                    # Отправляет письмо если прошло проверку

                    send_mail(f'{mailing.messages.title}',
                              f'{mailing.messages.message}',
                              EMAIL_HOST_USER,
                              [mailing.clients.email],
                              )

                    # Далее сохраняем лог

                    mailing.logs.last_mailing_date = now
                    mailing.logs.status = True
                    mailing.logs.save()

            # При условии, что отправка идёт каждую неделю, разница между временем сейчас
            # и временем прошлой отправки должна быть больше или равно 1 недели
            # или же лог отсутствует

            elif mailing.once_a_week:
                if (now - mailing.logs.last_mailing_date) >= timedelta(
                        weeks=1) or mailing.logs.last_mailing_date is None:

                    # Отправляет письмо если прошло проверку

                    send_mail(f'{mailing.messages.title}',
                              f'{mailing.messages.message}',
                              settings.EMAIL_HOST_USER,
                              [mailing.clients.email],
                              )

                    # Далее сохраняем лог

                    mailing.logs.last_mailing_date = now
                    mailing.logs.status = True
                    mailing.logs.save()

            # При условии, что отправка идёт каждый месяц, разница между временем сейчас
            # и временем прошлой отправки должна быть больше или равно 30 дней
            # или же лог отсутствует

            elif mailing.once_a_month:
                if (now - mailing.logs.last_mailing_date) >= timedelta(
                        days=30) or mailing.logs.last_mailing_date is None:

                    # Отправляет письмо если прошло проверку

                    send_mail(f'{mailing.messages.title}',
                              f'{mailing.messages.message}',
                              settings.EMAIL_HOST_USER,
                              [mailing.clients.email],
                              )

                    # Далее сохраняем лог

                    mailing.logs.last_mailing_date = now
                    mailing.logs.status = True
                    mailing.logs.save()

        # Возвращаю True для того, чтобы функция не возвращала None и не ломался schedule

        return True

    # Ниже приведён скрипт, который выполняет функцию send_by_email каждые 10 секунд

    schedule.every(1).seconds.do(send_by_email)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
