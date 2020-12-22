from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Roles

# Register your models here.
admin.site.register(User)
admin.site.register(Roles)
