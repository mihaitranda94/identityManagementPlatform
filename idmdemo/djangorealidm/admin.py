from django.contrib import admin
from .models import *
from django.urls import reverse
from django.utils.safestring import mark_safe

from django.utils.translation import gettext_lazy as _

from river.models import State

# Register your models here.

admin.site.register(Group)
admin.site.register(User)
admin.site.register(Role)


class ApprovalRequiredListFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('approval required')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'approval'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('yes', _('for me')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == 'yes':
            return Grant.river.status.get_on_approval_objects(as_user=request.user)


def create_river_button(obj, transition_approval):
    approve_ticket_url = reverse('approve', kwargs={'grant_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
    return f"""
        <input
            type="button"
            style="margin:2px;2px;2px;2px;"
            value="{transition_approval.transition.source_state} -> {transition_approval.transition.destination_state}"
            onclick="location.href=\'{approve_ticket_url}\'"
        />
    """


@admin.action(description='Approve selected grants')
def approve_grants(modeladmin, request, queryset):
    for obj in queryset:
        obj.river.status.approve(as_user=request.user, next_state=State.objects.get(slug="approved"))


@admin.action(description='Disable selected grants')
def disable_grants(modeladmin, request, queryset):
    for obj in queryset:
        obj.river.status.approve(as_user=request.user, next_state=State.objects.get(slug="disabled"))


@admin.register(Grant)
class UserGrantAdmin(admin.ModelAdmin):
    list_display = ("id", "group", "role", "user", "status", "approval_actions")
    list_filter = (ApprovalRequiredListFilter,"group")
    search_fields = ['user__username', "group__name", "role__name"]
    actions = [approve_grants, disable_grants]

    def get_list_display(self, request):
        self.user = request.user
        return super(UserGrantAdmin, self).get_list_display(request)

    def approval_actions(self, obj):
        content = ""
        for transition_approval in obj.river.status.get_available_approvals(as_user=self.user):
            content += create_river_button(obj, transition_approval)

        return mark_safe(content)
