# coding: UTF-8
from crontab import CronTab

if __name__ == '__main__':
    tasks = ['b_list']
    cron = CronTab()
    i = 0
    for task in tasks:
        job = cron.new(command="python3 mf.py {}".format(task))
        job.setall("{} 13 * * *".format(i))
        i += 1
    cron.write("./crontab")
    for result in cron.run_scheduler():
        print(result)
