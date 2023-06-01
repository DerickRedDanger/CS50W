from django import forms
from . import models

class eventForm(forms.ModelForm):
    class Meta:
        model = models.Event
        fields = ['title','day','start_time','end_time','description','notes','repeat','priority']
        widgets = {
            'day' : forms.DateInput(attrs = {'placeholder': 'Year-Month-Day'}),
            'start_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
            'end_time' : forms.TimeInput(attrs = {'placeholder': 'Hour:Minute'}),
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
        print(f"start_time = {start_time}")
        print(f"end_time = {end_time}")
        print(f"day = {Day}")
        print(f"cleaned_data = {data}")
        if end_time <= start_time:
            self.add_error("end_time", "Ending time must be after starting time")
 
        events = models.Event.objects.filter(day=Day)
        if events.exists():
            for event in events:
                if self.check_overlap(event.start_time, event.end_time, start_time, end_time):
                    self.add_error("title", f"This event overlaps with the event: {event.title} that starts at {event.start_time} and ends at {event.end_time}")
