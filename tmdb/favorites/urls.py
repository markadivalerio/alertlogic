from django.conf.urls import url
from favorites import views

urlpatterns = [
    url(r'^favorites/$', views.list_favorites),
    url(r'^favorites/add/$', views.add_to_favorites)
]