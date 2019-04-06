from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    template_name = 'posts.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(publish_date__lte=timezone.now()).order_by('-publish_date')

class DraftListView(LoginRequiredMixin, ListView):
    template_name = 'drafts.html'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    model = Post
    def get_queryset(self):
        return Post.objects.filter(publish_date__isnull=True).order_by('-create_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class UpdatePostView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class DeletePostView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    success_url = (reverse_lazy('posts'))

@login_required
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def see_approved_comments_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return post.approved_comments()

#Next section is dedicated to comments

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approval(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_removal(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    redirect('post_detail', pk=post_pk)
