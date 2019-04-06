from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin
from . import models, forms
from django.contrib import messages
from groups.models import Group
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

class PostList(SelectRelatedMixin, generic.ListView):
    model = models.Post
    template_name = 'posts/post_list.html'
    select_related = ('user','group')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['other_groups'] = Group.objects.exclude(members__in=[self.request.user])
            context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
        except: pass
        return context

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/post_list_user.html'
    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except UserDoesNotExist:                                                        #self.request.user.username???
            raise Http404
        else:
            return self.post_user.posts.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['concerned_username'] = self.post_user.username
        context['post_user'] = self.post_user
        try:
            context['other_groups'] = Group.objects.exclude(members__in=[self.request.user])
            context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
        except: pass
        return context

class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user','group')
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))
                                                    #self.request.user.username???

class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    #fields = ('title','message','group')
    form_class = forms.FilterPostForm
    model = models.Post
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    template_name = 'posts/post_confirm_delete.html'
    select_related = ('user','group')
    succes_url = reverse_lazy('posts:all')
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)
    def delete(self, *arg, **kwargs):
        messages.success(self.request, 'Post Deleted Successfully!')
        return super().delete(*arg, **kwargs)
