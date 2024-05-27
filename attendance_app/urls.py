from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_redirect, name='login_redirect'),
    path('admin_index/', views.AdminIndex, name='admin_index'),
    path('useradd/', views.UserAdd, name='useradd'),
    path('userlist/', views.UserList, name='userlist'),
    path('attendance_overview/', views.AttendanceOverview, name='attendance_overview'),
    path('login/', auth_views.LoginView.as_view(template_name='adminlogin.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    
    
    
    
    path('employee_login/',views.employee_login, name='employee_login'),
    path('employee_logout/',views.employee_logout, name='employee_logout'),
    path('employee_index/',views.employee_index, name='employee_index'),
    
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name = 'employee/password_reset.html'),name='password_reset'),
    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name = 'employee/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'employee/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name = 'employee/password_reset_complete.html'),name='password_reset_complete'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)