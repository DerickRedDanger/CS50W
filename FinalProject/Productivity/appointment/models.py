from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime,timedelta
from django.core.exceptions import ValidationError
from django.urls import reverse

# for calendar and daily/weekly activities
    # Events and appoitments for the callendar
class Event(models.Model):

    x = datetime.now()
    Year=x.year
    Month=x.month
    Day=x.day
    start=f"{x.hour}:{x.minute}"
    y = x + timedelta(minutes=1)
    end=f"{y.hour}:{y.minute}"
    


    title = models.CharField(u"Event's name",max_length=200,)
    day = models.DateField(u'Day of the event',default=f"{Year}-{Month}-{Day}", help_text=u"Format: year-month-day")
    start_time = models.TimeField(u'Starting time',default=f"{start}", help_text=u"Format: hour:minute")
    end_time = models.TimeField(u'Ending time',default=f"{end}", help_text=u"Format: hour:minute")
    description = models.TextField(u"Event's description",blank=True, null=True)
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    repeat = models.IntegerField(u'number of repetitions',default=1,null=True, blank=True)

    #repeatnumber = models.IntegerField(default=1, null=True, blank=True)
    #repeatupto = models.DateTimeField(null=True, blank=True)
    # Event's Priority:
    veryhight="vh"
    high="h"
    medium="m"
    low="l"
    priority_choices = [
        (veryhight, 'very hight'),
        (high, 'hight'),
        (medium, 'medium'),
        (low, 'low'),
    ]
    
    priority = models.CharField(
        max_length=2,
        choices= priority_choices,
        default=medium,
    )
    
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
 
        events = Event.objects.filter(day=self.day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, self.start_time, self.end_time):
                    raise ValidationError(
                        'There is an overlap with another event: ' + str(event.day) + ', ' + str(
                            event.start_time) + '-' + str(event.end_time))


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
            # where there walls?
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