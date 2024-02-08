from django.urls import path
from studentapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login', views.login_view, name='login'), 
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('status', views.status, name='status'),
    path('score', views.score, name='score'),
    path('editprofile', views.editprofile, name='editprofile'),
    path('appointment', views.appointment, name='appointment'),
    path('appointment/<int:year>/<int:month>/', views.appointment, name='appointment'),
    path('appointment/<int:year>/<int:month>/<int:day>/', views.appointment, name='appointment'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)