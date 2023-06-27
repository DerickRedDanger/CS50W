from django.shortcuts import render

# Create your views here.

from datetime import datetime,timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from . import models
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
    return render(request, "New_event.html",{"event":event,"error":error})

    #if request.method == "GET":
     #   context={}
     #   form = forms.eventForm
      #  context['form']=form

def dailytask(request):
    error = ""
    task = forms.DailyTaskForm(request.POST or None)
    if request.method == "POST":
        name = request.POST['task']
        weekday = request.POST['weekday']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        quick_description = request.POST['quick_description']
        description = request.POST['description']
        notes = request.POST['notes']
        urgency = request.POST['urgency']
        importance = request.POST['importance']
        print(f"name = {name}, weekday = {weekday}, Start = {start_time}, end = {end_time}, quick ={quick_description}, description = {description}, notes = {notes}, urgency = {urgency}, importance = {importance}")

    # checking if there is there is a overlap with another task, but ignoring if overlaps with itself:
        for day in weekday:

            # cheking if this task is being edited, not created.
            # if it is, ignore self in the filter.
            try:
                tasks = models.DailyTask.objects.filter(weekday=day).exclude(id=self.id)
            except:
                tasks = models.DailyTask.objects.filter(weekday=day)
            if tasks.exists():
                for test in tasks:
                    if check_overlap(test.start_time, test.end_time, start_time ,end_time):
                        # raise snackbar/toast
                        error = f' There is an overlap with another task: {test.task}, {test.start_time} - {test.end_time}) on the weekday {day}'
                        break
            if error=="":
                # models.DailyTask.objects.create(
                    # saving the new task
                new = models.DailyTask(task=name,start_time=start_time,
                    end_time=end_time,quick_description=quick_description,
                    description=description,notes=notes,urgency=urgency,
                    importance=importance)
                new.save()
                # adding the weekdays, since it raises a error if added without first saving
                new.weekday.add(weekday)
                
    return render(request,"dailytask.html",{"task":task,"error":error})

def check_overlap( fixed_start, fixed_end, new_start, new_end):
        overlap = False
        new_start = datetime.strptime(new_start, '%H:%M').time() 
        new_end = datetime.strptime(new_end, '%H:%M').time() 
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
 
        return overlap

def listtodo(request):
    error = ""
    todo = forms.ListToDoForm(request.POST or None)
    alltodo = models.ListToDo.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        quick_description = request.POST['quick_description']
        description = request.POST['description']
        # steps = request.POST['Steps'] Steps = {steps},
        notes = request.POST['notes']
        duration = request.POST['duration']
        urgency = request.POST['urgency']
        importance = request.POST['importance']
        progress = request.POST['progress']
        print(f"name = {name}, progress = {progress},  duration = {duration}, quick ={quick_description}, description = {description}, notes = {notes}, urgency = {urgency}, importance = {importance}")
        print("todo")
        print(todo)
        listtd = models.ListToDo.objects.filter(name=name)
        print(listtd.count())
        if not listtd.exists():
            todo.save()
            todo = forms.ListToDoForm(None)

    return render(request,"draft.html",{"alltodo":alltodo,"todo":todo,"error":error})

