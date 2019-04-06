from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.AboutView.as_view(), name='about'),
    path('',views.PostListView.as_view(), name='posts'),
    path('drafts/',views.DraftListView.as_view(), name='drafts'),
    path('post/(?P<pk>\d+)', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='new_post'),
    path('post/(?P<pk>\d+)/edit/', views.UpdatePostView.as_view(),name='update_post'),
    path('post/(?P<pk>\d+)/delete/', views.DeletePostView.as_view(),name='delete_post'),
    path('post/(?P<pk>\d+)/publish/', views.publish_post, name='publish_post'),
    path('post/(?P<pk>\d+)/comment/', views.add_comment_to_post,name='comment_on_post'),
    path('post/(?P<pk>\d+)/approved_comments/', views.see_approved_comments_post,name='approved_comment_of_post'),
    path('comment/(?P<pk>\d+)/approve/', views.comment_approval,name='approve_comment'),
    path('comment/(?P<pk>\d+)/remove/', views.comment_removal,name='remove_comment'),
]
