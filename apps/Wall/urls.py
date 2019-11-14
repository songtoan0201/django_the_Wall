from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.showWall),
    url(r'^post_message$', views.post_message),
    url(r'^post_comment/(?P<message_id>\d+)$', views.post_comment),
    url(r'^delete_message/(?P<message_id>\d+)$', views.delete_message),
    url(r'^delete_comment/(?P<comment_id>\d+)$', views.delete_comment),
]
