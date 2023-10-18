from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime,timedelta,time
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from . import models_post_save
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import m2m_changed

# for calendar and daily/weekly activities
    # Events and appoitments for the callendar


#test
print(time(5, 00))

now = datetime.now().date()

# Time choices
hours = {5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}
minutes = (00,15,30,45,)
start_choices=[]
end_choices=[]
for hour in hours:
    for minute in minutes:
        if hour == 5 and minute == 00:
                pass
        # dt.time(00, 00)
        else:
            x = time(hour,minute)
            end_choices.append((x,x))
            
        if hour == 23 and minute == 45:
                pass
        else:
            y = time(hour,minute)
            start_choices.append((y,y))
        
start_choices=tuple(start_choices)
end_choices=tuple(end_choices)
print(f"start_choices = {start_choices}")
print(f"end_choices = {end_choices}")

# Choices for Urgency/Importance
veryhight="vh"
high="h"
medium="m"
low="l"
verylow="vl"
circumstantial="cr"
priority_choices = [
        (veryhight, 'Essential'),
        (high, 'important'),
        (medium, 'desirable'),
        (low, 'Curiosity/interest'),
        (verylow,'trivial'),
        (circumstantial,'circumstantial')
    ]





veryclose="vh"
close="h"
medium="m"
far="l"
veryfar = "vl"
urgency_choices = [
    (veryclose, 'Very Close'),
    (close, 'close'),
    (medium, 'Medium'),
    (far,"far"),
    (veryfar, "Very far"),

    ]





# setting up basic date data
x = datetime.now()
Year=x.year
Month=x.month
Day=x.day
start=f"{x.hour}:{x.minute}"
y = x + timedelta(minutes=1)
end=f"{y.hour}:{y.minute}"

class datetracking(models.Model):
    title = models.CharField(max_length=50, unique=True)
    day = models.DateField()

class WeekDay(models.Model):
    day = models.CharField(max_length=10)
    number = models.IntegerField()
    
    
    def __str__(self):
        return f"{self.day} - {self.id}"
    
class EventTool(models.Model):
    pass

