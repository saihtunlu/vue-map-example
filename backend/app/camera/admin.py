from django.contrib import admin
from .models import Camera, Images, Activity
# Register your models here.
models = [Camera, Images, Activity]
admin.site.register(models)
