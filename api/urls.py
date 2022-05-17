from django.db import router
from django.urls import path,include
from django.contrib import admin
from api import views

urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/',views.student_api,name='student_api')
]
