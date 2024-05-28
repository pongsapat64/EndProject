from django.urls import path
from mysite import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('read/', views.read_user, name='read'),
    path('create/', views.create_user, name='create'),
    path('create_adviser/', views.create_adviser, name='create_adviser'),
    path('update/<int:id>/', views.update_user, name='update'),
    path('delete/<int:id>/', views.delete_user, name='delete'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('mainpage', views.mainpage, name='main'),
    path('profileLec', views.profileLec, name='profileLec'),
    path('addtime', views.addtime, name='addtime'),
    path('addthetime', views.create_freetime, name='addthetime'),
    path('showAvailableTime', views.showAvailableTime, name='showavt'),
    path('deleteAvailableTime/<int:id>', views.deleteAvailableTime, name='deleteavt'),
    path('get_freetime/', views.get_freetime, name='get_freetime'),
    path('history', views.history, name='history'),
    path('givescore/<int:id>', views.give_score, name='givescore'),
    path('showstudents', views.show_student, name='showstudents'),
    path('status', views.status, name='status'),
    path('score', views.score, name='score'),
    path('profile', views.profile, name='profile'),
    path('show_committee', views.show_committee, name='show_committee'),
    path('create_event', views.create_google_calendar_event, name='create_event'),
    path('create_event2', views.create_google_calendar_event2, name='create_event2'),
    path('appointment', views.appointment, name='appo'),
    path('create_project', views.create_project, name='create_project'),
    path('project_detail', views.project_detail, name='project_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
