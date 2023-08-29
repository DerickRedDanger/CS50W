from . import models
from datetime import datetime,timedelta



def event_post_save(sender,instance,created, *args, **kwargs):
    if not created:
        repetitions = instance.Repetitions.all()
        if len(repetitions) !=0:
            for y in range(len(repetitions)):
                z = models.EventRepetiton(pk=repetitions[y].id)
                z.delete()
  

    if instance.repeat != "nvr":


                # save the start, end time and the day it started.
              #  start_time= request.POST['start_time']
              #  end_time=request.POST['end_time']
              #  day=request.POST['day']
                dayi=instance.day

                # Post return datetime as str, so i need to change them back to datetime
               # time=instance.day
               # year=int(f"{time[0]}{time[1]}{time[2]}{time[3]}")
               # month= int(f"{time[5]}{time[6]}")
               # dai= int(f"{time[8]}{time[9]}")
               # day=datetime(year,month,dai)

                # save the initial/starting day of repetition as the same day the event started
               #  dayi=day

                # save if the event is meant to be repeated forever,
                # specific number of times or util a certain data
               # repeatd= request.POST['repeatd']
            
      
                # If weekdays was selected, get the selected weekdays from the original event.
                if instance.repeat =="wkd":
                        
                        week=[]
                        if instance.sunday == True:
                            week.append(0)
                        if instance.monday == True:
                            week.append(0)
                        if instance.tuesday == True:
                            week.append(0)
                        if instance.wednesday == True:
                            week.append(0)
                        if instance.thursday == True:
                            week.append(0)
                        if instance.friday == True:
                            week.append(0)
                        if instance.saturday == True:
                            week.append(0)



                # if the event is set to repeat till a certain data or forever
                if instance.repeatd=="utl" or instance.repeatd =="frv":
                        print(f"repeatd = until or forever")

                        #if set utill a certain data
                        if instance.repeatd=="utl":
                            print(f"repeatd = {instance.repeatd}")

                            # save that certain data
                           # repeatutil= request.POST['repeatutil']

                            

                            # changing the repeatutil from str to datetime
                           # time=repeatutil
                           # year=int(f"{time[0]}{time[1]}{time[2]}{time[3]}")
                           # month= int(f"{time[5]}{time[6]}")
                           # dai= int(f"{time[8]}{time[9]}")
                           # dayf=datetime(year,month,dai)
                            dayf = instance.repeatutil

                        # if set to repeat forever
                        elif instance.repeatd == "frv":
                            print(f"repeatd = {instance.repeatd}")

                            # Since simply creating an repetition event endlessly wouldn't be doable
                            # and would take a lot of space, instead, it will be set to repeat for three years
                            # than increase by an year when it has 2 years remaining.
                            dayf=datetime(dayi.year+3, dayi.month, dayi.day)

                    

                        # while the day in question isn't higher than the until date:
                        while(dayi<= dayf):
                            print(f'dayi = {dayi}')
                            print(f'dayf = {dayf}')
                            
                            # since it's starting on the same day as the event, 
                            # i have to skip that initial day.
                            if dayi!=instance.day:

                                # if specific week days was selected
                                if instance.repeat=='wkd':
                                    print(f'dayi = {dayi.strftime("%w")}')

                                    # check if the weekday in question was one of the selected.
                                    if dayi.strftime("%w") in week:
                                        print(f"dayi = {dayi.strftime} in")

                                        # if it's create a new repetition and save.
                                        new = models.EventRepetiton(original=instance, day=dayi,
                                        start_time=instance.start_time, end_time=instance.end_time)
                                        print(f'new = {new}')
                                        new.save()
                                    else:
                                        print(f"dayi = {dayi.strftime} in")
                                # if it's not the initial day and it's not set to repeat on specific weekdays
                                # than this is a day that event is meant to be created.
                                else:
                                    new = models.EventRepetiton(original=instance, day=dayi,
                                    start_time=instance.start_time, end_time=instance.end_time)
                                    new.save()

                            # If set to repeat weekly, montly or yearly
                            # increase the day by 7 or month/year by 1
                            if instance.repeat =="wek":
                                dayi=dayi+timedelta(days=7)
                                print(f'wek - dayi = {dayi}')
                            elif instance.repeat =="mth":
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
                                        dayi=datetime(dayi.year, dayi.month+2, dayi.day)
                                        print(f'mth - dayi = {dayi}')

                            elif instance.repeat =="yea":
                                dayi=datetime(dayi.year+1, dayi.month, dayi.day)
                                print(f'yea - dayi = {dayi}')

                            # if it's none of the above, it was set to daily,
                            # so increase day by 1
                            else:
                                dayi=dayi+timedelta(days=1)
                                print(f'day - dayi = {dayi} yea')

                # else, if the event is set to be repeted a certain number of times
                elif instance.repeatd == "spc":
                        print('spc')
                        
                        # save that number of times
                        #repeatnumber = instance.request.POST['repeatnumber']

                        # initialize the repetitions at 1
                        n = 1

                        # while the the number of repetitions isn't higher than the number asked
                        while(n <= int(instance.repeatnumber)):
                            print(f'dayi = {dayi}')
                            print(f'n = {n}')

                            
                            # since it's starting on the same day as the event, i have to skip that day.
                            if dayi!= instance.day:

                                # if specific week days was selected
                                if instance.repeat=='wkd':
                                    print(f'dayi = {dayi.strftime("%w")} wkd')

                                    # check if the weekday in question was one of the selected.
                                    if dayi.strftime("%w") in week:
                                        
                                        # if it's create a new repetition and save.
                                        new = models.EventRepetiton(original= instance, day=dayi,
                                        start_time=instance.start_time, end_time=instance.end_time)
                                        print(f'new = {new}')
                                        new.save()
                                        n=n+1 
                                    else:
                                        print(f'dayi = {dayi.strftime("%w")} else wkd')
                                        print (f"week = {week}")
                                       
                                # if it's not the initial day and it's not set to repeat on specific weekdays
                                # than this is a day that event is meant to be created.
                                else:
                                    new = models.EventRepetiton(original=instance, day=dayi,
                                    start_time=instance.start_time, end_time=instance.end_time)
                                    print(f'new = {new}')
                                    new.save()
                                    n=n+1

                            # If set to repeat weekly, montly or yearly
                            # increase the day by 7 or month/year by 1
                            if instance.repeat =="wek":
                                dayi=dayi+timedelta(days=7)
                                print(f'wek - dayi = {dayi}')
                            elif instance.repeat =="mth":
    
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

                            #-------
                            elif instance.repeat =="yea":
                                try:
                                    dayi=datetime(dayi.year+1, dayi.month, dayi.day)
                                    print(f'yea - dayi = {dayi}')

                                    # if the day in question is 29th february:
                                except ValueError:
                                    if int (dayi.day) == 29 and int(dayi.month) == 2:
                                        dayi=datetime(dayi.year+4, dayi.month, dayi.day)
                                        print('yearly except ok')
                                    print('yearly except')
                                    print (f'dayi.day = {dayi.day} and dayi.month = {dayi.month}')
                            # if it's none of the above, it was set to daily,
                            # so increase day by 1
                            else:
                                dayi=dayi+timedelta(days=1)
                                print(f'day - dayi = {dayi} day')
                
 