class Event(models.Model):

    title = models.CharField(u"Event's name",max_length=200, unique=True)
    day = models.DateField(u'Day of the event', help_text=u"Format: year-month-day",)
    start_time = models.TimeField(u'Starting time',choices= start_choices)
    end_time = models.TimeField(u'Ending time', choices = end_choices)
    description = models.TextField(u"Event's description",blank=True, null=True)
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    
    importance = models.CharField(u"How vital is this event ? will It bring great benefits if done? Great demerits if not done?",
        max_length=2,
        choices= priority_choices,
        default=medium,
    )

    #----------------!!--------------------

    #repeat choices:
    nvr="nvr"
    dly="day"
    wek="wek"
    mth="mth"
    yea="yea"
    wkd="wkd"
    evd="edv"
    repeat_choices = [
        (nvr, 'never'),
        (dly, 'daily'),
        (wek, 'weekly'),
        (mth, 'monthly'),
        (yea, 'yearly'),
        (wkd, 'specific weekdays'),
    ]

    repeat= models.CharField(u'when to repeat ?',
        max_length=3,
        choices= repeat_choices,
        default=nvr,
    )
    # here to fix a error in the data base
    today_weekday = (int(x.strftime('%w')) + int(2))
    # today_weekday = str()

    repeat_wkd = models.ManyToManyField(
        WeekDay,
        related_name="Todayevent",
        blank=True,
        )
    
    monday=models.BooleanField(default=False)
    tuesday=models.BooleanField(default=False)
    wednesday=models.BooleanField(default=False)
    thursday=models.BooleanField(default=False)
    friday=models.BooleanField(default=False)
    saturday=models.BooleanField(default=False)
    sunday=models.BooleanField(default=False)
    #repeat duration choices:
    frv="frv"
    spc="spc"
    utl="utl"
    repeatd_choices = [
        (frv, 'Forever'),
        (spc, 'Specific number of times'),
        (utl, 'Util'),
    ]

    repeatd = models.CharField(u'How many times ?',
        max_length=3,
        choices= repeatd_choices,
        default=frv,
    )  
    repeatutil = models.DateField(u'Repeat util', help_text=u"Format: year-month-day",null=True, blank=True)
    repeatnumber = models.IntegerField(u'number of repetitions',default=1)
    color = models.CharField(u"Color in the planner/calendar",max_length= 9,blank=True,null=True)
 #--------------------!!------------------
    
    def serialize(self):
        
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "title": self.title,
            "color": self.color,
            "link":self.get_absolute_url(),
        }


    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
 
        return overlap
 
    #def get_absolute_url(self):
    #    url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
    #    return u'<a href="%s">%s</a>' % (url, str(self.start_time))
 
    # clean was here.   ------
    def clean(self):
        data=self
        Day=data.day
        repeatd=data.repeatd
        repeatutil = data.repeatutil
        repeatnumber = data.repeatnumber
        repeat = data.repeat
        monday=data.monday
        tuesday=data.tuesday
        wednesday=data.wednesday
        thursday=data.thursday
        friday=data.friday
        saturday=data.saturday
        sunday=data.sunday
        #print(self.end_time)
        #print(type(self.end_time))
        #print(self.start_time)
        #print(type(self.start_time))
        #self.end_time = datetime.strptime(self.end_time, '%H:%M').time()
        #print(self.end_time)
        #print(type(self.end_time))
        #print(self.start_time)
        #print(type(self.start_time))
        print (f"repeat = {repeat}")

        try:


            non_unique_name = Event.objects.filter(title=self.title).exclude(id=self.id)
            print(f"self.pk = {self.pk}")
            print(f"non_unique_name with id = {non_unique_name}")
        except:
            non_unique_name = Event.objects.filter(title=self.title)
        if non_unique_name:
            print(non_unique_name)
            raise ValidationError ('This title is already in use, pick another one')

        try:
            if self.end_time <= self.start_time:
                print("raise validation error in models")
                raise ValidationError ('From Models: Ending times must be after starting times')
        except TypeError:
                raise ValidationError('From Models: There is an error in start/end time')
        
        if (repeat == "day" or repeat == "wek" or repeatd == "wkd") and repeatd == "frv":
            raise ValidationError ("Don't use repeat forever with daily/weekly/specific weekdays. In that case, use daily task instead")

        if repeat != "nvr" and repeatd == "spc" and (type(repeatnumber) is not str or repeatnumber <= 0):
            raise ValidationError ( "If set to repeat a specific amount of time, the number of repetitions must be higher than 0")

        if repeat != "nvr" and repeatd == "utl" and repeatutil <= Day:
            raise ValidationError ("If set to repeat util a date, the date must be after the day of the event")

        if repeat == "wkd" and sunday == False and monday == False and tuesday == False and wednesday == False and thursday == False and friday == False and saturday == False:
            raise ValidationError("If set to on specific weekdays, at least one weekday needs to be selected")

        if repeat == "wkd" and sunday == True and monday == True and tuesday == True and wednesday == True and thursday == True and friday == True and saturday == True:
            raise ValidationError("If set to on specific weekdays, don't select all weekdays, use daily task intead")

        events = Event.objects.filter(day=self.day).exclude(id=self.id)
        if events.exists():
            for event in events:

                # event isn't updating because it isn't being validated.
                # below is the likely reason, make it so that it try to
                # check if self.id == event.id, if it's, ignore this event.
                try:
                    if self.id == event.id:
                        print("self.id == event.id")
                        continue
                finally:
                    if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                        raise ValidationError(
                            f'There is an overlap with another event: {event.title} on {event.day}, {event.start_time} - {event.end_time})')
        
        repeatedevents = EventRepetiton.objects.filter(day=self.day).exclude(original=self.id)
        if repeatedevents.exists():
            for repevent in repeatedevents:
                if self.check_overlap(repevent.original.start_time,repevent.original.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        f'There is an overlap with a repeating event: {repevent.original.title} on {repevent.original.day}, {repevent.original.start_time} - {repevent.original.end_time})')
 
    def get_absolute_url(self):
        return f"/event/{self.id}"

    def __str__(self):
        return f"{self.title}"
    
