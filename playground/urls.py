from django.urls import path
from . import views
#urlconfig for playground app
urlpatterns = [
    path('hello/', views.say_hello),
]