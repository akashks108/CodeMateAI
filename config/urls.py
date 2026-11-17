from django.contrib import admin as django_admin
from django.urls import path
from accounts.views import login_view
from administrator.views import admin_dashboard
from accounts.views import signup_view
from student.views import student_dashboard
from administrator.views import student_list
from django.contrib.auth import views as auth_views
from student.views import learning_page
from django.urls import include
from administrator.views import curriculum_management, add_topic, edit_topic, delete_topic

urlpatterns = [
    path('django-admin/', django_admin.site.urls),
    path('', login_view, name='login'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('signup/', signup_view, name='signup'),
    path('student-dashboard/', student_dashboard, name='student_dashboard'),
    path('admin-dashboard/students/', student_list, name='student_list'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('learn/<str:language>/', learning_page, name='learning_page'),
    path('student/', include('student.urls')),
    path('admin-dashboard/curriculum/', curriculum_management, name='curriculum_management'),
    path('admin-dashboard/curriculum/<slug:language_slug>/level/<int:level_id>/add-topic/',add_topic,name='add_topic'),
    path('admin-dashboard/curriculum/<slug:language_slug>/topic/<int:topic_id>/edit/',edit_topic,name='edit_topic'),
    path('admin-dashboard/curriculum/<slug:language_slug>/topic/<int:topic_id>/delete/', delete_topic, name='delete_topic'),
    
]