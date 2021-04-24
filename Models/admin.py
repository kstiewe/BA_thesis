from django.contrib import admin
from .models import PhotoModel, UserModel, SelectionModel, AlgorithmModel
# Register your models here.
admin.site.register(PhotoModel)
admin.site.register(UserModel)
admin.site.register(SelectionModel)
admin.site.register(AlgorithmModel)
