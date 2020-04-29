from django.conf.urls import url 
from tutorials import views 
 
urlpatterns = [ 
    url(r'^blogs/$', views.blogs_view),
    url(r'^api/tutorials/$', views.tutorial_list),
    url(r'^api/tutorials/(?P<pk>[0-9]+)$', views.tutorial_detail),
    url(r'^api/tutorials/published$', views.tutorial_list_published)
]