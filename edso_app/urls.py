from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register_student/', views.register_student, name='register_student'),
    path('login/', views.login_student, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    
    path('login_member/', views.login_member, name='login_member'),
    path('member_dashboard/', views.member_dashboard, name='member_dashboard'),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    
    path('login_admin/', views.login_admin, name='login_admin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('add-course/', views.add_course, name='add_course'),
    path('edit-course/<int:course_id>/', views.edit_course, name='edit_course'),
    path('course-list/', views.course_list, name='course_list'),
]
