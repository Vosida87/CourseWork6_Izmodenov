from django.contrib import admin
from mailing.models import Client, MailingMassage, Mailing, MailingLogs


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name')


admin.site.register(Mailing)


@admin.register(MailingMassage)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('mailing',)


@admin.register(MailingLogs)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_mailing_date', 'status')
