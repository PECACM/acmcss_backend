from django.conf.urls import url

from events.views import RegisterEvent

urlpatterns = [
    url(r'^(?P<event_id>[-\w]+)/team/', view=RegisterEvent.as_view(), name='register_event'),
]
