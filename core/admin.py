from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Copyright)
admin.site.register(models.Contestimg)
admin.site.register(models.Judgecat)
admin.site.register(models.Judge)
admin.site.register(models.Contest)
admin.site.register(models.Gallery) 