# Event's Post_save at models_post_save:
post_save.connect(models_post_save.event_post_save,sender=Event)
    
    

class EventRepetiton(models.Model):

    original=models.ForeignKey(
        Event, 
        on_delete=models.CASCADE,
        related_name="Repetitions"
    )

    day = models.DateField(u'Day of the event',default=f"{Year}-{Month}-{Day}", help_text=u"Format: year-month-day")
    start_time = models.TimeField(u'Starting time',default=f"{start}", help_text=u"Format: hour:minute")
    end_time = models.TimeField(u'Ending time',default=f"{end}", help_text=u"Format: hour:minute")
    
    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
 
        return overlap
 
    #def get_absolute_url(self):
    #    url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
    #    return u'<a href="%s">%s</a>' % (url, str(self.start_time))
 

    def serialize(self):
        
        return {
            "id": self.original.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "title": self.original.title,
            "color": self.original.color,
            "link":self.get_absolute_url(),
        }

    def clean(self):
        
        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.original.start_time, self.original.end_time):
                    raise ValidationError(
                        f'There is an overlap with another event: {event.title} on {event.day}, {event.start_time} - {event.end_time})')
        
        repeatedevents = EventRepetiton.objects.filter(day=self.day).exclude(id=self.id)
        if repeatedevents.exists():
            for repevent in repeatedevents:
                if self.check_overlap(repevent.original.start_time,repevent.original.end_time, self.original.start_time, self.original.end_time):
                    raise ValidationError(
                        f'There is an overlap with a repeating event: {repevent.original.title} on {repevent.day}, {repevent.start_time} - {repevent.end_time})')

    def get_absolute_url(self):
        return f"{self.original.get_absolute_url}"

    def __str__(self):
        return f"{self.original.title} - R - {self.day}"
