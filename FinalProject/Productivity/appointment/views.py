from django.shortcuts import render

# Create your views here.

from datetime import datetime,timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from . import models
from .utils.calendarutils import Calendar
from . import forms
from . import models_auto_functions
from django.forms.models import model_to_dict

now = datetime.now().date()

# Checking the date to decide if it's time to do all the auto functions.
last_checkup=models.datetracking.objects.get(id=1).day

# --------
# Check if it's been a day since last autofunction
try:
    y = datetime(now.year, now.month, now.day+1).date()
except ValueError:
    # in case today's the last day of a month
    try:
        y = datetime (now.year, now.month + 1, 1).date()
    # in case today's the last day of the year
    except ValueError:
        y = datetime (now.year+1, 1, 1).date()
print("auto test")
print("all good till here 1")

# if the time difference between now and last check up is more than one day
if (now - last_checkup) >= (y-now):
    print("all good till here 2")
    # do all Auto functions:
    #-------------------

#-------------------- Models.listtodo - auto urgency update --------------------
auto = models_auto_functions.listtodo_urgency_auto_update(now)

#-------------------- Models.event-forever - auto repetitions creation --------------------
auto = models_auto_functions.event_forever_repeat_creation(now)

#how old (in years) should the repetitions/events be before being deleted
years = 3

#-------------------- Models.event-Nonforever - auto delete --------------------
auto = models_auto_functions.event_ForeverRepetitions_auto_delete(years)
#-------------------- Models.event-forever - repetition auto delete --------------------
auto = models_auto_functions.event_NonForever_auto_delete(years)

weekday=[]
weekdays = models.WeekDay.objects.all()
for x in weekdays:
        weekday.append((x.day,x.id))

weekday = tuple (weekday)


#print(weekdays)
#weekdays=[("Sunday",2) ,("Monday",3),("Tuesday",4),("Wednesday",5),("Thursday",6), ("Friday",7), ("Saturday",8)]

repeat_choices = [
        ('nvr', 'never'),
        ('dly', 'daily'),
        ('wek', 'weekly'),
        ('mth', 'monthly'),
        ('yea', 'yearly'),
        ('wkd', 'specific weekdays'),
    ]

priority_choices = [
        ('veryhight', 'Essential'),
        ('high', 'important'),
        ('medium', 'desirable'),
        ('low', 'Curiosity/interest'),
        ('verylow','trivial'),
        ('circumstantial','circumstantial')
    ]

hours = {5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}
minutes = ('00','15','30','45',)
start=[]
end=[]
for hour in hours:
    for minute in minutes:
        if hour == 5 and minute == "00":
                pass
        else:
                end.append(f"{hour}:{minute}")
        if hour == 23 and minute == "45":
                pass
        else:
            start.append(f"{hour}:{minute}")
leng=len(start)
#print(start)





def index(request):
    x = datetime.now()
    print(x)
    error = ""
    alltodo = models.ListToDo.objects.all()
    today = models.WhatToDoToday.objects.filter(day=x).order_by('start_time')
    print(today)
    

    return render(request,"index.html",{"alltodo":alltodo,'today':today,"error":error,"start":start, "end":end,"leng":leng,"repeat_choices":repeat_choices,"priority_choices":priority_choices,})

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

