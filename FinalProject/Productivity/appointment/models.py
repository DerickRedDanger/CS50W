from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime,timedelta,time
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from . import models_util

# for calendar and daily/weekly activities
    # Events and appoitments for the callendar


#test
print(time(5, 00))

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
        blank=False,
        default=today_weekday
        )
    
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
        #print(self.end_time)
        #print(type(self.end_time))
        #print(self.start_time)
        #print(type(self.start_time))
        #self.end_time = datetime.strptime(self.end_time, '%H:%M').time()
        #print(self.end_time)
        #print(type(self.end_time))
        #print(self.start_time)
        #print(type(self.start_time))
        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must be after starting times')
 
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
    
    def __str__(self):
        return f"{self.title}"
    
# Event's Post_save at models_util:
post_save.connect(models_util.event_post_save,sender=Event)
    
    

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

    def __str__(self):
        return f"{self.original.title} - R - {self.day}"
class DailyTask(models.Model):

    title = models.CharField(u"Event's name",max_length=200,)

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
        if self.end_time <= self.start_time:
            raise ValidationError('Ending times must after starting times')
            #zones__in=[<id1>]
        tasks = DailyTask.objects.filter(weekday__in=[self.weekday.all().get().id]).exclude(id=self.id)
        if tasks.exists():
            for task in tasks:
                if self.check_overlap(task.start_time, task.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        f'There is an overlap with another task: {task.title}, {task.start_time} - {task.end_time}) on {task.weekday.all()}')



    def __str__(self):
        return f"{self.title}"
class ListToDo(models.Model):
    title = models.CharField(u"Event's name",max_length=200,)
    quick_description = models.TextField(u"quick description",blank=True, null=True)
    description = models.TextField(u"detailed description",blank=True, null=True)
    steps = models.ManyToManyField(
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
    duration = models.CharField(u"How long do you expect this to take ?",
        max_length=2,
        choices= duration_choices,
        default=hours,
    )
    urgency = models.CharField(u"How urgent is this task ? can it wait/be delayed?",
        max_length=2,
        choices= urgency_choices,
        default=medium,
    ) # Very hight, hight, medium, low
    importance = models.CharField(u"How vital is this task ? will It bring great benefits if done? Great demerits if not done?",
        max_length=2,
        choices= priority_choices,
        default=medium,
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
        (fn, "forgottten and not started"),
        (har,"Hardship"),
    ]
    progress= models.CharField(u"What's the progress on this task? ",
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
        }

    def __str__(self):
        return f"{self.title}"

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


