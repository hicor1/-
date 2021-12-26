from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'APIreport' #Namespace에 등록해야 {% url %}에서 call할수있다

router = DefaultRouter()

router.register(r'ReportView', views.ReportViewset, basename='ReportView')


urlpatterns = [
    path('',include(router.urls)),
]