class DailyTask(models.Model):

    title = models.CharField(u"Event's name",max_length=200,unique=True)

    #weekday choices:
    mon="1"
    tue="2"
    wed="3"
    thu="4"
    fri="5"
    sat="6"
    sun="0"
    weekday_choices = [
        (mon, 'monday'),
        (tue, 'tuesday'),
        (wed, 'wednesday'),
        (thu, 'thursday'),
        (fri, 'friday'),
        (sat, 'saturday'),
        (sun, 'sunday'),
    ]

    weekday = models.ManyToManyField(
        WeekDay,
        related_name="Todaytask",
        blank=True,
        )

    monday=models.BooleanField(default=False)
    tuesday=models.BooleanField(default=False)
    wednesday=models.BooleanField(default=False)
    thursday=models.BooleanField(default=False)
    friday=models.BooleanField(default=False)
    saturday=models.BooleanField(default=False)
    sunday=models.BooleanField(default=False)

    start_time = models.TimeField(u'Starting time',default=f"{start}", help_text=u"Format: hour:minute")
    end_time = models.TimeField(u'Ending time',default=f"{end}", help_text=u"Format: hour:minute")
    quick_description = models.TextField(u"quick description",blank=True, null=True)
    description = models.TextField(u"detailed description",blank=True, null=True)
    notes = models.TextField(u"task's Notes", help_text=u'Textual Notes', blank=True, null=True)
    
    urgency = models.CharField(u"How urgent is this task ? Can it wait/be delayed?",
        max_length=2,
        choices= urgency_choices,
        default=medium,
    )


    importance = models.CharField(u"How vital is this task ? Will It bring great benefits if done? Great demerits if not done?",
        max_length=2,
        choices= priority_choices,
        default=medium,
    )
    color = models.CharField(u"Color in the planner",max_length= 9,blank=True,null=True)

    #repeat choices:
    #nvr="nvr"
    #day="day"
    #wek="wek"
    #mth="mth"
    #yea="yea"
    #wkd="wkd"
    #evd="edv"
    #repeat_choices = [
    #    (nvr, 'never'),
    #    (wek, 'weekly'),
    #    (mth, 'monthly'),
    #    (yea, 'yearly'),
    #    (wkd, 'specific weekdays'),
    #]

    #repeat= models.CharField(u'Repeat ?',
    #    max_length=3,
    #    choices= repeat_choices,
    #    default=nvr,
    #)

    def serialize(self):
        
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "title": self.title,
            "color": self.color,
            "link":self.get_absolute_url(),
            
        }

    def check_overlap(self, fixed_start, fixed_end, new_start, new_end):
        overlap = False
        if new_start == fixed_end or new_end == fixed_start:    #edge case
            overlap = False
        elif (new_start >= fixed_start and new_start <= fixed_end) or (new_end >= fixed_start and new_end <= fixed_end): #innner limits
            overlap = True
        elif new_start <= fixed_start and new_end >= fixed_end: #outter limits
            overlap = True
 
        return overlap
 
    #def get_absolute_url(self):
    #    url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
    #    return u'<a href="%s">%s</a>' % (url, str(self.start_time))
 
    def clean(self):

        try:
            non_unique_name = DailyTask.objects.filter(title=self.title).exclude(id=self.id)
        except:
            non_unique_name = DailyTask.objects.filter(title=self.title)
        if non_unique_name:
            raise ValidationError ('This title is already in use, pick another one')

        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must after starting times')
            #zones__in=[<id1>]
        if self.sunday == False and self.monday == False and self.tuesday == False and self.wednesday == False and self.thursday == False and self.friday == False and self.saturday == False:
            raise ValidationError("At least one weekday needs to be selected")

        tasks = DailyTask.objects.none()
        sun = DailyTask.objects.none()
        mon = DailyTask.objects.none()
        tue = DailyTask.objects.none()
        wed = DailyTask.objects.none()
        thu = DailyTask.objects.none()
        fri = DailyTask.objects.none()
        sat = DailyTask.objects.none()
        print(f"tasks at start = {tasks}")
        if self.sunday == True:
            sun = DailyTask.objects.filter(sunday = True)
            print(f"day on sunday = {sun}")

        if self.monday == True:
            mon = DailyTask.objects.filter(monday = True)
            print(f"day on monday = {mon}")

        if self.tuesday == True:
            tue = DailyTask.objects.filter(tuesday = True)
            print(f"day on tuesday = {tue}")

        if self.wednesday == True:
            wed = DailyTask.objects.filter(wednesday = True)
            print(f"day on wednesday = {wed}")

        if self.thursday == True:
            thu = DailyTask.objects.filter(thursday = True)
            print(f"day on thursday = {thu}")

        if self.friday == True:
            fri = DailyTask.objects.filter(friday = True)
            print(f"day on friday = {fri}")

        if self.saturday == True:
            sat = DailyTask.objects.filter(saturday = True)
            print(f"day on saturday = {sat}")
        tasks = (sun | mon | tue | wed | thu | fri | sat).distinct()
        tasks.exclude(id=self.id)
        print(f"tasks at end = {tasks}")

        if tasks.exists():
            for task in tasks:
                if self.check_overlap(task.start_time, task.end_time, self.start_time, self.end_time):
                    weekdays=[]
                    if self.sunday == True and task.sunday== True: # could be short handed to "if sunday and task.sunday:" As False fails in "if x:"
                        weekdays.append("Sunday")

                    if self.monday == True and task.monday==True:
                        weekdays.append("Monday")

                    if self.tuesday == True and task.tuesday==True:
                        weekdays.append("Tuesday")
                        
                    if self.wednesday == True and task.wednesday==True:
                        weekdays.append("Wednesday")

                    if self.thursday == True and task.thursday==True:
                        weekdays.append("Thursday")

                    if self.friday == True and task.friday==True:
                        weekdays.append("Friday")

                    if self.saturday == True and task.saturday==True:
                        weekdays.append("Saturday")
                    raise ValidationError(f"There is an overlap with another task: {task.title}, {task.start_time} - {task.end_time}) on {weekdays}")

    def get_absolute_url(self):
        return f"/dailytask/{self.id}"

    def __str__(self):
        return f"{self.title}"

