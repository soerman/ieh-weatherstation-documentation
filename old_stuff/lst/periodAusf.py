from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

#Definition der Funktion, die aufgerufen werden soll
def job_function():
    print("Hello World")
#Wahl des Schedulers; wenn der Scheduler das einzige ist, was im Prozess laeuft,
#wird der BlockingScheduler benutzt
sched = BlockingScheduler()

# job_function soll jede Sekunde aufgerufen werden
sched.add_job(job_function, 'interval', seconds=1)

#Scheduler starten
sched.start()