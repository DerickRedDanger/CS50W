from django.shortcuts import render

# Create your views here.

from datetime import datetime,timedelta
from django.views import generic
from django.utils.safestring import mark_safe
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from . import models
from .utils.calendarutils import Calendar
from . import forms


# Checking the date to decide if it's time to do all the auto functions.
last_checkup=models.datetracking.objects.get(id=1).day
x = datetime.now().date()
# --------
# Remember to switch this back to month + 1
try:
    y = datetime(x.year, x.month, x.day+1).date()
except ValueError:
    try:
        y = datetime (x.year, x.month + 1, 1).date()
    except ValueError:
        y = datetime (x.year+1, 1, 1).date()
print("auto test")
if (x - last_checkup) >= (y-x):

    # All Auto functions:
    #-------------------

    #------------------------ testing the auto functions
    All_Forever_Event = models.Event.objects.filter(repeatd = "frv").exclude(repeat="nvr")
    print(len(All_Forever_Event))
    if len(All_Forever_Event) != 0 :
        for y in range(len(All_Forever_Event)):
            
            x = All_Forever_Event[y]
            print (f"event = {x}")
            All_Forever_Repetition = x.Repetitions.all()
            print(f"All repetitions from event x = {All_Forever_Repetition}")
            if len(All_Forever_Repetition) != 0 :
                print("from repetition")
                z = All_Forever_Repetition[len(All_Forever_Repetition)-1].day
                Last_repetition = datetime(z.year, z.month, z.day)
            else:
                print("from event.day")
                Last_repetition = datetime(x.day.year, x.day.month, x.day.day) 
                #print(Last_repetition)
            today = datetime.now()
            Two_Years_From_Today = datetime(today.year + 2, today.month, today.day)
            print(f'last_repetition = {Last_repetition}')
            print(f'today = {today}')
            print(f'two years from today = {Two_Years_From_Today}')
            print ( f" ({Last_repetition} - {today}) <= ({Two_Years_From_Today} - {today})")
            if (Last_repetition - today) <= (Two_Years_From_Today - today):
                print(f"x = {x}")
                dayf = datetime(today.year+2, Last_repetition.month, Last_repetition.day)
                dayi = datetime(Last_repetition.year, Last_repetition.month, Last_repetition.day)

                # If weekdays was selected, get the selected weekdays from the original event.
                #if x.repeat =="wkd":
                #            weekdays=x.repeat_wkd.all()
                #            print(f"weekdays = {weekdays}")
                #            week=[]
                #            for x in range(len(weekdays)):
                #                week.append(weekdays[x].day)
                #            print(f"week = {week}")

                # while the date in question isn't higher than he final date
                while(dayi<= dayf):
                                print(f'dayi = {dayi}')
                                print(f'dayf = {dayf}')

                                # since it's starting on the same day as the event, 
                                # i have to skip that initial day.
                                if dayi!=Last_repetition and dayi>=today:

                                    print(f"dayi != last {dayi} != {Last_repetition}")

                                    # if specific week days was selected
                                    #if x.repeat=='wkd':
                                    #    print(f'dayi = {dayi.strftime("%A")}')

                                    #    # check if the weekday in question was one of the selected.
                                    #    if dayi.strftime("%A") in week:

                                            # if it's create a new repetition and save.
                                    #        new = models.EventRepetiton(original=x, day=dayi,
                                    #        start_time=x.start_time, end_time=x.end_time)
                                    #        print(f'new = {new}')
                                    #        new.save()
                                    
                                    # if it's not the initial day and it's not set to repeat on specific weekdays
                                    # than this is a day that event is meant to be created.
                                    #else:
                                    new = models.EventRepetiton(original=x, day=dayi,
                                    start_time=x.start_time, end_time=x.end_time)
                                    new.save()

                                # If set to repeat weekly, montly or yearly
                                # increase the day by 7 or month/year by 1
                                #if x.repeat =="wek":
                                #    dayi=dayi+timedelta(days=7)
                                #    print(f'wek - dayi = {dayi}')
                                

                                # If ser to repeat monthly, increase month by 1
                                if x.repeat =="mth":
                                    try :
                                        dayi=datetime(dayi.year, dayi.month+1, dayi.day)
                                        print(f'mth - dayi = {dayi}')
                                        
                                        # if this doesn't work
                                    except:

                                        # check if it's the end of the year, on which case month would end up being 13
                                        if (dayi.month + 1) == 13:

                                            # if it's, than month will be 1 and year will be year + 1
                                            dayi=datetime(dayi.year+1, 1, dayi.day)
                                            print(f'mth - dayi = {dayi}')

                                            # In cases where the day doesn't exist in that month, 
                                            # like 31 in a month with 30 days or 30 in frebuary
                                            # skip to next month, as there are no months in a row that ends in 30 or lower
                                        else:
                                            try:
                                                dayi=datetime(dayi.year, dayi.month+1, dayi.day)
                                                print(f'mth - dayi = {dayi}')
                                            except ValueError:
                                                dayi=datetime(dayi.year, dayi.month+2, dayi.day)
                                                print(f'mth - dayi = {dayi}')
                                
                                # if ser to repeat yearly, increase year by 1
                                elif x.repeat =="yea":
                                    try:
                                        dayi=datetime(dayi.year+1, dayi.month, dayi.day)
                                        print(f'yea - dayi = {dayi}')

                                        # if the day in question is 29th february:
                                    except ValueError:
                                        if dayi.day == '29' and dayi.month == "02":
                                            dayi=datetime(dayi.year+4, dayi.month, dayi.day)

                                # if it's none of the above, it was set to daily,
                                # so increase day by 1
                                
                                
                                #else:
                                #    dayi=dayi+timedelta(days=1)
                                #    print(f'day - dayi = {dayi}')

    #AllForeverEvent = models.Event.objects.filter(repeatd = "frv")
    
    # Get all events that aren't set to repeat forever.
    All_Non_Forever_Events = models.Event.objects.all().exclude(repeatd = "frv")| models.Event.objects.all().filter(repeat='nvr').filter(repeatd = "frv")
    print(len(All_Non_Forever_Events))

    # If there are events of that kind.
    if len(All_Non_Forever_Events) != 0 :

        # Run through each of them
        for y in range(len(All_Non_Forever_Events)):
            x = All_Non_Forever_Events[y]
            print (f"event = {x}")

            # and check if they have repetitions
            All_Non_Forever_Events_Repetition = x.Repetitions.all()
            print(f"All repetitions from event x = {All_Non_Forever_Events_Repetition}")
            
            # If they do, get the latest one. (the one more in the "future")
            if len(All_Non_Forever_Events_Repetition) != 0 :
                print("from repetition")
                z = All_Non_Forever_Events_Repetition[len(All_Non_Forever_Events_Repetition)-1].day
                Last_repetition = datetime(z.year, z.month, z.day)
            
            # if they don't, get the event's date.
            else:
                print("from event.day")
                Last_repetition = datetime(x.day.year, x.day.month, x.day.day) 
                #print(Last_repetition)
            
            # Get today's date and the date of 3 years in the future
            today = datetime.now()
            Three_Years_From_Today = datetime(today.year + 3, today.month, today.day)
            print(f'last_repetition = {Last_repetition}')
            print(f'today = {today}')
            print(f'two years from today = {Two_Years_From_Today}')
            print ( f" ({Last_repetition} - {today}) <= ({Two_Years_From_Today} - {today})")
            print (f"{Last_repetition - today} >= {Three_Years_From_Today - today}")
            
            # check if the latest repetitions or the event is older than 3 years.
            if (today - Last_repetition ) >= (Three_Years_From_Today - today):
                print(f"this event {x} is outdated")
                
                # if it's, delete it.
                x.delete()



                #--------------------

    # Get all events set to repeat forever
    All_Forever_Event = models.Event.objects.filter(repeatd = "frv").exclude(repeat="nvr")
    
    # if there are events of that kind
    if len(All_Forever_Event) != 0 :

        # Run through each of them
        for y in range(len(All_Forever_Event)):
            x = All_Forever_Event[y]
            print (f"event = {x}")

            # And check if they have repetitions
            All_Forever_Repetition = x.Repetitions.all()
            print(f"All repetitions from event x = {All_Forever_Repetition}")
            
            # If they do, run through each one of them
            if len(All_Forever_Repetition) != 0 :
                print("from repetition")
                for z in range(len(All_Forever_Repetition)):

                    # Saving that repetition and it's date
                    repetition = All_Forever_Repetition[z]
                    repetition_date = datetime(repetition.day.year, repetition.day.month, repetition.day.day)
                    
                    # Get Today's date and the date of 3 years in the future
                    today = datetime.now()
                    Three_Years_From_Today = datetime(today.year + 3, today.month, today.day)
                    print(f'last_repetition = {Last_repetition}')
                    print(f'today = {today}')
                    print(f'two years from today = {Two_Years_From_Today}')
                    print ( f" ({Last_repetition} - {today}) <= ({Two_Years_From_Today} - {today})")
                    print (f'event = {x}, repetition = {repetition}')
                    print (f"repeatedevent {Last_repetition - today} >= {Three_Years_From_Today - today}")
                    
                    # Check if this repetitions is 3 years older or more.
                    if (today - repetition_date) >= (Three_Years_From_Today - today):
                        
                        # If it's, delete it.
                        repetition.delete()

            # If this event doesn't have repetitions, then something is wrong.
            # as all events set to repeat forever create repetitions by default.
            else:
                print (f"Something is wrong. the event {x} doesn't have repetition, despite being a forever event and going through an auto fill function.")
                break
                #print("from event.day")
                #Last_repetition = datetime(x.day.year, x.day.month, x.day.day) 
                #print(Last_repetition)
    
    pass

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

