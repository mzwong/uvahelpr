from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(HelprUser)
admin.site.register(Message)
admin.site.register(Job)
admin.site.register(Authenticator)

