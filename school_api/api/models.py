import uuid
from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    pass_hash = models.CharField(max_length=128)

    def __str__(self):
        return self.username
