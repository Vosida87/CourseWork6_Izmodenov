from random import randint
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, TemplateView, FormView
from django.conf import settings
from users.forms import UserRegisterForm, UserProfileForm, UserResetPasswordForm
from users.models import User


class RegisterView(CreateView):
    """
    Регистрация пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

    def form_valid(self, form):
        user = form.save()
        user.rand_key = randint(0, 2147483647)
        user.save()
        verify_url = reverse('users:verify_email', args=[user.rand_key])
        verify_link = self.request.build_absolute_uri(verify_url)
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Пожалуйста, перейдите по следующей ссылке, чтобы подтвердить свой адрес электронной почты:{verify_link}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )
        return super().form_valid(form)


class ProfileView(UpdateView):
    """
    Страница профиля
    """
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class VerifyEmailView(View):
    """
    Проверка через почту
    """
    def get(self, request, rand_key):
        try:
            user = User.objects.get(rand_key=rand_key)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse('users:email_confirmed'))
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('users:email_verify_failed.html'))


class ResetPasswordView(FormView):
    """
    Сброс пароля
    """
    model = User
    template_name = 'users/reset_password.html'
    form_class = UserResetPasswordForm
    success_url = reverse_lazy('users:reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['username']
        try:
            user = User.objects.get(email=email)
            new_password = User.objects.make_random_password(length=12)
            user.set_password(new_password)
            user.save()
            send_mail(
                'Восстановление пароля',
                f'Ваш новый пароль для входа: {new_password}',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False
            )
        except User.DoesNotExist:
            return redirect('users:reset_failed')
        return super().form_valid(form)
