from django.urls import path
from lecturerapp import views

urlpatterns = [
    path('mainpage', views.mainpage, name='main'),
    path('editprofile', views.editprofile, name='editlec'),
    path('addtime', views.addtime, name='addtime'),
    path('history', views.history, name='history'),
]