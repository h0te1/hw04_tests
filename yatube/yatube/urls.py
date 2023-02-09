from django.contrib import admin
from django.urls import path, include
# from . import views

urlpatterns = [
    path('', include('posts.urls', namespace='posts')),
    path('auth/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('about.urls', namespace='about')),
]
