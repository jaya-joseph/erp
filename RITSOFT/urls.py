"""RITSOFT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from RITSOFT_APP import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # account urls
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_redirect, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # admin urls
    path('admin_home/', views.admin_home, name='admin_home'),

    path('designation/', views.designation, name='designation'),
    path('fetch_faculty/', views.fetch_faculty_of_dept, name='fetch_faculty'),
    path('fetch_designation/', views.fetch_designation_of_faculty, name='fetch_designation'),

    path('add_academic_year/', views.add_academic_year, name='add_academic_year'),
    path('change_academic_year/', views.change_academic_year, name='change_academic_year'),

]
