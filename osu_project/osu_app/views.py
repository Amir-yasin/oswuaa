from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import CustomUserCreationForm
from .models import CustomUser
from django.shortcuts import get_object_or_404



def home(request):
    return render(request, 'base.html', {'current_page': 'base'})
## Home view
def home(request):
    return render(request, 'index.html', {'current_page': 'home'})

# About view
def about(request):
    return render(request, 'about.html', {'current_page': 'about'})

# Contact view
def contact(request):
    return render(request, 'contact.html', {'current_page': 'contact'})

# Signup view


def send_otp_email(user):
    otp = user.generate_otp()
    subject = 'Verify your account'
    message = f'Hello {user.username},\n\nYour OTP is {otp}. Please use this code to verify your account.'
    email_from = 'your-email@example.com'
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_otp_email(user)  # Send OTP after saving the user
            return redirect('verify_otp', user_id=user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


# Login view

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            # phone_number = form.cleaned_data.get('phone_number')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_verified:
                    login(request, user)
                    messages.success(request, 'Logged in successfully!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Please verify your email before logging in.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('home')



def verify_otp(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        entered_otp = request.POST['otp']
        if user.otp == entered_otp:
            user.is_verified = True
            user.is_active = True  # Activate user after successful verification
            user.otp = None  # Clear OTP after verification
            user.save()
            messages.success(request, 'Your account has been verified! Please log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verify_otp.html', {'user': user})


from django.http import HttpResponse
from django.core.management import call_command

def create_superuser_view(request):
    call_command('create_superuser')
    return HttpResponse("Superuser created.")



# Dashboard view
@login_required
def dashboard(request):
    sp_profile = None
    st_profile = None
    
    try:
        sp_profile = SP_Profile.objects.get(user=request.user)
    except SP_Profile.DoesNotExist:
        pass

    try:
        st_profile = ST_Profile.objects.get(user=request.user)
    except ST_Profile.DoesNotExist:
        pass

    context = {
        'sp_profile': sp_profile,
        'st_profile': st_profile,
        'current_page': 'dashboard',
    }
    return render(request, 'dashboard.html', context)
# SP Profile view
@login_required
def SP_profile(request):
    try:
        sp_profile = request.user.sp_profile
    except SP_Profile.DoesNotExist:
        sp_profile = None

    if request.method == 'POST':
        form = SP_ProfileForm(request.POST, request.FILES, instance=sp_profile)
        if form.is_valid():
            sp_profile = form.save(commit=False)
            sp_profile.user = request.user
            sp_profile.save()
            messages.success(request, 'Profile Updated successfully!')
            return redirect('dashboard')
    else:
        form = SP_ProfileForm(instance=sp_profile)
    return render(request, 'SP_profile.html', {'form': form, 'current_page': 'SP_profile'})

# ST Profile view
@login_required
def ST_profile(request):
    try:
        st_profile = request.user.st_profile
    except ST_Profile.DoesNotExist:
        st_profile = None

    if request.method == 'POST':
        form = ST_ProfileForm(request.POST, request.FILES, instance=st_profile)
        if form.is_valid():
            st_profile = form.save(commit=False)
            st_profile.user = request.user
            st_profile.save()
            messages.success(request, 'Profile Updated successfully!')
            return redirect('dashboard')
    else:
        form = ST_ProfileForm(instance=st_profile)
    return render(request, 'ST_profile.html', {'form': form, 'current_page': 'ST_profile'})

# Category view
@login_required
def category(request):
    category = request.GET.get("category")
    if category is None:
        users = SP_Profile.objects.all()
    else:
        users = SP_Profile.objects.filter(category__name=category)
    categories = Category.objects.all()
    return render(request, 'category.html', {'users': users, 'categories': categories, 'current_page': 'category'})






def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': request.META['HTTP_HOST'],
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    send_mail(subject, email, 'admin@example.com', [user.email], fail_silently=False)
                return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form": password_reset_form})

def password_reset_done(request):
    return render(request=request, template_name="password_reset_done.html")

def password_reset_confirm(request, uidb64=None, token=None):
    if request.method == "POST":
        set_password_form = SetPasswordForm(user=request.user, data=request.POST)
        if set_password_form.is_valid():
            set_password_form.save()
            return redirect('password_reset_complete')
    else:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and default_token_generator.check_token(user, token):
            set_password_form = SetPasswordForm(user=user)
            return render(request, 'password_reset_confirm.html', {'set_password_form': set_password_form})
        else:
            return HttpResponse('Password reset link is invalid!', status=400)

def password_reset_complete(request):
    return render(request=request, template_name="password_reset_complete.html")
