from django.contrib import admin
from .models import Blog, Contact, Message, Random

# Register your models here.
admin.site.register(Blog)
admin.site.register(Message)
admin.site.register(Random)
admin.site.register(Contact)
