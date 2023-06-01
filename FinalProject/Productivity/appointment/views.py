from django.shortcuts import render

# Create your views here.

from datetime import datetime,timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import *
from .utils.calendarutils import Calendar
from . import forms

def index(request):
    return HttpResponse('hello')


def calendar(request,year=None, month=None):
    if request.method == "GET":
        # use today's date for the calendar
        d = datetime.today()

        context={}
        

        # Initiate our calendar class with today's year and date
        cal = Calendar(year,month)

        # Call the formatmonth method, which returns our calendar as a table
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        
        prev_m= month-1
        if prev_m==0:
            prev_m = 12
            p_year = year - 1
        else:
            p_year=year

        next_m= month+1
        if next_m==13:
            next_m = 1
            n_year = year + 1
        else:
            n_year=year

        context['previous']=prev_m
        context['p_year']=p_year
        context['next']=next_m
        context['n_year']=n_year

        return render(request, "calendar.html",{"context":context})

    else:
        return HttpResponseRedirect(reverse("index"))

def new_event(request):
    error=""
    event = forms.eventForm(request.POST or None)
    if request.method == "POST":
        print("post")
        if event.is_valid():
            event.save()
            event = forms.eventForm
        else:
            print("something went wrong")
            error = "something went wrong"
    return render(request, "new_event.html",{"event":event,"error":error})

    
    #if request.method == "GET":
     #   context={}
     #   form = forms.eventForm
      #  context['form']=form

    