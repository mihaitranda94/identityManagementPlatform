from django.urls import re_path, path
from django.views.generic import TemplateView


from . import views

urlpatterns = [
        re_path(r'^approve/(?P<grant_id>\d+)/(?P<next_state_id>\d+)/$', views.approve_ticket, name='approve'),
        path('', TemplateView.as_view(template_name="djangorealidm/main.html"), name="index"),
        path('basic-report', views.reports, name='basic-report'),
        path('history-report', views.grant_history, name='history-report')
    ]
