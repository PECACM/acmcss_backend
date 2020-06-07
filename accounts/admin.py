from django.contrib import admin
from django.contrib.admin import ModelAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from accounts.models import Participant, Team

import json

from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay


class ParticipateResource(resources.ModelResource):

    username = Field(attribute='user__username', column_name='PECFest ID')
    firstName = Field(attribute='user__first_name', column_name='First Name')
    lastName = Field(attribute='user__last_name', column_name='Last Name')
    email = Field(attribute='user__email', column_name="Email ID")
    contactNumber = Field(attribute='contactNumber', column_name='Contact Number')
    accommodation = Field(attribute='accommodation', column_name='Accommodation Required Status')
    college = Field(attribute='college', column_name='College')
    address = Field(attribute='address', column_name='Residential Address')
    yearOfStudy = Field(attribute='yearOfStudy', column_name='Year of Study')

    class Meta:
        model = Participant
        fields = (
            'username',
            'firstName',
            'lastName',
            'email',
            'contactNumber',
            'accommodation',
            'college',
            'address',
            'yearOfStudy',
        )


class ParticipateAdmin(ImportExportModelAdmin, ModelAdmin):
    resource_class = ParticipateResource
    search_fields = ('user__first_name', 'user__last_name', 'user__username')
    change_list_template = 'admin/accounts/participant_list_change.html'

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = (
            Participant.objects.annotate(date=TruncDay("user__date_joined"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by("-date")
        )

        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}

        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)


admin.site.register(Participant, ParticipateAdmin)
admin.site.register(Team)
