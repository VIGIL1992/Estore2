from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('short_course_view/', views.short_course_view, name='short_course_view'),
    path('short_course_create/', views.short_course_create, name='short_course_create'),
    
    path('course_delete/<int:course_id>', views.course_delete, name='course_delete'),
    path('course_create/', views.course_create, name='course_create'),
    path('course_edit/<int:course_id>', views.course_edit, name='course_edit'),
    path('search_courses/', views.search_courses, name='search_courses'),
    
    
    
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    
]