from django.conf.urls import url 
from . import views 

urlpatterns =[
  url(r'^$', views.index),
  url(r'^users/register$', views.register),
  url(r'^users/login$', views.login),
  url(r'^users/success$', views.success),
  url(r'^users/logout$', views.logout),

  url(r'^users/jobs/new$', views.new_job),
  url(r'^users/create$', views.create_job),
  url(r'^users/jobs/(?P<job_id>\d+)$', views.display_job),
  url(r'^users/jobs/delete/(?P<job_id>\d+)$', views.delete),
  url(r'users/jobs/edit/(?P<job_id>\d+)$', views.edit),
  url(r'users/jobs/update/(?P<job_id>\d+)$', views.update),
]
