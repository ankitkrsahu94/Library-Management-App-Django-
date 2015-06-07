from django.conf.urls import include, url
from django.contrib import admin
from app.views import Index

admin.autodiscover()

urlpatterns = [
    url(r'^app/',include('app.urls')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^$','app.views.index'),
    url(r'^$',Index.as_view()),
]
