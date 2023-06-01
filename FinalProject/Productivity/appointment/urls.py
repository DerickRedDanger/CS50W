from django.urls import path,include
from . import views

app_name = 'appointment'
urlpatterns = [
    path('index/',views.index, name='index'),
    path('new/',views.new_event, name='new_event'),
    path('calendar/<int:month>/<int:year>',views.calendar, name='calendar'),
]
