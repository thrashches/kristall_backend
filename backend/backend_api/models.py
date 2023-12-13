from django.db import models

from django.db import models


class MyModel(models.Model):
    text = models.CharField(max_length=100)