class ListToDo(models.Model):
    title = models.CharField(u"Event's name",max_length=200,unique=True)
    quick_description = models.TextField(u"quick description",blank=True, null=True)
    description = models.TextField(u"detailed description",blank=True, null=True)
    
    step = models.BooleanField(u"This task is one of the steps to another one?",default=False)

    step_to = models.ManyToManyField(
        "self", symmetrical=False,
        related_name="bigtask",
        blank=True,
        )
    
    #Duration choices
    minutes="mi"
    hours="hs"
    days="ds"
    weeks="wk"
    months="mn"
    years="ys"
    perpetual="Pe"
    duration_choices = [
        (minutes, "Minutes"),
        (hours, "Hours"),
        (days, "Days"),
        (weeks, "Weeks"),
        (months, "Months"),
        (years, "Years"),
        (perpetual, "Perpetual"),
    ]

    duration = models.CharField(u"How long do you expect this to take?",
        max_length=2,
        choices= duration_choices,
        default=hours,
    )


    deadline = models.BooleanField(u"This task has a deadline?",default=False)
    #repeatutil = models.DateField(u'Repeat util', help_text=u"Format: year-month-day",null=True, blank=True)
    deadline_date= models.DateField(u'When is the deadline?', help_text=u"Format: year-month-day", null=True, blank=True)

    importance = models.CharField(u"How vital is this task? Will It bring great benefits if done? Great demerits if not done?",
        max_length=2,
        choices= priority_choices,
        default=medium,
    )
    
    urgency = models.CharField(u"How urgent is this task? can it wait/be delayed?",
        max_length=2,
        choices= urgency_choices,
        default=medium,
    ) # Very hight, hight, medium, low

    urgency_update = models.BooleanField(u"Want this urgency to auto update as the deadline gets closer?",default=False)
    none="nn"
    day="dy"
    week="wk"
    month="mh"
    year="yr"
    type_choices = [
        (none,"---------"),
        (day, "Day(s)"),
        (week, "Week(s)"),
        (month, "Month(s)"),
        (year, "Year(s)"),
    ]

    urgency_veryclose_number= models.IntegerField(
        u'Update to "very close" when deadline is within:',
        default=1,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ])
    urgency_veryclose_type=models.CharField(
        max_length=2,
        choices=type_choices,
        default=day
    )
    
    urgency_close_number= models.IntegerField(
        u'Update to "close" when deadline is within:',
        default=1,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ])
    urgency_close_type=models.CharField(
        max_length=2,
        choices=type_choices,
        default=week
    )

    urgency_medium_number= models.IntegerField(
        u'Update to "medium" when deadline is within:',
        default=1,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ])
    urgency_medium_type=models.CharField(
        max_length=2,
        choices=type_choices,
        default=month
    )

    urgency_far_number= models.IntegerField(
        u'Update to "far" when deadline is within:',
        default=1,
        validators=[
            MaxValueValidator(30),
            MinValueValidator(1)
        ])
    urgency_far_type=models.CharField(
        max_length=2,
        choices=type_choices,
        default=year
    )

    #progress choices:
    nts="nt"
    inp="ip"
    done="dn"
    fo="fo"
    fn="fn"
    har="hd"
    progress_choices = [
        (nts, "Not Started"),
        (inp, "In Progress"),
        (done, "Done"),
        (fo, "forgotten"),
        (fn, "forgotten and not started"),
        (har,"Hardship"),
    ]
    progress= models.CharField(u"What's the progress on this task?",
        max_length=2,
        choices=progress_choices,
        default=nts
    )
    notes = models.TextField(u"task's Notes", help_text=u'Textual Notes', blank=True, null=True)
    color = models.CharField(u"Color in the planner",max_length= 9,blank=True,null=True)
    last_update = models.DateField(auto_now = True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "quick_description": self.quick_description,
            "duration": self.duration,
            "urgency": self.urgency,
            "importance": self.importance,
            "progress": self.progress,
            "notes": self.notes,
            "color": self.color,
            "link":self.get_absolute_url(),
        }
    
    def urgency_time_calculation(self,number,time):
        if time == "nn":
            return 0
        elif time == "dy":
            total_time = now + timedelta(days=number)
        elif time == "wk":
            total_time = now + timedelta(days=7*number)
        elif time == "mh":
            total_time = now + timedelta(days=30*number)
        elif time == "yr":
            total_time = now + timedelta(days=365*number)
        return total_time

    
    def clean(self):

        if self.deadline == True:
            try:
                if now > self.deadline_date:
                    raise ValidationError("The deadline can't be set to before today")
            except:
                raise ValidationError("The deadline can't be set to before today")

        if self.urgency_update == True:
            veryclose = self.urgency_time_calculation(self.urgency_veryclose_number,self.urgency_veryclose_type)
            print (f"veryclose = {veryclose}")
            close = self.urgency_time_calculation(self.urgency_close_number,self.urgency_close_type)
            print (f"close = {close}")
            medium = self.urgency_time_calculation(self.urgency_medium_number,self.urgency_medium_type)
            print (f"medium = {medium}")
            far = self.urgency_time_calculation(self.urgency_far_number,self.urgency_far_type)
            print (f"far = {far}")

            if far != 0 and self.urgency == "vl":
                lower=[]
                if medium != 0 and far < medium:
                    lower.append("medium")
                if close != 0 and far < close:
                    lower.append("close")
                if veryclose != 0 and far < veryclose:
                    lower.append("very close")
                if lower != []:
                    raise ValidationError(f"Far must be higher then {lower}")

            if medium != 0 and (self.urgency == "vl" or self.urgency == "l"):
                lower=[]
                if close != 0 and medium < close:
                    lower.append("close")
                if veryclose != 0 and medium < veryclose:
                    lower.append("very close")
                if lower != []:
                    raise ValidationError(f"Medium must be higher then {lower}")

            if close != 0 and (self.urgency != "h" or self.urgency != "vh"):
                if veryclose != 0 and close < veryclose:
                    raise ValidationError(f"Close must be higher then 'Very close'")

        try:
            print(f"self.pk = {self.pk}")
            non_unique_name = ListToDo.objects.filter(title=self.title).exclude(id=self.pk)
            print(f"non_unique_name with id = {non_unique_name}")
        except:
            non_unique_name = ListToDo.objects.filter(title=self.title)
        if non_unique_name:
            raise ValidationError('This title is already in use, pick another one')
        

    def save(self, *args, **kwargs):
        
        # if deadline is set to false, set deadline_date to null
        if self.deadline == False:
            self.deadline_date= None

        # If deadline set to true, urgency isn't set to Very Close and auto update is set to true
        if self.deadline == True and self.urgency != "vh" and self.urgency_update == True:
            
            # If urgency is set to far, zero the auto update of far
            if self.urgency == "l":
                self.urgency_far_value=1
                self.urgency_far_type="nn"
            
            # If urgency is set to medium, zero the auto update of far and medium
            if self.urgency == "m":
                self.urgency_medium_value=1
                self.urgency_medium_type="nn"
                self.urgency_far_value=1
                self.urgency_far_type="nn"
            
            # If urgency is set to close, zero the auto update of far, medium and close
            if self.urgency == "h":
                self.urgency_close_value=1
                self.urgency_close_type="nn"
                self.urgency_medium_value=1
                self.urgency_medium_type="nn"
                self.urgency_far_value=1
                self.urgency_far_type="nn"


        # else, if there isn't a deadline, auto update set to False or Urgency set to Very Close
        # set all auto updates to zero
        else:
            self.urgency_veryclose_value=1
            self.urgency_veryclose_type="nn"
            self.urgency_close_value=1
            self.urgency_close_type="nn"
            self.urgency_medium_value=1
            self.urgency_medium_type="nn"
            self.urgency_far_value=1
            self.urgency_far_type="nn"
            self.urgency_update=False
            
        super().save(*args, **kwargs)

        # Under th ListToDo model is a function that is connected to this one
        # when ManytoMany relationship is edited from this model a signal will be sent
        # to the function ListToDo_Steps_clear

    def get_absolute_url(self):
        return f"/listtodo/{self.id}"

    def __str__(self):

        return f"{self.title}"
    
