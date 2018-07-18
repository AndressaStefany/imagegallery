from django.contrib import admin

from .models import User
from .models import Images

admin.site.register(User)
admin.site.register(Images)