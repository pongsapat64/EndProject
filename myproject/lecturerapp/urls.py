from django.urls import path
from lecturerapp import views

urlpatterns = [
    path('mainpage', views.mainpage, name='main'),
    path('editprofile', views.editprofile, name='editlec'),
    path('addtime', views.addtime, name='addtime'),
    path('addthetime', views.create_freetime, name='addthetime'),
    path('get_freetime/', views.get_freetime, name='get_freetime'),
    path('addtime/<int:year>/<int:month>/', views.addtime, name='addtime'),
    path('addtime/<int:year>/<int:month>/<int:day>/', views.addtime_select, name='addtime_time'),
    path('history', views.history, name='history'),
    path('givescore/<int:id>', views.give_score, name='givescore'),
    path('showstudents', views.show_student, name='showstudents'),
]