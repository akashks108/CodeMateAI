from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')

            return redirect('student_dashboard')

        return render(request, 'accounts/login.html', {
            'error': 'Invalid username or password.'
        })

    return render(request, 'accounts/login.html')
def signup_view(request):
    User = get_user_model()

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {
                'error': 'Username already exists.'
            })

        if password != confirm_password:
            return render(request, 'accounts/signup.html', {
                'error': 'Passwords do not match.'
            })

        if not all([first_name, username, email, password, confirm_password]):
            return render(request, 'accounts/signup.html', {
                'error': 'Please fill in all required fields.'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        return redirect('login')

    return render(request, 'accounts/signup.html')