from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('mysite/login/', views.login_view, name='login'), 
    path('mysite/logout/', views.logout_view, name='logout'),
    path('mysite/register/', views.register, name='register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)