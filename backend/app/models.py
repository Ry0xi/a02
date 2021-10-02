from django.db import models

# Create your models here.

class User(models.Model):
    # user_id = models.AutoField(primary_key=True) #id
    user_name = models.CharField(max_length=30, null=False) #name
    email_address = models.EmailField(null=False) #mail adress
    token = models.CharField(max_length=100,null=False) #token
    task_count = models.IntegerField(default=0, null=False) #today's task count
    is_notification = models.BooleanField(default=True, null=False) #notification flag (on/off)
    task_limit = models.IntegerField(default=15, null=False) #task display limit


class Category(models.Model):
    # category_id = models.AutoField(primary_key=True) #id
    category_name = models.CharField(max_length=30, null=False) #name
    color_code = models.CharField(max_length=7, null=False) #color code (ex. #FF0060)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)


class Task(models.Model):
    # task_id = models.AutoField(primary_key=True) #id
    title = models.CharField(max_length=30, null=False) #task title
    detail = models.CharField(max_length=1000, null=True) #task detail
    url = models.CharField(max_length=300, null=True) #task URL
    created_at = models.DateTimeField(auto_now=True) #create datetime
    priority = models.IntegerField(default=10, null=False) #priority
    next_display_date = models.DateField(null=False) #next display date
    display_times = models.IntegerField(default=1, null=False) #Number of times displayed
    consecutive_times = models.IntegerField(default=0, null=False) #Number of consecutive achievements
    is_update = models.BooleanField(default=True, null=False) #update flag (on/off)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
    category_id = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True) #category id (fk)


class History(models.Model):
    # history_id = models.AutoField(primary_key=True) #id
    date = models.DateField(null=False) #completed date
    feedback = models.IntegerField(default=1, null=False) #feedback number
    number_of_tasks = models.IntegerField(default=0, null=False) #today's task count
    execution_tasks = models.IntegerField(default=0, null=False) #today's execution task count
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False) #user id (fk)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE, null=False) #task id (fk)
