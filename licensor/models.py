from django.db import models
from . import validater
from datetime import datetime
# Create your models here.

class Access_key(models.Model):
    pass_code = models.TextField(unique=True)
    feret_key = models.TextField()
    licensed_to = models.CharField(max_length=500)
    activated = models.BooleanField(default=True)
    used_already = models.BooleanField(default=False)
    first_use_date = models.DateField(null=True)
    valid_for_days = models.IntegerField(default=0)
    valid_till = models.TextField()
    sequence = models.IntegerField()
    user_macid = models.CharField(max_length=200, null=True)
    app_name = models.CharField(max_length=200, default='ira')

    def __str__(self) -> str:
        return(self.licensed_to + "--license no--" + str(self.sequence))

    