from django.urls import path
from lecturerapp import views

urlpatterns = [
    path('mainpage', views.mainpage, name='main'),
    path('editprofile', views.editprofile, name='editlec'),
    path('addtime', views.addtime, name='addtime'),
    path('addtime/<int:year>/<int:month>/', views.addtime, name='addtime'),
    path('addtime/<int:year>/<int:month>/<int:day>/', views.addtime_select, name='addtime_time'),
    path('history', views.history, name='history'),
]