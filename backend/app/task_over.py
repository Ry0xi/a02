from datetime import date, timedelta

from apscheduler.schedulers.background import BackgroundScheduler

from .models import Task, Profile, History

# 実行job関数
def job(update_time):
  # Userモデルからupdate_timeがtimeの時刻のuser_idを取得してusers配列に入れる．
  users = Profile.objects.filter(update_time=update_time)
  for user in users:

    #Profileモデルから対象のuser.idでdisplay_dateが昨日のタスクに対し更新処理を行う．
    tasks = Task.objects.filter(user_id=user.user_id, is_update=True)
    for task in tasks:
      if task.next_display_date < date.today():

        display_times = task.display_times

        # 優先度を設定
        if display_times == 0:
          task.priority = task.priority + 20
          task.next_display_date = task.next_display_date + timedelta(days=1)

        #対象のtaskに対して更新処理
        history = History.objects.filter(task_id=task.id).order_by("-completed_date")[:1]
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

    print("update completed! user_id:"+str(user.user_id)+str(update_time)+":00")

# # 本番
# def start():
#   """
#   Scheduling data update
#   """
#   scheduler = BackgroundScheduler()
#   for update_time in range(0,6):
#     scheduler.add_job(job, 'cron', [update_time],  hour=update_time) # schedule
#   scheduler.start()

#test
def start():
  """
  Scheduling data update
  Run update function once every 1 minutes
  """
  scheduler = BackgroundScheduler()
  for update_time in range(0,6):
    scheduler.add_job(job, 'interval', [update_time],  seconds=20) # schedule
  scheduler.start()
