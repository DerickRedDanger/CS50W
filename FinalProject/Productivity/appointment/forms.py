from django import forms
from . import models
import datetime as datetime
HOUR_CHOICES = [(datetime.time(hour=x), '{:02d}:00'.format(x)) for x in range(0, 24)]

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
        fields = ['title','day','start_time','end_time','description','notes','importance','repeat','repeat_wkd','repeatd','repeatutil','repeatnumber','color',
                'monday','tuesday','wednesday','thursday','friday','saturday','sunday',]
        widgets = {
            'day' : forms.DateInput(attrs = {'placeholder': 'Year-Month-Day'}),
            #'start_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            #'end_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            'start_time': forms.Select(choices=start_choices),
            'end_time': forms.Select(choices=end_choices),
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
        end_time=data.get("end_time")
        start_time=data.get("start_time")
        Day=data.get("day")
        repeatd=data.get("repeatd")
        repeatutil = data.get("repeatutil")
        repeatnumber = data.get("repeatnumber")
        repeat = data.get("repeat")
        #print(f"start_time = {start_time}")
        #print(f"end_time = {end_time}")
        #print(f"day = {Day}")
        #print(f"cleaned_data = {data}")
        #print(type(end_time))
        #print(type(start_time))
        if end_time <= start_time:
            #raise forms.ValidationError("Ending time must be after starting time")
            self.add_error("end_time", "Ending time must be after starting time")
        
        if (repeat == "dly" or repeat == "wek") and repeatd == "frv":
            self.add_error("repeatd", "Don't use repeat forever with daily/weekly. In that case, use daily task instead")

        if repeat != "nvr" and repeatd == "spc" and (type(repeatnumber) is not str or repeatnumber <= 0):
            self.add_error("repeatnumber", "If set to repeat a specific amount of time, the number of repetitions must be higher than 0")

        if repeat != "nvr" and repeatd == "utl" and repeatutil <= Day:
            self.add_error("repeatutil", "If set to repeat util a date, the date must be after the day of the event")

        try:
            events = models.Event.objects.filter(day=Day).exclude(id=self.id)
        except:
            events = models.Event.objects.filter(day=Day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, start_time, end_time):
                    self.add_error("title", f"This event overlaps with the event: ''{event.title}'' that starts at {event.start_time} and ends at {event.end_time}")


class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = models.DailyTask
        fields = ['title','weekday','start_time','end_time','quick_description','description','notes','urgency','importance','color',]
        widgets = {
            
            'start_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            'end_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            'quick_description': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'description': forms.Textarea(attrs={'cols': 90, 'rows': 5}),
            'notes':forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }
class ListToDoForm(forms.ModelForm):
    class Meta:
        model = models.ListToDo
        fields = ['title','quick_description','description','steps','duration','urgency','importance','progress','notes','color',]

        widgets={
            'quick_description': forms.Textarea(attrs={'cols': 60, 'rows': 3}),
            'description': forms.Textarea(attrs={'cols': 90, 'rows': 5}),
            'notes':forms.Textarea(attrs={'cols': 60, 'rows': 3}),
        }

class WhatToDoTodayForm(forms.ModelForm):
    class Meta:
        model = models.WhatToDoToday
        fields = ['title','day','todo','need','start_time','end_time','done',]
