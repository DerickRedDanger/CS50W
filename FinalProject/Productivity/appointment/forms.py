from django import forms
from . import models
import datetime
from django.core.exceptions import ValidationError

HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]
now = datetime.datetime.now().date()
hours = {5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}
minutes = (00,15,30,45,)
start_choices=[]
end_choices=[]
for hour in hours:
    for minute in minutes:
        if hour == 5 and minute == 00:
            pass
        else:
            x = f"{hour}:{minute}"
            y = datetime.time(hour,minute)
            end_choices.append((y,x))
            
        if hour == 23 and minute == 45:
            pass
        else:
            j = f"{hour}:{minute}"
            k = datetime.time(hour,minute)
            start_choices.append((j,k))
class eventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['title','day','start_time','end_time','short_description','description','notes','importance','repeat','repeat_wkd','repeatd','repeatutil','repeatnumber','color',
                'monday','tuesday','wednesday','thursday','friday','saturday','sunday',]
        widgets = {
            'day' : forms.DateInput(attrs = {'placeholder': 'Year-Month-Day'}),
            #'start_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            #'end_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            'start_time': forms.Select(choices=start_choices),
            'end_time': forms.Select(choices=end_choices),
            'short_description':forms.Textarea(attrs={'cols': 90, 'rows': 3}),
            'description': forms.Textarea(attrs={'cols': 90, 'rows': 5}),
            'notes':forms.Textarea(attrs={'cols': 90, 'rows': 3}),
        }
#'day' : forms.DateInput(attrs = {'placeholder': 'Year-Month-Day'}),
#forms.CharField(widget=CalendarWidget)
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
        data=self.cleaned_data
        title=data.get("title")
        end_time=data.get("end_time")
        start_time=data.get("start_time")
        Day=data.get("day")
        repeatd=data.get("repeatd")
        repeatutil = data.get("repeatutil")
        repeatnumber = data.get("repeatnumber")
        repeat = data.get("repeat")
        monday=data.get("monday")
        tuesday=data.get("tuesday")
        wednesday=data.get("wednesday")
        thursday=data.get("thursday")
        friday=data.get("friday")
        saturday=data.get("saturday")
        sunday=data.get("sunday")
        print(f"start_time = {start_time}")
        print(f"end_time = {end_time}")
        #print(f"day = {Day}")
        #print(f"cleaned_data = {data}")
        print(type(end_time))
        print(type(start_time))

        #try:
        #    non_unique_name = models.Event.objects.filter(title=title).exclude(id=self.id)
        #    print(f"self.pk = {self.id}")
        #    print(f"non_unique_name with id = {non_unique_name}")
        #except:
        #    non_unique_name = models.Event.objects.filter(title=title)
        #    print(f"self.pk = {self.id}")
        #    print(f"non_unique_name with id = {non_unique_name}")
        #if non_unique_name:
        #    self.add_error ("title",'This title is already in use, pick another one')
        
        if end_time <= start_time:
            #raise forms.ValidationError("Ending time must be after starting time")
            print("raise validation error in forms")
            self.add_error("end_time", "Ending time must be after starting time")
            print("end before start")
            raise ValidationError("Form not saved, something went wrong.")
        
        if (repeat == "day" or repeat == "wek" or repeat == "wkd") and repeatd == "frv":
            self.add_error("repeatd", "Don't use repeat forever with daily/weekly/specific weekdays. In that case, use daily task instead")

        if repeat != "nvr" and repeatd == "spc" and (type(repeatnumber) is not int or repeatnumber <= 0):
            self.add_error("repeatnumber", "If set to repeat a specific amount of time, the number of repetitions must be higher than 0")

        if repeat != "nvr" and repeatd == "utl" and repeatutil <= Day:
            self.add_error("repeatutil", "If set to repeat util a date, the date must be after the day of the event")

        if repeat == "wkd" and sunday == False and monday == False and tuesday == False and wednesday == False and thursday == False and friday == False and saturday == False:
            self.add_error("sunday", "If set to on specific weekdays, at least one weekday needs to be selected")
        
        if repeat == "wkd" and sunday == True and monday == True and tuesday == True and wednesday == True and thursday == True and friday == True and saturday == True:
            self.add_error("sunday", "If set to on specific weekdays, don't select all weekdays, use daily task intead")
        
        try:
            events = models.Event.objects.filter(day=Day).exclude(id=self.id)
        except:
            events = models.Event.objects.filter(day=Day)

    
        
        #if events.exists():
        #    for event in events:
        #        if self.check_overlap(event.start_time, event.end_time, start_time, end_time):
        #            self.add_error("title", f"This event overlaps with the event: ''{event.title}'' that starts at {event.start_time} and ends at {event.end_time}")


