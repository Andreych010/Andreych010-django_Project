from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import CreateView, UpdateView

from django_project import settings
from users.forms import UserRegisterForm, UserProfileForm, LoginUserForm
from users.models import User, Code


class UserLoginView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('catalog:home')


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm')

    def form_valid(self, form):
        code = get_random_string(6, '1234567890')  # Генерируем 6ти значный код для подтверждения
        user = form.save(commit=False)  # Создание объекта пользователя без сохранения в базу данных
        user.is_active = False  # Установка статуса активации на False
        user.save()
        Code.objects.create(
            code=code,
            user=user
        )  # Создаём запись кода для пользователя в БД
        self.request.session['user_id'] = user.id
        # Сохраняем id пользователя в сессии, чтобы в подтверждении можно было найти этого пользователя
        # и при правильном вводе кода авторизовать
        send_mail(
            subject='Верификация почты',
            message=f'Для верификации почты введите данный код {code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return redirect('users:confirm')


class ConfirmView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'users/confirm_account.html')

    def post(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        # Получаем id пользователя
        user = User.objects.get(pk=user_id)  # Получаем пользователя по id
        code_user = request.POST.get('code_user')  # Получаем код(который ввел пользователь) с формы
        if not code_user:  # Если код не введен, перенаправляем снова на ввод
            return redirect('users:confirm')
        try:
            Code.objects.get(code=code_user, user=user)
            # Пытаемся найти код пользователя в таблице с кодами, и если код найден, то идем дальше
        except Code.DoesNotExist:
            # Если код не совпал, то перенаправляем на повторное подтверждение, но уже с ошибкой
            return render(request, 'users/confirm_account.html', context={
                'error': 'Не верно введенный код'
            })
        user.is_active = True
        # Если код совпал, то пользователь имеет статус активного
        user.save()
        Code.objects.get(
            code=code_user,
            user=user
        ).delete()
        # Удаляем код из БД, тк пользователь его ввёл
        login(request, user)
        # Авторизовываем пользователя в сессии
        del request.session['user_id']
        # Удаляем id пользователя из сессии
        return redirect('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def user_gen_password(request):
    user_email = request.POST.get("user_email")
    # Получаем почту (с формы), на которую отправлять новый пароль
    if not user_email:
        return redirect(reverse('users:login'))
        # Если почта не указана, то опять на логин
    try:
        # Пытаемся найти пользователя в БД по почте
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        # Если не нашли, то опять на логин
        return redirect(reverse('users:login'))
    # chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    new_password = get_random_string(6, '1234567890')
    send_mail(
        subject='Сгенерированн новый пароль',
        message=f'Ваш пароль для авторизации {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )
    # Отправляем на почту новый пароль
    user.set_password(new_password)
    # Для пользователя, которого нашли по введенной почте меняем пароль
    user.save()
    return redirect(reverse('users:login'))
