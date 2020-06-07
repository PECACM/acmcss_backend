import datetime
import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from simple_history.admin import SimpleHistoryAdmin

from events.models import Event, Club, Registration, PastSponsor, NewSponsor, EventType, EventCategory, Brochure, \
    DetailWinner, \
    TeamWinner, Winners, SponsorPartnership


class RegistrationResource(resources.ModelResource):
    eventID = Field(attribute='registered_event__id', column_name='Event ID')
    eventName = Field(attribute='registered_event__name', column_name='Event Name')
    teamName = Field(attribute='team__name', column_name='Name of the team')
    team = Field(column_name='Team members')
    username = Field(attribute='team_leader__username', column_name='Team Leader PECFest ID')
    firstName = Field(attribute='team_leader__first_name', column_name='First Name of Leader')
    lastName = Field(attribute='team_leader__last_name', column_name='Last Name of Leader')
    email = Field(attribute='team_leader__email', column_name="Email ID of Leader")
    contactNumber = Field(attribute='team_leader__participant__contactNumber', column_name='Contact Number of Leader')

    def dehydrate_team(self, registration):
        listOfMembers = []
        try:
            members = registration.team.members.all()
            for member in members:
                listOfMembers.append(
                    "[" + member.username + "," + str(member.participant.contactNumber) + "," + member.email + "," +
                    member.first_name + " " + member.last_name + "," + member.participant.college + "]"
                )
        except Exception as e:
            pass

        return ','.join(listOfMembers)

    class Meta:
        model = Registration
        fields = (
            'eventID',
            'eventName',
            'teamName',
            'team',
            'username',
            'firstName',
            'lastName',
            'email',
            'contactNumber',

        )


class RegistrationAdmin(ImportExportModelAdmin):
    resource_class = RegistrationResource
    list_filter = (
        'registered_event__association',
        'registered_event__eventType__eventCategory',
        'registered_event__eventType',
        'registered_event__name',
    )

    def changelist_view(self, request, extra_context=None):
        qs = self.get_queryset(request)
        query_attrs = dict([(param, val) for param, val in request.GET.items()])
        qs = qs.filter(**query_attrs)

        chart_data = (
            qs.annotate(date=TruncDay("record_created"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


class DetailWinnerAdmin(SimpleHistoryAdmin):
    search_fields = ['user__username']


class EventResource(resources.ModelResource):
    eventID = Field(attribute='id', column_name='Event Id')
    name = Field(attribute='name', column_name='Name')
    details = Field(attribute='details', column_name='Details of Event')
    shortDescription = Field(attribute='shortDescription', column_name='Short Description')
    ruleList = Field(attribute='ruleList', column_name='Rules List')
    locations = Field(attribute='locations', column_name='Location of the event')
    dateTime = Field(column_name='Date and Time')
    prize = Field(attribute='prize', column_name="Prizes")
    minTeam = Field(attribute='minTeam', column_name='Minimum members')
    maxTeam = Field(attribute='maxTeam', column_name='Maximum members')
    eventType = Field(attribute='eventType__name', column_name='Event Type')
    eventCategory = Field(attribute='eventType__eventCategory__name', column_name='Event Category')

    class Meta:
        model = Event
        fields = (
            'name',
            'details',
            'shortDescription',
            'ruleList',
            'locations',
            'dateTime',
            'prize',
            'minTeam',
            'maxTeam',
            'eventType',
            'eventCategory',
        )

    def dehydrate_dateTime(self, event):
        return datetime.datetime.strftime(event.dateTime, '%m/%d/%Y %I:%M:%S %p')


class EventAdmin(ImportExportModelAdmin, SimpleHistoryAdmin):
    resource_class = EventResource
    search_fields = (
        'name',
        'eventType__name',
        'eventType__eventCategory__name',
    )


admin.site.register(EventType)
admin.site.register(EventCategory)
admin.site.register(Event, EventAdmin)
admin.site.register(Club)
admin.site.register(PastSponsor)
admin.site.register(NewSponsor)
admin.site.register(SponsorPartnership)
admin.site.register(Brochure)
admin.site.register(Registration, RegistrationAdmin)
admin.site.register(TeamWinner, SimpleHistoryAdmin)
admin.site.register(DetailWinner, DetailWinnerAdmin)
admin.site.register(Winners, SimpleHistoryAdmin)