# checking for events set to forever.
fore = models.Event.objects.filter(repeatd = "frv")
#-----------------------------------



def index(request):
    x = datetime.now()
    print(x)
    error = ""
    alltodo = models.ListToDo.objects.all()
    today = models.WhatToDoToday.objects.filter(day=x).order_by('start_time')
    print(today)
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
    print(start)
    print(end)
    

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

def new_event(request):
    error=""
    event = forms.eventForm(request.POST or None)
    if request.method == "POST":
        if event.is_valid():
            event.save()
            event = forms.eventForm

        # if event wasn't valid
        else:
            print("something went wrong")
            error = "something went wrong"

    # returns the html with the empty form is through GET or a correct POST
    # returns with the filled post if event wasn't valid to make it easier to fix.
    return render(request, "New_event.html",{"event":event,"start":start,"end":end,"error":error,"weekday":weekday,"repeat_choices":repeat_choices,"priority_choices":priority_choices,})

    #if request.method == "GET":
     #   context={}
     #   form = forms.eventForm
      #  context['form']=form

def dailytask(request):

    error = ""
    task = forms.DailyTaskForm(request.POST or None)
    if request.method == "POST":
        title = request.POST['title']
        weekday = request.POST['weekday']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        quick_description = request.POST['quick_description']
        description = request.POST['description']
        notes = request.POST['notes']
        urgency = request.POST['urgency']
        importance = request.POST['importance']
        color=request.POST['color']

        print(f"title = {title}, weekday = {weekday}, Start = {start_time}, end = {end_time}, quick ={quick_description}, description = {description}, notes = {notes}, urgency = {urgency}, importance = {importance}")

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
                        error = f' There is an overlap with another task: {test.title}, {test.start_time} - {test.end_time}) on the weekday {day}'
                        break
            if error=="":
                # models.DailyTask.objects.create(
                    # saving the new task
                new = models.DailyTask(title=title,start_time=start_time,
                    end_time=end_time,quick_description=quick_description,
                    description=description,notes=notes,urgency=urgency,
                    importance=importance,color=color)
                new.save()
                # adding the weekdays, since it raises a error if added without first saving
                new.weekday.add(weekday)
                
    return render(request,"dailytask.html",{"task":task,"start":start,"end":end,"error":error,"repeat_choices":repeat_choices,"priority_choices":priority_choices,})

