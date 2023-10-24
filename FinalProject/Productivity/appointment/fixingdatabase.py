from . import models

def fixing(all):

    obj = models.Event.objects.filter(importance = "vh")
    for i in obj:
        i.importance = "5"
        i.save()
    obj = models.Event.objects.filter(importance = "h")
    for i in obj:
        i.importance = "4"
        i.save()
    obj = models.Event.objects.filter(importance = "cr")
    for i in obj:
        i.importance = "3"
        i.save()
    obj = models.Event.objects.filter(importance = "m")
    for i in obj:
        i.importance = "2"
        i.save()
    obj = models.Event.objects.filter(importance = "l")
    for i in obj:
        i.importance = "1"
        i.save()
    obj = models.Event.objects.filter(importance = "vl")
    for i in obj:
        i.importance = "0"
        i.save()
    print("fixed event")


    obj = models.DailyTask.objects.filter(importance = "vh")
    for i in obj:
        i.importance = "5"
        i.save()
    obj = models.DailyTask.objects.filter(importance = "h")
    for i in obj:
        i.importance = "4"
        i.save()
    obj = models.DailyTask.objects.filter(importance = "cr")
    for i in obj:
        i.importance = "3"
        i.save()
    obj = models.DailyTask.objects.filter(importance = "m")
    for i in obj:
        i.importance = "2"
        i.save()
    obj = models.DailyTask.objects.filter(importance = "l")
    for i in obj:
        i.importance = "1"
        i.save()
    obj = models.DailyTask.objects.filter(importance = "vl")
    for i in obj:
        i.importance = "0"
        i.save()


    obj = models.DailyTask.objects.filter(urgency = "vh")
    for i in obj:
        i.urgency = "5"
        i.save()
    obj = models.DailyTask.objects.filter(urgency = "h")
    for i in obj:
        i.urgency = "4"
        i.save()
    obj = models.DailyTask.objects.filter(urgency = "m")
    print(f'obj ={obj}')
    for i in obj:
        i.urgency = "3"
        print(f'obj = {i}')
        i.save()
    obj = models.DailyTask.objects.filter(urgency = "l")
    for i in obj:
        i.urgency = "2"
        i.save()
    obj = models.DailyTask.objects.filter(urgency = "vl")
    for i in obj:
        i.urgency = "1"
        i.save()


    obj = models.ListToDo.objects.filter(importance = "vh")
    for i in obj:
        i.importance = "5"
        i.save()
    obj = models.ListToDo.objects.filter(importance = "h")
    for i in obj:
        i.importance = "4"
        i.save()
    obj = models.ListToDo.objects.filter(importance = "cr")
    for i in obj:
        i.importance = "3"
        i.save()
    obj = models.ListToDo.objects.filter(importance = "m")
    for i in obj:
        i.importance = "2"
        i.save()
    obj = models.ListToDo.objects.filter(importance = "l")
    for i in obj:
        i.importance = "1"
        i.save()
    obj = models.ListToDo.objects.filter(importance = "vl")
    for i in obj:
        i.importance = "0"
        i.save()

    
    obj = models.ListToDo.objects.filter(urgency = "vh")
    for i in obj:
        i.urgency = "5"
        i.save()
    obj = models.ListToDo.objects.filter(urgency = "h")
    for i in obj:
        i.urgency = "4"
        i.save()
    obj = models.ListToDo.objects.filter(urgency = "m")
    for i in obj:
        i.urgency = "3"
        i.save()
    obj = models.ListToDo.objects.filter(urgency = "l")
    for i in obj:
        i.urgency = "2"
        i.save()
    obj = models.ListToDo.objects.filter(urgency = "vl")
    for i in obj:
        i.urgency = "1"
        i.save()

    

    obj = models.WhatToDoToday.objects.filter(need = "Bw")
    for i in obj:
        i.need = "5"
        i.save()
    obj = models.WhatToDoToday.objects.filter(need = "Hv")
    for i in obj:
        i.need = "4"
        i.save()
    obj = models.WhatToDoToday.objects.filter(need = "Dn")
    for i in obj:
        i.need = "3"
        i.save()
    obj = models.WhatToDoToday.objects.filter(need = "Dl")
    for i in obj:
        i.need = "2"
        i.save()
    obj = models.WhatToDoToday.objects.filter(need = "it")
    for i in obj:
        i.need = "1"
        i.save()

    obj = models.ListToDo.objects.filter(duration = "mi")
    for i in obj:
        i.duration = "7"
        i.save()
    obj = models.ListToDo.objects.filter(duration = "hs")
    for i in obj:
        i.duration = "6"
        i.save()
    obj = models.ListToDo.objects.filter(duration = "ds")
    for i in obj:
        i.duration = "5"
        i.save()
    obj = models.ListToDo.objects.filter(duration = "wk")
    for i in obj:
        i.duration = "4"
        i.save()
    obj = models.ListToDo.objects.filter(duration = "mn")
    for i in obj:
        i.duration = "3"
        i.save()
    obj = models.ListToDo.objects.filter(duration = "ys")
    for i in obj:
        i.duration = "2"
        i.save()
    obj = models.ListToDo.objects.filter(duration = "Pe")
    for i in obj:
        i.duration = "1"
        i.save()

    obj = models.ListToDo.objects.filter(progress = "5")
    for i in obj:
        i.progress = "nt"
        i.save()
    obj = models.ListToDo.objects.filter(progress = "4")
    for i in obj:
        i.progress = "ip"
        i.save()
    obj = models.ListToDo.objects.filter(progress = "3")
    for i in obj:
        i.progress = "dn"
        i.save()
    obj = models.ListToDo.objects.filter(progress = "2")
    for i in obj:
        i.progress = "fo"
        i.save()
    obj = models.ListToDo.objects.filter(progress = "1")
    for i in obj:
        i.progress = "fn"
        i.save()
    obj = models.ListToDo.objects.filter(progress = "0")
    for i in obj:
        i.progress = "hd"
        i.save()
