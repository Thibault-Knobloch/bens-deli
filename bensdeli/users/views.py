from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, UserEditForm, CustomPasswordResetForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView


# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # authenticate the user
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            next_url = request.GET.get('next', '/')
            # log in the user
            login(request, user)
            return redirect(next_url)
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def logout_view(request):
    next_url = request.GET.get('next', '/')
    logout(request)
    return redirect(next_url)


def user_login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            next_url = request.GET.get('next', '/')
            if next_url == "/register/" or next_url == "/login/":
                next_url = "/"
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def profile_view(request):
    user = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile_view")
    if request.method == "GET":
        form = UserEditForm(instance=user, initial={'username': user.username, 'email': user.email})
        return render(request, "users/profile.html", {'form': form})
    return redirect("index_view")


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Replace with your desired template name

    def form_valid(self, form):
        # Perform any custom logic here
        return super().form_valid(form)

    def get_success_url(self):
        # Replace with your desired URL or reverse_lazy reference
        return reverse_lazy('password_reset_complete')