def event(request,id):
    error=""
    date = None
    start_time = None
    end_time = None
    dateu=None
    if request.method == "GET":
        if id != 0:
            obj = models.Event.objects.get(id = id)

            event = forms.eventForm(instance = obj)

        else:
            obj = models.Event(None)
            event = forms.eventForm(None)

    if request.method == "POST":
        if id != 0:
            obj = models.Event.objects.get(id = id)
            event=forms.eventForm(request.POST,instance = obj)
        else:
            event=forms.eventForm(request.POST)
        if event.is_valid():
            print("event is valid")
            event.save()
            event = forms.eventForm

            if id != 0:
                event = forms.eventForm(instance = obj)
            else:
                obj = models.Event(None)
                event = forms.eventForm(None)  

        # if event wasn't valid
        else:
            print("something went wrong")
            error = "something went wrong"

            date = request.POST['day']
            dateu = request.POST['repeatutil']

    try: 
        if obj.day:
            print(f"obj.day = {obj.day}")
            date=obj.day.strftime("%Y-%m-%d")
            start_time = obj.start_time.strftime("%H:%M")
            end_time = obj.end_time.strftime("%H:%M")
    
    except:
        print("no obj.day")
        

    try:

        if obj.repeatutil:
            dateu=obj.repeatutil.strftime("%Y-%m-%d")
    except:
        print("no obj.repeatutil")
    
    # returns the html with the empty form is through GET or a correct POST
    # returns with the filled post if event wasn't valid to make it easier to fix.
    # return render(request, "forms.html",{"event":event,"start":start,"end":end,"error":error,"weekday":weekday,"repeat_choices":repeat_choices,"priority_choices":priority_choices,})
    return render(request, "event.html",{"event":event,"id":id,"start_time":start_time,"end_time":end_time,"date":date,"dateu":dateu,"start":start,"end":end,"error":error,"weekday":weekday,"repeat_choices":repeat_choices,"priority_choices":priority_choices,})

    #if request.method == "GET":
     #   context={}
     #   form = forms.eventForm
      #  context['form']=form

def dailytask(request,id):


    if request.method == "GET":
        if id != 0:
            obj = models.DailyTask.objects.get(id = id)
            form = forms.DailyTaskForm(instance = obj)
        else:
            obj = models.DailyTask(None)
            form = forms.DailyTaskForm(None)

    if request.method == "POST":
        form=forms.DailyTaskForm(request.POST)
        if form.is_valid():
            print("Dailytask is valid")
            form.save()
            form = forms.DailyTaskForm

    snack=""
            #if id == 0 :
            #    snack =f"The task {task.title} has been created"
            #else : 
            #    snack =f"The task {task.title} has been saved"
            
    return render(request,"daily.html",{"form":form,"start":start,"end":end,
                                            "repeat_choices":repeat_choices,"priority_choices":priority_choices,
                                            "snack":snack,"id":id,})

def listtodo(request,id):
    print(f"todo id = {id}")
    if request.method == "GET":
        if id != 0:
            obj = models.ListToDo.objects.get(id = id)
            form = forms.ListToDoForm(instance = obj)
        else:
            obj = models.ListToDo(None)
            form = forms.ListToDoForm(None)

    if request.method == "POST":
        if id != 0:
            obj = models.ListToDo.objects.get(id = id)
            form=forms.ListToDoForm(request.POST,instance = obj)
        else:
            form=forms.ListToDoForm(request.POST)
        if form.is_valid():
            print("ListToDo is valid")
            form.save()
            form = forms.ListToDoForm

            if id != 0:
                obj =models.ListToDo.objects.get(id = id)
                form = forms.ListToDoForm(instance = obj)
            else:
                obj = models.ListToDo(None)
                form = forms.ListToDoForm(None) 

        else:
            print("'list to do' form is not valid")
    try: 
        if obj.deadline_date:
            print(f"obj.day = {obj.deadline_date}")
            deadline_date=obj.deadline_date.strftime("%Y-%m-%d")
        else:
            deadline_date=None
    except:
        deadline_date=None
        print("no obj.day")
    snack=""


    return render(request,"todo.html",{"id":id,"snack":snack,"form":form,"repeat_choices":repeat_choices,"priority_choices":priority_choices,"deadline_date":deadline_date})

