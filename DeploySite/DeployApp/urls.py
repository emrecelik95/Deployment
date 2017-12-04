from django.conf.urls import url
from .import views


urlpatterns = [
	url(r'^$',views.index,name='index'),
	url(r'^index.html$',views.index,name='index'),
	url(r'^createApp.html$',views.createApp,name='createApp'),
	url(r'^listApp.html$',views.listApp,name='listApp'),
	url(r'^listDep.html$',views.listDeps,name='listDeps'),
	url(r'^getApp.html$',views.getApp,name='listApp'),
	url(r'^listAppRev.html$',views.listAppRevisions,name='listAppRevision'),
	url(r'^listDepGroup.html$',views.listDepGroups,name='listDepGroups'),
	url(r'^createDep.html$',views.createDep,name='createDep'),
	url(r'^createDepGroup.html$',views.createDepGroup,name='createDepGroup'),
	url(r'^request$',views.request,name='request'),
]