# Function created to remove the Steps_to ManytoMany relationship on ListTodo Object if thir Step is set to false
def ListToDo_step_to_clearer(sender,instance, **kwargs):

    # after reaching this function, it disconects so that it's not signalled again while is edit the M2M
    # as, othewise, it would cause an endless recursion, activating itself over and over again.
    m2m_changed.disconnect(ListToDo_step_to_clearer, sender=ListToDo.step_to.through)

    # If step set to false
    if instance.step == False:
        # delete all M2M relationships on step_to
        instance.step_to.clear()
    # once done, reconnect.
    m2m_changed.connect(ListToDo_step_to_clearer, sender=ListToDo.step_to.through)

#  -- Command to connect ListTodo to it's Step_to_clearer --
m2m_changed.connect(ListToDo_step_to_clearer, sender=ListToDo.step_to.through)
    


class WhatToDoToday(models.Model):

    # need_to_do's choices:
    Hv="Hv" # I need to do today / Piority and rewarding things/ things that can't wait
    Dn="Dn" # I don't need to do today / Piority but not as rewarding and can wait compared to the others
    Bw="Bw" # I need to do and will bring great rewards/ The most complex and most rewarding
    Dl="Dl" # Needs to be done, but i don't need to do it myself
    it="it" # if enough  time, task that aren't priority, but don't take much effort or long time, 
    # thus can be done in low production moments, but NOT during times of rest
    need_choices = [
        (Hv, 'Have to do today'),
        (Dn, "Don't have to do today"),
        (Bw, 'Big Win'),
        (Dl, 'Can delegate'),
        (it, 'If enough time'),
    ]

    title = models.CharField(u"Name",max_length=50,)
    day = models.DateField(u"the day i (don't) have to do this",default=f"{Year}-{Month}-{Day}", help_text=u"Format: year-month-day")
    todo = models.ForeignKey(
        ListToDo,
        related_name="days_done",
        on_delete=models.CASCADE,
        null=True,
        )
    need = models.CharField(
        max_length=2,
        choices= need_choices,
        default=Hv,)
    color = models.CharField(u"Color in the planner",max_length= 9,blank=True,null=True)

    #--------------- create this's task's start and ending time
    #remembering it will be compared to the daily tasks and events time
    #so use time, not date
    start_time = models.TimeField(u'Starting time',default=f"{start}", help_text=u"Format: hour:minute")
    end_time = models.TimeField(u'Ending time',default=f"{end}", help_text=u"Format: hour:minute")
    #--------------
    done = models.BooleanField(default=False)
    
    def serialize(self):
        
        return {
            "id": self.id,
            "start_time": self.start_time,
            "end_time": self.end_time,       
            "title": self.title,
            "color": self.color,
        # "link":self.get_absolute_url(), ------ still have to create this model's page
        }

    def __str__(self):
        return f"{self.title} - {self.todo}"