def planner(request):
    x = datetime.now()
    data={}
    # Getting the ListToDo itens.
    alltodo = models.ListToDo.objects.all()
    alllist= []
    N=0
    for n in alltodo:
        data[f"all{N}"]= n.serialize()
        alllist.append(f"all{N}")
        N=N+1
    data['alllist']= alllist

    # Querysets can't be JSON serialized
    # so it had to be done manually

    # Getting WhatToDoToday itens.
    today = models.WhatToDoToday.objects.filter(day=x).order_by('start_time')
    todaylist= []
    N=0
    for n in today:
        data[f"today{N}"]= n.serialize()
        todaylist.append(f"today{N}")
        N=N+1
    data['todaylist']= todaylist

    # Getting DailyTask itens.
    weekday = x.strftime("%w")
    if weekday == "0":
        daily = models.DailyTask.objects.filter(sunday=True).order_by('start_time')
    elif weekday == "1":
        daily = models.DailyTask.objects.filter(monday=True).order_by('start_time')
    elif weekday == "2":
        daily = models.DailyTask.objects.filter(tuesday=True).order_by('start_time')
    elif weekday == "3":
        daily = models.DailyTask.objects.filter(wednesday=True).order_by('start_time')
    elif weekday == "4":
        daily = models.DailyTask.objects.filter(thursday=True).order_by('start_time')
    elif weekday == "5":
        daily = models.DailyTask.objects.filter(friday=True).order_by('start_time')
    elif weekday == "6":
        daily = models.DailyTask.objects.filter(saturday=True).order_by('start_time')
        
    dailylist= []
    N=0
    for n in daily:
        data[f"daily{N}"]= n.serialize()
        dailylist.append(f"daily{N}")
        N=N+1
    data['dailylist']= dailylist

    # Getting Event itens.
    event = models.Event.objects.filter(day=x).order_by('start_time')
    eventlist= []
    N=0
    for n in event:
        data[f"event{N}"]= n.serialize()
        eventlist.append(f"event{N}")
        N=N+1
    data['eventlist']= eventlist

    # Getting EventRepetition itens.
    revent = models.EventRepetiton.objects.filter(day=x).order_by('start_time')
    reventlist= []
    N=0
    for n in revent:
        data[f"revent{N}"]= n.serialize()
        reventlist.append(f"revent{N}")
        N=N+1
    data['reventlist']= reventlist

    error = ""
    hours = {5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}
    minutes = ('00','15','30','45',)
    start=[]
    end=[]
    for hour in hours:
        for minute in minutes:
            if hour == 5 and minute == "00":
                pass
            else:
                end.append(f"{hour}:{minute}")
            if hour == 23 and minute == "45":
                pass
            else:
                start.append(f"{hour}:{minute}")
    
    leng=[]
    for n in range(len(start)):
        leng.append(n)
    
    print(f"leng = {leng}")
    print(start)
    print(end)

    #data['alltodo'] = alltodo
    #data['todo_today'] = today
    data['s'] = start
    data['e'] = end
    data['leng'] = leng
    #data['daily_today'] = daily
    #data['event_today'] = event
    #data['repeated_event_today'] = revent
    data['error'] = error
    
    return JsonResponse(data)
    

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

def test(request):
    Snackbar = "This is a success"
    alert = "success"

    return render(request, "test.html",{"Snackbar":Snackbar, "alert":alert})

