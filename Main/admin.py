from django.contrib import admin
from .models import *

admin.site.register(user)
admin.site.register(Article)
admin.site.register(Commet)
admin.site.register(News)
admin.site.register(exLesson)
admin.site.register(Tag)