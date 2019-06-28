from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),                # /
    url(r'^create$', views.create),         # /create
    url(r'^login$', views.login),           # /login
    url(r'^dashboard$', views.dashboard),   # /dashboard
    url(r'^destroy$', views.destroy),       # /destroy
    url(r'^wishes/new$', views.newwish),     # /wishes/new
    url(r'^wishes/create$', views.create_wish),                  # /wishes/create
    url(r'^wishes/(?P<id>\d+)/edit$', views.edit_wish),          # /wishes/<id>/edit
    url(r'^wishes/update', views.update_wish),                   # /wishes/update
    url(r'^wishes/(?P<id>\d+)/destroy$', views.destroy_wish),    # /wishes/<id>/destroy
    url(r'^wishes/(?P<id>\d+)/granted$', views.wish_granted),    # /wishes/<id>/granted
    url(r'^wishes/(?P<id>\d+)/like$', views.wish_like),          # /wishes/<id>/like
    url(r'^wishes/stats$', views.stats),                          # /wishes/stats
]
