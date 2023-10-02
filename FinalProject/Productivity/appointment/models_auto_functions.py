from . import models
from datetime import datetime,timedelta


#-------------------- Models auto urgency update ---------------------

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

def listtodo_urgency_auto_update(today):
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