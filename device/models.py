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
    deviceType = models.CharField(max_length=20, choices=[
        ('router', '路由器'),
        ('controller', '控制器'),
        ('terminal', '终端'),
    ], default='router')

class portInfoModel(models.Model):
    id = models.IntegerField(primary_key=True)
    portName = models.CharField(max_length=10, default='default_port')  # 设置默认值
    ipAddress = models.CharField(max_length=15)
    mask = models.IntegerField(default=32)
    arriveSpeed = models.IntegerField(default=0)
    rx = models.IntegerField(default=0)
    tx = models.IntegerField(default=0)
    device = models.ForeignKey(deviceInfoModel, on_delete=models.CASCADE, null=True)