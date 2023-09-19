def clean(self):
        data=self
        Day=data.day
        repeatd=data.repeatd
        repeatutil = data.repeatutil
        repeatnumber = data.repeatnumber
        repeat = data.repeat
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
        if self.end_time <= self.start_time:
            print("raise validation error in models")
            raise ValidationError ('2 Ending times must be after starting times')
 
        if (repeat == "dly" or repeat == "wek") and repeatd == "frv":
            raise ValidationError ("Don't use repeat forever with daily/weekly. In that case, use daily task instead")

        if repeat != "nvr" and repeatd == "spc" and (type(repeatnumber) is not str or repeatnumber <= 0):
            raise ValidationError ( "If set to repeat a specific amount of time, the number of repetitions must be higher than 0")

        if repeat != "nvr" and repeatd == "utl" and repeatutil <= Day:
            raise ValidationError ("If set to repeat util a date, the date must be after the day of the event")


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
 