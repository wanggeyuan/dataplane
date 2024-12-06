from django.db import models

class netInfoModel(models.Model):
    id = models.IntegerField(primary_key=True)
    ipAddress = models.CharField(max_length=15)
    mask = models.IntegerField(default=32)
    arriveSpeed = models.IntegerField(default=0)
    # link_speed = models.IntegerField(default=0)

class deviceInfoModel(models.Model):
    throughput = models.IntegerField(default=0)
    verifySpeed = models.IntegerField(default=0)
    avgDelay = models.FloatField(default=0.0)
    verifyMode = models.BooleanField(default=False)
    tableUsage = models.FloatField(default=0.0)

class portInfoModel(models.Model):
    id = models.IntegerField(primary_key=True)
    ipAddress = models.CharField(max_length=15)
    mask = models.IntegerField(default=32)
    arriveSpeed = models.IntegerField(default=0)
    rx = models.IntegerField(default=0)
    tx = models.IntegerField(default=0)