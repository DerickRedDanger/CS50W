def event(request,id):
    error=""
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

    return render(request,"event.html",{"start":start,"end":end,"start_time":start_time,"end_time":end_time,"event":event,"date":date,"error":error,"thisweekday":thisweekday, "dateu":dateu})

 