def event_outdated(request,id):
    error=request.POST or None
    # variable to decide to where the submit button will post.
    # if Id = 0, it will lead back to a empty form so another event can be crate
    # if id != 0, will lead back to the page of the edited event.
    if id == 0:
        event=[]
        # the below is used when an event is not validated, so they are set to null for now
        thisweekday =""
        start_time=""
        end_time=""
        dateu=""
        date=""
        if request.method == "POST":
            event = forms.eventForm(request.POST or None)
            print(f"form = {event}")

            if event.is_valid():
                event.save()
                event = []

            # if event wasn't valid
            else:

                event=models.Event()
                event.title = request.POST['title']
                event.day = request.POST['day']
                event.start_time = request.POST['start_time']
                event.end_time = request.POST['end_time']
                event.description = request.POST['description']
                event.notes = request.POST['notes']
                event.repeat = request.POST['repeat']
                print("wkd")
                print((request.POST.getlist('repeat_wkd')))
                wkdlist=(request.POST.getlist('repeat_wkd'))
                event.repeatd = request.POST['repeatd']
                event.repeatutil = request.POST['repeatutil']
                event.repeatnumber = request.POST['repeatnumber']
                event.color=request.POST['color']


                thisweekday=[]

                    #creates a variable to check if the loop appended the day to the list
                k = 1

                    # for day and id in weekday
                for d,n in weekday:

                    # for weekdays selected in the events
                    for x in wkdlist:
                        print(f" n = {n} and x = {x}")
                        # if the weekday Id is equal to one selected
                        if int(n) == int(x):
                            # append it to the list with a 1 (selected) at the end and set K = 0
                            thisweekday.append((d,n,1))
                            k = 0
                            print("added")
                    # if none of the weekdays selected is equal to the weekday in question
                    if k == 1 :
                        # append it to the list, with a 0 (not seletected) at the end
                        thisweekday.append((d,n,0))
                        print("not added")
                    # resets K to 1 at the end of the loop.
                    k = 1

                # converts the list to a proper tuple to be used in the html
                thisweekday = tuple (thisweekday)
                print(f"thisweekday = {thisweekday}")

                print(f"event.day = {event.day}")
                y = event.day
                year = f"{y[0]}{y[1]}{y[2]}{y[3]}"
                month = f"{y[5]}{y[6]}"
                day= f"{y[8]}{y[9]}"
                #date = datetime.datetime(year,month,day)
                #day=event.day.strftime("%d")
                #month=event.day.strftime("%m")
                #year=event.day.strftime("%Y")
                #print(f"{year}-{month}-{day}")
                print(event.day)
                print(f"date {year} - {month} - {day}")
                date=f"{year}-{month}-{day}"
                print(f"date = {date}")
                if event.repeatutil:
                    y = event.repeatutil
                    year = f"{y[0]}{y[1]}{y[2]}{y[3]}"
                    month = f"{y[5]}{y[6]}"
                    day= f"{y[8]}{y[9]}"
                    dateu =f"{year}-{month}-{day}"
                else:
                    dateu=""
                print(f"start_time = {event.start_time}")
                print(f"lengt of start_time = {len(event.start_time)}")
                if len(event.start_time) == 4:
                    y = event.start_time
                    start_time= f'{y[0]}:{y[2]}{y[3]}'
                else:
                    y = event.start_time
                    start_time= f'{y[0]}{y[1]}:{y[3]}{y[4]}'

                if len(event.end_time) == 4:
                    y = event.end_time
                    end_time= f'{y[0]}:{y[2]}{y[3]}'
                else:
                    y = event.end_time
                    end_time= f'{y[0]}{y[1]}:{y[3]}{y[4]}'

                
                nevent = forms.eventForm(request.POST or None)
                #print (f"nevent1 = {nevent}")



                print("something went wrong")
                error = "something went wrong"

        # returns the html with the empty form is through GET or a correct POST
        # returns with the filled post if event wasn't valid to make it easier to fix.
        return render(request, "event_outdated2.html",{"event":event,"start":start,"end":end,"error":error,
                    "thisweekday":thisweekday,"start_time":start_time,"end_time":end_time, "dateu":dateu, "date":date,})
    else:
        event=models.Event.objects.get(id=id)
        day=event.day.strftime("%d")
        month=event.day.strftime("%m")
        year=event.day.strftime("%Y")
        #print(f"{year}-{month}-{day}")
        date=f"{year}-{month}-{day}"
        if event.repeatutil:
            dateu = f'{event.repeatutil.strftime("%Y")}-{event.repeatutil.strftime("%m")}-{event.repeatutil.strftime("%d")}'
        else:
            dateu=""

        start_time = f'{event.start_time.strftime("%H")}:{event.start_time.strftime("%M")}'
        end_time = f'{event.end_time.strftime("%H")}:{event.end_time.strftime("%M")}'
        
        nevent = forms.eventForm(request.POST or None)
        #print (f"nevent1 = {nevent}")

        if request.method == "POST":

            # Since an error ocours when repeatutil isn't a date normalise it to today's date.
            # it doesn't affect the  models, as if repeatutil wasn't a date
            # it means it wasn't being used to begin with.
            if dateu=="":
                dateu = datetime.now()

            event.title = request.POST['title']
            event.day = request.POST['day']
            event.start_time = request.POST['start_time']
            event.end_time = request.POST['end_time']
            event.description = request.POST['description']
            event.notes = request.POST['notes']
            event.repeat = request.POST['repeat']
            event.repeat_wkd.set(request.POST.getlist('repeat_wkd'))
            event.repeatd = request.POST['repeatd']
            event.repeatutil = dateu
            event.repeatnumber = request.POST['repeatnumber']
            event.color=request.POST['color']
            #print(f"event.repatutil = {event.repeatutil}")


            #event=event(title=title,day=day,start_time=start_time,end_time=end_time,description=description,notes=notes,repeat=repeat,repeat_wkd=repeat_wkd,repeatd=repeatd,repeatutil=repeatutil, repeatnumber=repeatnumber,color=color,)
            event.save()

            #------------------------
            #It's working so far, but gotta delete and recreate all repetitions
            #
            #
            #--------------------------




            #nevent = forms.eventForm(request.POST or None)
            #print (f"event2 = {event}")
            #if event.is_valid():
            #    event.save()
            #    event = forms.eventForm(request.POST or None)
            #    print("ok")
            #else:
            #    event = forms.eventForm(request.POST)
            #    #print("something went wrong")
            #    print(f'ValidationError = {event.ValidationError}')
            #    error = "something went wrong"
            #    print(error)

        if request.method == "GET":
            event=models.Event.objects.get(id=id)
            error = ""

        # checking which weekdays were selected

            # create a empty list to hold the tuples   
        thisweekday=[]

            #creates a variable to check if the loop appended the day to the list
        k = 1

            # for day and id in weekday
        for d,n in weekday:

            # for weekdays selected in the events
            for x in event.repeat_wkd.all():
                # if the weekday Id is equal to one selected
                if n == x.id:
                    # append it to the list with a 1 (selected) at the end and set K = 0
                    thisweekday.append((d,n,1))
                    k = 0
            # if none of the weekdays selected is equal to the weekday in question
            if k == 1 :
                # append it to the list, with a 0 (not seletected) at the end
                thisweekday.append((d,n,0))
            # resets K to 1 at the end of the loop.
            k = 1

        # converts the list to a proper tuple to be used in the html
        thisweekday = tuple (thisweekday)

        print(f"This is weekday = {thisweekday}")

        return render(request,"event_outdated2.html",{"start":start,"end":end,"start_time":start_time,
                    "end_time":end_time,"event":event,"date":date,"error":error,"thisweekday":thisweekday,
                     "dateu":dateu,})