class day(models.Model):
# divide in block of 30/10 mins each and paint the ones with tasks/appointments

    # appointment
    # description
    # start time
    # end time
    # days
    # color in day
    # priority
    pass
class daily(models.Model):
    # task
    # description
    # start time
    # end time
    # days
    # color in day
    # priority
    
    pass
class week(models.Model):
    #appointment
    # description
    # start time
    # end time
    # days
    # color in day
    # priority
    pass
class weekly(models.Model):
    # task
    # start time
    # end time
    # days
    # color in day
    # priority
    # description
    pass

# planning/priorities for today
class whatdotoday(models.Model):
    pass

# quotes
class quotes(models.Model):
    pass

# tips
class tip(models.Model):
    pass

# Methods
class method(models.Model):
    pass

# tools
class tools(models.Model):
    pass

# Useful links
class usefullinks(models.Model):
    pass

# For defining goals and objectives
class objective(models.Model):
    pass
class goals(models.Model):
    pass
class actions(models.Model):
    pass
class followup(models.Model):
    pass
class milestones(models.Model):
    pass
class reward(models.Model):
    # reward and celebrate your small achievments, it will help you keep on track
    # think about good side effects to your effort and your accomplishments
    # think about what you learned about yourself as you tried to acomplish your objectives
    # pick he right time
    # you don't need to do it alone
    # you deserve a reward
    # make theses celebrations a compromise with youself
    # do it without being afraid of being happy, it's the time to enjoy life and value what you've accomplished
    pass
