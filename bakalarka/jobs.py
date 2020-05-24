"""This is the jobs module.

Sets jobs to APSCHEDULER and set refresh to 00:00:00
"""
import json,time,os
from bakalarka import sched


def setBlinds(vyska,uhol):
    """Dummy function to show interaction with blinds"""
    print("Nastaví výšku: "+vyska+", uhol: "+uhol)


def initializer():
    """Load and sets events for actual date"""
    this_directory = os.path.dirname(__file__)
    aDate = time.strftime('%Y-%m-%d')
    with open(os.path.join(this_directory, 'static/events.json'), 'r') as f:
        data = json.loads(f.read()) 
        if aDate in data:
            for event in data[aDate]:
                datetime = aDate+" "+event['time']+":00"
                vyska = event['vyska']
                uhol = event['uhol']
                sched.add_job(setBlinds, 'date', run_date=datetime,args=[vyska, uhol])
    
initializer() #set job list
sched.add_job(initializer,'cron',hour ='0') #set job list refresh to 00:00:00 

