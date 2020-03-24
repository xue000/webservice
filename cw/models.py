from django.db import models

class Professor(models.Model):
    pid = models.CharField(primary_key=True, unique=True, max_length=32)
    pname = models.CharField(max_length=32)

class Module(models.Model):
    mcode = models.CharField(primary_key=True, unique=True, max_length=32)
    mname = models.CharField(max_length=32)

class List(models.Model):
    module = models.ForeignKey('Module', on_delete=models.CASCADE)
    year = models.IntegerField(default=2020)
    semester = models.IntegerField(default=1)
    professor = models.ManyToManyField('Professor')

class Rate(models.Model):
    rp = models.ForeignKey('Professor', on_delete=models.CASCADE)
    rm = models.ForeignKey('Module', on_delete=models.CASCADE)
    rate = models.IntegerField(default=5)
