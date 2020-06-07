from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from accounts.views import ParticipantViewSet
from events.views import UserViewSet, EventViewSet, EventCategoryViewSet, EventTypeViewSet, ClubViewSet, \
    RegistrationViewSet, SponsorViewSet, BrochureViewSet
from acmcss import settings

# Routers provide an easy way of automatically determining the URL conf.
#
router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'event', EventViewSet, basename='event')
router.register(r'event_category', EventCategoryViewSet, basename='eventcategory')
router.register(r'event_type', EventTypeViewSet, basename='eventtype')
router.register(r'club', ClubViewSet, basename='club')
router.register(r'registration', RegistrationViewSet, basename='registration')
router.register(r'sponsor', SponsorViewSet, basename='sponsor')
router.register(r'brochure', BrochureViewSet, basename='brochure')
router.register(r'participant', ParticipantViewSet, basename='participant')

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/auth/', include('accounts.urls')),
                  url(r'^api/', include(router.urls)),
                  url(r'^events/', include('events.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
