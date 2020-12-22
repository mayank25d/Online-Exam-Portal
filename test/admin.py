from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Quarter)
admin.site.register(Package)
admin.site.register(Subjects)
admin.site.register(DifficultyLevel)
admin.site.register(TestLanguage)
admin.site.register(Test)
admin.site.register(TestTopic)
admin.site.register(Question)
admin.site.register(Options)