# Review your objectives to achieve more
class review(models.Model):
    # Define a clear and specific objective
    # plan of action
    # execution
    # frequent measure of progress
    # review if your objective still makes sense for you today and if you achieving your milestones and goals
        # proress analysis
            # In a scale of 1-10 how confident are you on your progress toward your goal?
            # What had the most positive impact in your goals in this period?
            # are you on the right path?
            # were there walls?
            # is your rhythm good, slow or fast?
            # on what can you seek help?
        # failure analysis
            # did you accomplish the planned or it failed somewhere?
            # were there exernal factors out of your control?
                # which were they?
            # Which actions can be taken to bring the plan back on track
            # were there mistakes/errors?
            # on what can you seek help?
        # Subjective analysis
            # the accomplished objectives and goals contribute to your happiness on the long run?
            # do your objectives still make sense to you at this moment?
            # are they still what you want to accomplish? do you wanna aim higher? or change your target?
        # accept the result and think on how to improve
    # readjust as needed
    # execute and repeat
    # review your progress with a defined frequency and interval
    # Objective review is what allows you to go further
    # it's about what you become along the way that and what makes you aim higher
    pass

# predicting and preparing for problems 
class unexpectedevents(models.Model):
    pass
class countermeasures(models.Model):
    pass

# Motivation
class motivation(models.Model):
    # Why do you want to achieve this objetive?
    # what will it change for you or in your life?
    # what it will change for the ones you love or their lives?
    pass

# How much is your time worth it - calculator:
class calculator(models.Model):
    pass

# Time thieves and renters:
class thief(models.Model):
    pass
class renters(models.Model):
    pass
# List of time thieves/renters in your day:
class timelist(models.Model):
    #why is it a thief/renter
    #strategy to deal with them 
    pass

# Productivity block:
class Pblock(models.Model):
    # commitment
    # task
    # 5 more important tasks
    # less important but long tasks, save for another time or day (like next day)
    # less important but short tasks, do when there is time enough time
    # distribute the time for each task (what to do when)
    # how many breaks (drink water, strech, relax a bit) and when. Remember, you deserve breaks
    pass

# procrastination: 
    # types
class ptypes(models.Model):
    # types
    # habits
    # counters to each type
    pass
class distraction(models.Model):
    # think about the things that distract you from what matters
    # think of how to avoid/eliminate them 
    pass
# daily route - take a moment to stop and plan your day. knowing what to expect helps you stay on track.
class dailyroute(models.Model):
    # think about everything you want and have to do today
    # dismantle bigger tasks into smaller on es
    # name each task in a descriptive way
    # prioritise them
    # create a route through your tasks in the order and time you are going to do them
    # tick them as you complete them while focusing on a single one at time
    # start your day with the most important and most hard task as it's the time when you have more energy
    pass

# continuous growth 
class growth(models.Model):
    # grow a bit everyday
    # better 1% a day than 100% a year as the grow is exponential
    # do every single day something that will help you on your growth
    # exercises, classes, training, work out, practice
    # save a small amount of time everyday to dedicate for your own growth 
    pass

# creativity and problem solving
class inovationengine(models.Model):
    # imagination
    # ways of how to improve
    # what you will do to improve
    # creativity often comes from the need created from constrains
    # dedicate a set amount of time and effort to a task, and don't forget to focus on one at time

    # environment
    # ways of how to improve
    # what you will do to improve

    # attitude
    # ways of how to improve
    # what you will do to improve

    # knowledge
    # ways of how to improve
    # what you will do to improve

    # resources
    # ways of how to improve
    # what you will do to improve

    # culture
    # ways of how to improve
    # what you will do to improve
    pass

# pomodoro
class pomodoro(models.Model):
    # focus time (in min)
    # break time (in min)
    # total laps till large break
    # large break time(in min)
    # auto start/repeat
    pass

# mindfullness
class mindfulness(models.Model):
    pass


