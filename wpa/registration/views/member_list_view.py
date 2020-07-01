from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from registration.models import Member, Membership


class MemberListView(LoginRequiredMixin, generic.ListView):
    model = Member
    template_name = 'registration/member_list_view.html'
    context_object_name = 'member_list'

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(MemberListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['member_list'] = 'This is just some data'
    #     return context
