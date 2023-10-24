from . import models
from datetime import datetime,timedelta

# ---------------------- Warning --------------------------
# When add/removing "rows" to the model's field, make sure to wipe this file clear before migrating
# and then using Ctr + Z to restore it, because theses auto function will cause errors on the creation
# of fields during migrations
# Also need to delete the auto functions on view before migrating and Ctr + Z after it to restore them

#-------------------- Models.Listtodo auto urgency update ---------------------
# Function made to update all Listtodo whose Auto urgency update was enabled.
# increasing their ungency as their deadline approaches

now = datetime.now().date()

def urgency_time_calculation(number,time):
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

def listtodo_urgency_auto_update(now):
    auto_update_objects = models.ListToDo.objects.filter(urgency_update=True)
    if len(auto_update_objects)!= 0:
        for object in auto_update_objects:

            print(f"object = {object}")
            print(f"object.urgency_update = {object.urgency_update}")
            save = False

            if object.urgency != "vh":

                veryclose = urgency_time_calculation(object.urgency_veryclose_number,object.urgency_veryclose_type)
            
                close = urgency_time_calculation(object.urgency_close_number,object.urgency_close_type)

                medium = urgency_time_calculation(object.urgency_medium_number,object.urgency_medium_type)
        
                far = urgency_time_calculation(object.urgency_far_number,object.urgency_far_type)
                    
                if far != 0 and far > object.deadline_date and object.deadline_date > medium:
                        object.urgency = "l"
                        save = True

                elif medium != 0 and medium > object.deadline_date and object.deadline_date > close:
                        object.urgency = "m"
                        save = True

                elif close != 0 and close > object.deadline_date and object.deadline_date > veryclose:
                        object.urgency = "h"
                        save = True

                elif veryclose != 0 and veryclose > object.deadline_date:
                        object.urgency = "vh"
                        save = True

                if save == True:
                    object.save()
                    print(f"saved the object: {object}")

#--------------------- Models.event-forever auto update and models.eventrepetitions auto delte ------------------------------
# Function made to create repetitions to events sets to repeat forever, while deleting repetitions that are from 3 years ago
# Function created to create repetitions for events set to repeat forever to up to 2 years from now. 
# while also deleting every kind of repetition from 3 years ago



    #------------------------ testing the auto functions
def event_forever_repeat_creation(now):
    All_Forever_Event = models.Event.objects.filter(repeatd = "frv").exclude(repeat="nvr")

    print("all good till here 3")



    print("all good till here 4")

    if len(All_Forever_Event) != 0 :

        print("all good till here 4")

        for y in range(len(All_Forever_Event)):

            print("all good till here 5")

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
    print("all good till here")

#------------
def event_NonForever_auto_delete(years):
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
                # and get it's date
                z = All_Non_Forever_Events_Repetition[len(All_Non_Forever_Events_Repetition)-1].day
                Last_repetition = datetime(z.year, z.month, z.day)
            
            # if they don't, get the event's date.
            else:
                print("from event.day")
                Last_repetition = datetime(x.day.year, x.day.month, x.day.day) 
                #print(Last_repetition)
            
            # Get today's date and the date of N years in the future (determined on the function's execution)
            today = datetime.now()
            N_Years_From_Today = datetime(today.year + years, today.month, today.day)
   
            
            # check if the latest repetitions or the event is older than N years.
            if (today - Last_repetition ) >= (N_Years_From_Today - today):
                print(f"this event {x} is outdated")
                
                # if it's, delete it.
                x.delete()

# an exception created to help stop the below's function of one of the events set to forever doesn't have repetition
class EmptyResultSet(Exception):
    """A database query predicate is impossible."""
    pass

                #--------------------
def event_ForeverRepetitions_auto_delete(years):
    # Get all events set to repeat forever
    All_Forever_Event = models.Event.objects.filter(repeatd = "frv").exclude(repeat="nvr")
    
    # if there are events of that kind
    if len(All_Forever_Event) != 0 :

        # Run through each of them
        for y in range(len(All_Forever_Event)):
            x = All_Forever_Event[y]
            print (f"event = {x}")

            # And check if they have repetitions(Ps: Since they are set to repeat forever, they must have repeititons)
            All_Forever_Repetition = x.Repetitions.all()
            print(f"All repetitions from event x = {All_Forever_Repetition}")
            
            # If they do, run through each one of them
            if len(All_Forever_Repetition) != 0 :
                print("from repetition")
                for z in range(len(All_Forever_Repetition)):

                    # Saving that repetition and it's date
                    repetition = All_Forever_Repetition[z]
                    repetition_date = datetime(repetition.day.year, repetition.day.month, repetition.day.day)
                    
                    # Get Today's date and the date of N years in the future (N decided at the function's execution)
                    today = datetime.now()
                    N_Years_From_Today = datetime(today.year + years, today.month, today.day)

                    
                    # Check if this repetitions is N years older or more.
                    if (today - repetition_date) >= (N_Years_From_Today - today):
                        
                        # If it's, delete it.
                        repetition.delete()

            # If this event doesn't have repetitions, then something is wrong.
            # as all events set to repeat forever create repetitions by default.
            else:
                raise EmptyResultSet(f"Something is wrong. the event {x} doesn't have repetition, despite being a forever event and going through an auto fill function.")
                #print("from event.day")
                #Last_repetition = datetime(x.day.year, x.day.month, x.day.day) 
                #print(Last_repetition)
    
    pass