def listtodo(request):
    error = ""
    todo = forms.ListToDoForm(request.POST or None)
    alltodo = models.ListToDo.objects.all()
    if request.method == "POST":
        title = request.POST['title']
        quick_description = request.POST['quick_description']
        description = request.POST['description']
        # steps = request.POST['Steps'] Steps = {steps},
        notes = request.POST['notes']
        duration = request.POST['duration']
        urgency = request.POST['urgency']
        importance = request.POST['importance']
        progress = request.POST['progress']
        color = request.POST['color']
        print(f"color = {color}")
        print(f"todo['color'].value={todo['color'][0]}")
        #todo['color'][0]=str(todo['color'][0])
        #print(f"title = {title}, progress = {progress},  duration = {duration}, quick ={quick_description}, description = {description}, notes = {notes}, urgency = {urgency}, importance = {importance},color={color}")
        #print("todo")
        #print(todo)
        new = models.ListToDo(title=title,quick_description=quick_description,
                    description=description,notes=notes,
                    duration=duration, urgency=urgency,
                    progress=progress, color=color,
                    importance=importance)
        new.save()
        print(f"new = {new}")
        #listtd = models.ListToDo.objects.filter(title=title)
        #print(listtd.count())
        #if not listtd.exists():
            #print("listtd = 0")
            #if todo.is_valid():
            #print("valid")
            #todo.save()
            #todo = forms.ListToDoForm(None) 
            #else:
                #print("invalid")

    return render(request,"listtodo.html",{"alltodo":alltodo,"todo":todo,"error":error,"repeat_choices":repeat_choices,"priority_choices":priority_choices,})

