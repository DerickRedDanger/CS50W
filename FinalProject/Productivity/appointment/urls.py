from django.urls import path,include
from . import views

app_name = 'appointment'
urlpatterns = [
    path('index/',views.index, name='index'),
    path('old/<int:id>',views.event_outdated, name='event_outdated'),
    path('dailytask/<int:id>',views.dailytask, name='dailytask'),
    path('listtodo/<int:id>',views.listtodo, name='listtodo'),
    path('planner',views.planner, name='planner'),
    path('calendar/<int:month>/<int:year>',views.calendar, name='calendar'),
    path('test/', views.test, name='test') ,
    path('event/<int:id>',views.event, name='event'),
    path('daily/<int:id>',views.daily, name='daily'),
    path('todo/<int:id>',views.todo, name='todo'),
]
