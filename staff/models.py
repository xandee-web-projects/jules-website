from django.db import models
from portal.models import Staff
from datetime import time

# Create your models here.
class Test(models.Model):
    name = models.CharField(max_length=40)
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    time = models.TimeField(default=time.fromisoformat("00:10"))
    done = models.IntegerField(default=0)
    code = models.CharField(max_length=5, null=True, blank=True)

class Question(models.Model):
    number = models.IntegerField()
    text = models.TextField()
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

class Option(models.Model):
    text = models.TextField()
    option_id = models.IntegerField()
    answer = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