def daily(request,id):
    error=""
    task=models.DailyTask.objects.get(id=id)
    day=event.day.strftime("%d")
    month=event.day.strftime("%m")
    year=event.day.strftime("%Y")
    #print(f"{year}-{month}-{day}")
    date=f"{year}-{month}-{day}"

    if request.method == "Post":
        if event.is_valid():
            event.save()
            event = forms.eventForm(request.POST or None)
        else:
            #print("something went wrong")
            print(f'ValidationError = {event.ValidationError}')
            error = "something went wrong"

    if request.method == "GET":
        event=models.Event.objects.get(id=id)
        error = ""
    return render(request,"event.html",{"event":event,"date":date,"error":error})

def todo(request,id):
    error=""
    event=models.Event.objects.get(id=id)
    day=event.day.strftime("%d")
    month=event.day.strftime("%m")
    year=event.day.strftime("%Y")
    #print(f"{year}-{month}-{day}")
    date=f"{year}-{month}-{day}"

    if request.method == "Post":
        if event.is_valid():
            event.save()
            event = forms.eventForm(request.POST or None)
        else:
            #print("something went wrong")
            error = "something went wrong"

    if request.method == "GET":
        event=models.Event.objects.get(id=id)
        error = ""
    return render(request,"event.html",{"event":event,"date":date,"error":error})





