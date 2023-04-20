"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
            template_name='accounts/login.html',
            redirect_authenticated_user=True),
         name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_page, name='signup'),
    path('flux/', views.flux, name='flux'),
    path('ticket/', views.ticket_create, name='ticket'),
    path('ticket/<int:ticket_id>/edit', views.ticket_edit, name='ticket_edit'),
    path('posts/', views.posts, name='posts'),
    path('posts/<str:post_type>/<int:post_id>/edit', views.post_edit, name='post_edit'),
    path('posts/<str:post_type>/<int:post_id>/del', views.post_delete, name='post_delete'),
    path('abonnements/', views.abonnements, name='abonnements'),
    path('abonnements/<int:follow_id>', views.unfollow, name='unfollow')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
