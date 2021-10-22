import schedule
import time
from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from .models import Task, Setting, History

# 実行job関数
def job(update_time):
  # Userモデルからupdate_timeがtimeの時刻のuser_idを取得してusers配列に入れる．
  users = Setting.objects.filter(update_time=update_time)
  for user in users:

    #Settingモデルから対象のuser.idでdisplay_dateが昨日のタスクに対し更新処理を行う．
    tasks = Task.objects.filter(user_id=user.user_id)
    for task in tasks:
      if task.next_display_date < date.today():

        display_times = task.display_times

        # 優先度を設定
        if display_times == 0:
          task.priority = task.priority + 20

        #対象のtaskに対して更新処理
        history = History.objects.filter(task_id=task.id).order_by("-created_at")[:1]
        for history in history:
          feedback = history.feedback

          if feedback == 2:
            if display_times == 1:
              task.priority = task.priority + 9
            elif display_times == 2:
              task.priority = task.priority + 2
            elif display_times == 3:
              task.priority = task.priority + 1
          elif feedback == 1:
            if display_times == 1:
              task.priority = task.priority + 10
            elif display_times == 2:
              task.priority = task.priority + 3
            elif display_times == 3:
              task.priority = task.priority + 1
          elif feedback == 0:
            if display_times == 1:
              task.priority = task.priority + 11
            elif display_times == 2:
              task.priority = task.priority + 4
            elif display_times == 3:
              task.priority = task.priority + 2

          task.next_display_date = task.next_display_date + timedelta(days=1)
          task.save()

  print("update completed! "+str(update_time)+":00")


# def start():
#   """
#   Scheduling data update
#   Run update function once every 12 seconds
#   """
#   scheduler = BackgroundScheduler()
#   for update_time in range(0,6):
#     scheduler.add_job(job, 'cron', [update_time],  hour=update_time) # schedule
#   scheduler.start()

def start():
  """
  Scheduling data update
  Run update function once every 12 seconds
  """
  scheduler = BackgroundScheduler()
  for update_time in range(0,6):
    scheduler.add_job(job, 'interval', [update_time],  seconds=0.1) # schedule
  scheduler.start()

# def test(update_time):
#   print("update completed! ", update_time)

# def start():
#   """
#   Scheduling data update
#   Run update function once every 12 seconds
#   """
#   scheduler = BackgroundScheduler()
#   print("start")
#   for update_time in range(0,6):
#     scheduler.add_job(test, 'interval', [update_time],  seconds=0.05) # schedule
#   scheduler.start()