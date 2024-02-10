from django.urls import path
from studentapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('status', views.status, name='status'),
    path('score', views.score, name='score'),
    path('editprofile', views.editprofile, name='edit'),
    path('appointment', views.appointment, name='appo'),
    path('appointment/<int:year>/<int:month>/', views.appointment, name='appo'),
    path('appointment/<int:year>/<int:month>/<int:day>/', views.appointment_time_select, name='app_time'),
    path('appointment_details/<int:year>/<int:month>/<int:day>/<str:start_time>/<str:end_time>/', views.appointment_details, name='app_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)