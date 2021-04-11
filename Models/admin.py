from django.contrib import admin
from .models import PhotoModel, UserModel, SelectionModel
# Register your models here.
admin.site.register(PhotoModel)
admin.site.register(UserModel)
admin.site.register(SelectionModel)
