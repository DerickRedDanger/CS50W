from django.urls import path,include
from . import views

app_name = 'appointment'
urlpatterns = [
    path('index/',views.index, name='index'),
    path('new/',views.new_event, name='new_event'),
    path('dailytask/',views.dailytask, name='dailytask'),
    path('listtodo/',views.listtodo, name='listtodo'),
    path('planner',views.planner, name='planner'),
    path('calendar/<int:month>/<int:year>',views.calendar, name='calendar'),
    path('test/', views.test, name='test') ,
    path('event/<int:id>',views.event, name='event'),
    path('daily/<int:id>',views.daily, name='daily'),
    path('todo/<int:id>',views.todo, name='todo'),
]
