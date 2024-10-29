from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [

path('', views.home , name = 'home'),
path('about', views.about , name = 'about'),
path('contact', views.contact , name = 'contact'),
path('signup', views.signup , name = 'signup'),
path('logins/', views.user_login , name = 'logins'),
path('login/', views.user_login , name = 'login'),
path('logout/', views.user_logout, name='user_logout'),
path('dashboard', views.dashboard , name = 'dashboard'),
path('SP_profile', views.SP_profile , name = 'SP_profile'),
path('ST_profile', views.ST_profile , name = 'ST_profile'),
path('category', views.category, name='category'),
path('verify/<int:user_id>/', views.verify_otp, name='verify_otp'),

path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)