class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = models.DailyTask
        fields = ['title','weekday','start_time','end_time','quick_description','description','notes','urgency','importance','color',
                  'monday','tuesday','wednesday','thursday','friday','saturday','sunday',]
        widgets = {
            
            'start_time': forms.Select(choices=start_choices),
            'end_time': forms.Select(choices=end_choices),
            'quick_description': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'description': forms.Textarea(attrs={'cols': 90, 'rows': 5}),
            'notes':forms.Textarea(attrs={'cols': 60, 'rows': 3}),
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

        data=self.cleaned_data
        end_time=data.get("end_time")
        start_time=data.get("start_time")
        title=data.get("title")
        id = data.get("id")
        monday=data.get("monday")
        tuesday=data.get("tuesday")
        wednesday=data.get("wednesday")
        thursday=data.get("thursday")
        friday=data.get("friday")
        saturday=data.get("saturday")
        sunday=data.get("sunday")
        #repeatd=data.get("repeatd")
        #repeatutil = data.get("repeatutil")
        #repeatnumber = data.get("repeatnumber")
        #monday=data.get("monday")
        #tuesday=data.get("tuesday")
        #wednesday=data.get("wednesday")
        #thursday=data.get("thursday")
        #friday=data.get("friday")
        #saturday=data.get("saturday")
        #sunday=data.get("sunday")

        #try:
        #    non_unique_name = models.DailyTask.objects.filter(title=title).exclude(id=self.id)
        #except:
        #    non_unique_name = models.DailyTask.objects.filter(title=title)
        #if non_unique_name:
        #    self.add_error ("title",'This title is already in use, pick another one')

        if end_time <= start_time:
            self.add_error('sunday','Ending times must after starting times')
            #zones__in=[<id1>]
        if sunday == False and monday == False and tuesday == False and wednesday == False and thursday == False and friday == False and saturday == False:
            self.add_error("sunday", "At least one weekday needs to be selected")

        tasks = models.DailyTask.objects.none()
        sun = models.DailyTask.objects.none()
        mon = models.DailyTask.objects.none()
        tue = models.DailyTask.objects.none()
        wed = models.DailyTask.objects.none()
        thu = models.DailyTask.objects.none()
        fri = models.DailyTask.objects.none()
        sat = models.DailyTask.objects.none()
        print(f"tasks at start = {tasks}")
        if sunday == True:
            sun = models.DailyTask.objects.filter(sunday = True)
            print(f"day on sunday = {sun}")

        if monday == True:
            mon = models.DailyTask.objects.filter(monday = True)
            print(f"day on monday = {mon}")

        if tuesday == True:
            tue = models.DailyTask.objects.filter(tuesday = True)
            print(f"day on tuesday = {tue}")

        if wednesday == True:
            wed = models.DailyTask.objects.filter(wednesday = True)
            print(f"day on wednesday = {wed}")

        if thursday == True:
            thu = models.DailyTask.objects.filter(thursday = True)
            print(f"day on thursday = {thu}")

        if friday == True:
            fri = models.DailyTask.objects.filter(friday = True)
            print(f"day on friday = {fri}")

        if saturday == True:
            sat = models.DailyTask.objects.filter(saturday = True)
            print(f"day on saturday = {sat}")
        tasks = (sun | mon | tue | wed | thu | fri | sat).distinct()
        tasks.exclude(id=id)
        print(f"tasks at end = {tasks}")

        if tasks.exists():
            for task in tasks:
                if self.check_overlap(task.start_time, task.end_time, start_time, end_time):
                    weekdays=[]
                    if sunday == True and task.sunday== True: # could be short handed to "if sunday and task.sunday:" As False fails in "if x:"
                        weekdays.append("Sunday")

                    if monday == True and task.monday==True:
                        weekdays.append("Monday")

                    if tuesday == True and task.tuesday==True:
                        weekdays.append("Tuesday")
                        
                    if wednesday == True and task.wednesday==True:
                        weekdays.append("Wednesday")

                    if thursday == True and task.thursday==True:
                        weekdays.append("Thursday")

                    if friday == True and task.friday==True:
                        weekdays.append("Friday")

                    if saturday == True and task.saturday==True:
                        weekdays.append("Saturday")
                    self.add_error("sunday", f"There is an overlap with another task: {task.title}, {task.start_time} - {task.end_time}) on {weekdays}")

class ListToDoForm(forms.ModelForm):
    class Meta:
        model = models.ListToDo
        fields = ['title','quick_description','description','step','step_to','duration','deadline',
                  'deadline_date','urgency','urgency_update',
                  'urgency_veryclose_number','urgency_veryclose_type',
                  'urgency_close_number','urgency_close_type',
                  'urgency_medium_number','urgency_medium_type',
                  'urgency_far_number','urgency_far_type',
                  'importance','progress','notes','color',]

        widgets={
            'deadline_date' : forms.DateInput(attrs = {'required': 'False'}),
            'quick_description': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'description': forms.Textarea(attrs={'cols': 90, 'rows': 5}),
            'notes':forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }

    def urgency_time_calculation(self,number,time):
        if time == "nn":
            return 0
        elif time == "dy":
            total_time = now + datetime.timedelta(days=number)
        elif time == "wk":
            total_time = now + datetime.timedelta(days=7*number)
        elif time == "mh":
            total_time = now + datetime.timedelta(days=30*number)
        elif time == "yr":
            total_time = now + datetime.timedelta(days=365*number)
        return total_time

    
    def clean(self):

        data = self.cleaned_data
        title=data.get("title")
        step = data.get("step")
        deadline=data.get("deadline")
        deadline_date=data.get("deadline_date")
        urgency=data.get("urgency")
        urgency_update=data.get("urgency_update")
        urgency_veryclose_number=data.get("urgency_veryclose_number")
        urgency_veryclose_type=data.get("urgency_veryclose_type")
        urgency_close_number=data.get("urgency_close_number")
        urgency_close_type=data.get("urgency_close_type")
        urgency_medium_number=data.get("urgency_medium_number")
        urgency_medium_type=data.get("urgency_medium_type")
        urgency_far_number=data.get("urgency_far_number")
        urgency_far_type=data.get("urgency_far_type")
        
        if deadline == True:
            if now > deadline_date:
                self.add_error ("deadline_date","The deadline can't be set to before today")

        if urgency_update == True:
            veryclose = self.urgency_time_calculation(urgency_veryclose_number,urgency_veryclose_type)
            close = self.urgency_time_calculation(urgency_close_number,urgency_close_type)
            medium = self.urgency_time_calculation(urgency_medium_number,urgency_medium_type)
            far = self.urgency_time_calculation(urgency_far_number,urgency_far_type)

            if far != 0 and urgency == "vl":
                lower=[]
                if medium != 0 and far < medium:
                    lower.append("medium")
                if close != 0 and far < close:
                    lower.append("close")
                if veryclose != 0 and far < veryclose:
                    lower.append("very close")
                if lower != []:
                    self.add_error("urgency_far_number",f"Far must be higher then {lower}")

            if medium != 0 and (urgency == "vl" or urgency == "l"):
                lower=[]
                if close != 0 and medium < close:
                    lower.append("close")
                if veryclose != 0 and medium < veryclose:
                    lower.append("very close")
                if lower != []:
                    self.add_error("urgency_medium_number",f"Medium must be higher then {lower}")

            if close != 0 and (urgency != "h" or urgency != "vh"):
                if veryclose != 0 and close < veryclose:
                    self.add_error("urgency_close_number",f"Close must be higher then 'Very close'")

        #try:
        #    non_unique_name = models.ListToDo.objects.filter(title=title).exclude(id=self.id)
        #except:
        #    non_unique_name = models.ListToDo.objects.filter(title=title)
        #if non_unique_name:
        #    self.add_error ("title",'This title is already in use, pick another one')

class WhatToDoTodayForm(forms.ModelForm):
    class Meta:
        model = models.WhatToDoToday
        fields = ['title','day','todo','need','start_time','end_time','done',]
