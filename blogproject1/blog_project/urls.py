"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from blog import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.post_list_view,name='home'),
    path('home/', views.post_list_view),
    path('<str:tag_slug>', views.post_list_view,name='post_list'),
    path('signup/', views.signup_view),
    path('logout/', views.logout_view),
    path('userposts/<int:author_id>/', views.user_post,name='userposts'),
    path('share/<int:id>', views.mail_send_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('<int:year>/<int:month>/<int:day>/<str:post>', views.post_detail_view,name='post_detail'),
    path('dashboard/', views.dashboard_view),
    path('createpost/', views.createpost_view),
    path('delete/<str:slug>', views.deletepost_view),
    path('update/<str:slug>', views.updatepost_view),
]
