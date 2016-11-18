from django.conf.urls import url
from . import views
  # ^ So we can call functions from our routes!
urlpatterns = [
  url(r'^$', views.index),
  url(r'^add$', views.add_user),
  url(r'^verify$', views.verify_user),
  url(r'^home$', views.homepage),
  url(r'^additem$', views.add_item),
  url(r'^delete/(?P<string>\w+)$', views.delete_item),
  url(r'^add_item_now$', views.add_item_now),
]
