from django.shortcuts import render
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib import messages
from groups.models import Group, GroupMember
from django.views import generic

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name','description')
    model = Group

class SingleGroup(generic.DetailView):
    model  = Group

class ListGroup(generic.ListView):
    model = Group
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['other_groups'] = Group.objects.exclude(members__in=[self.request.user])
            context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
        except: pass
        return context

class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try: GroupMember.objects.create(user=self.request.user, group=group)
        except: messages.warning(self.request, 'You Are Already In Group!')
        else: messages.success(self.request, 'You Are Now A Member!')
        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug'),
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'You Are Not In This Group!')
        else:
            membership.delete()
            messages.success(self.request, 'You Are No Longer A Member!')
        return super().get(request, *args, **kwargs)
