import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from fernet_fields import EncryptedEmailField, EncryptedCharField



class MyUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_num = EncryptedCharField(max_length=15) 
    email = EncryptedEmailField()
    name = EncryptedCharField(max_length=50)
