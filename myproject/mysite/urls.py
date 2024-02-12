from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('read/', views.read_user, name='read'),
    path('create/', views.create_user, name='create'),
    path('update/<int:id>/', views.update_user, name='update'),
    path('delete/<int:id>/', views.delete_user, name='delete'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)