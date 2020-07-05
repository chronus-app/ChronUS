from django.contrib import admin
from core import models


admin.site.register(models.User)
admin.site.register(models.Student)
admin.site.register(models.CollaborationRequest)
admin.site.register(models.Collaboration)
admin.site.register(models.Competence)
admin.site.register(models.Degree)