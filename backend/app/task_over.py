from backend.app.models import Task
import schedule
import time
from datetime import date, timedelta

from .models import Task, User, History

# 実行job関数
def job(time):
  # Userモデルからupdate_timeがtimeの時刻のuser_idを取得してusers配列に入れる．
  users = User.objects.filter(update_time=time)
  for user in users:

    #Taskモデルから対象のuser.idでdisplay_dateが昨日のタスクに対し更新処理を行う．
    tasks = Task.objects.filter(user_id=1)#1->user.id
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


#1時間毎のjob実行を登録
for i in range(0, 5):
  schedule.every().day.at(str(i)+":01").do(job(i))

# jobの実行監視、指定時間になったらjob関数を実行
while True:
    schedule.run_pending()
    time.sleep(1)