def planner(request):
    x = datetime.now()
    data={}
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
    today = models.WhatToDoToday.objects.filter(day=x).order_by('start_time')
    todaylist= []
    N=0
    for n in today:
        data[f"today{N}"]= n.serialize()
        todaylist.append(f"today{N}")
        N=N+1
    data['todaylist']= todaylist

    daily = models.DailyTask.objects.filter(weekday=(x+timedelta(days=2)).strftime("%w")).order_by('start_time')
    dailylist= []
    N=0
    for n in daily:
        data[f"daily{N}"]= n.serialize()
        dailylist.append(f"daily{N}")
        N=N+1
    data['dailylist']= dailylist

    event = models.Event.objects.filter(day=x).order_by('start_time')
    eventlist= []
    N=0
    for n in event:
        data[f"event{N}"]= n.serialize()
        eventlist.append(f"event{N}")
        N=N+1
    data['eventlist']= eventlist

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
    test = models.DailyTask.objects.get(id=4)
    test1=test.weekday.all()[:1].get()
    #something=test1[0]
    #test2=something
    test2=test1.day
    test4=[]
    test3=test.weekday.all().get()
    #topping.name for topping in self.toppings.all()
    #test4 = test3.day
    #for x in range(len(test4)):
    #  test4.append(test.weekday.all()[:1].get())
    test4 = test3.id
    # getting a queryset with all Dailytask whose's weekday is among test's weekday.
    tasks = models.DailyTask.objects.filter(weekday__in=[test.weekday.all().get().id])
    # getting the lenght of that queryset
    test5 = len(tasks)
    # getting one object from that query set, allowing me to once again use thm as objects.
    test5 = tasks[3].weekday.all()
    x = datetime.now().date()

    # checking for events set to forever.
    fore = All_Non_Forever_Events = models.Event.objects.all().exclude(repeatd = "frv")| models.Event.objects.all().filter(repeatd = "frv").filter(repeat='nvr')
    # models.Event.objects.filter(repeatd = "frv").exclude(repeat="nvr")
    ftest=fore

    allf=0
    testtimetest =0
    testtimey=0
    #f=len(fore)-2
    #ftest=fore[f].Repetitions.all()
    #allf = fore
    #F=len(ftest) - 1
    #ftest=fore[f].Repetitions.all()[F].day
    #testtimetest = ftest - x
    #y = datetime(x.year + 2, x.month, x.day).date()
    #testtimey = y - x
    #if (ftest - x) >=(y-x):
    #    ftest = f"it's working!"
    #else:
    #    ftest = f"it's not working..."

    
            
    #test2=models.DailyTask.objects.get(id=something)
    #daily = models.DailyTask.objects.filter(id=5).get()
    #week = models.WeekDay.objects.filter(Todaytask__in=daily)[:1].get()
    
    #test1 = daily
    #test2 = week
    
    #test2=[]
    #for x in test1:
    #    test2.append(models.WeekDay.objects.filter(id=x[0])) 
    #test1 = models.DailyTask.objects.filter(weekday__in=[test.weekday.all()])
    todo = forms.WhatToDoTodayForm(request.POST or None)
    return render(request, "test.html",{'todo':todo, 'test':test,'test1':test1,'test2':test2,
        'test3':test3,'test4':test4,'test5':test5, 'ftest':ftest,
        'testtimetest':testtimetest,'testtimey':testtimey,'allf':allf})

def event(request,id):
    error=request.POST or None
    # variable to decide to where the submit button will post.
    # if Id = 0, it will lead back to a empty form so another event can be crate
    # if id != 0, will lead back to the page of the edited event.
    if error != None:
        tipe='error'
    else:
        tipe = id

    if id == 0:
        event = forms.eventForm(request.POST or None)
        if request.method == "POST":
            if event.is_valid():
                event.save()
                event = forms.eventForm

            # if event wasn't valid
            else:
                print("something went wrong")
                error = "something went wrong"
        
        # returns the html with the empty form is through GET or a correct POST
        # returns with the filled post if event wasn't valid to make it easier to fix.
        return render(request, "event.html",{"event":event,"start":start,"end":end,"error":error,
                    "weekday":weekday,"repeat_choices":repeat_choices,"priority_choices":priority_choices,
                    "tipe":tipe,})
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

        return render(request,"event.html",{"start":start,"end":end,"start_time":start_time,
                    "end_time":end_time,"event":event,"date":date,"error":error,"thisweekday":thisweekday,
                     "dateu":dateu, "tipe":tipe, })

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
