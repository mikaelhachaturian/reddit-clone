from django.contrib import admin
from django.urls import path, include
from . import views
from accounts.views import login_view, register_view, logout_view

urlpatterns = [
    path('', views.home, name='homepage'),
    path('<int:post_id>/<str:vote_type>', views.home, name='homepage'),
    path('admin/', admin.site.urls),
    path('r/', include('subreddits.urls')),
    path('accounts/login/', login_view, name='login_view'),
    path('accounts/register/', register_view, name='register_view'),
    path('accounts/logout/', logout_view, name='logout_view')
]
