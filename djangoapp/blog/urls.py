import blog.views as blog
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', blog.PostListView.as_view(), name='index'),
    path('post/<slug:slug>/', blog.post, name='post'),
    path('page/<slug:slug>/', blog.page, name='page'),
    path('created_by/<int:author_pk>/', blog.CreatedByListView.as_view(), name='created_by'),
    path('category/<slug:slug>/', blog.CategoryListView.as_view(), name='category'),
    path('tag/<slug:slug>/', blog.TagListView.as_view(), name='tag'),
    path('search/', blog.SearchListView.as_view(), name='search'),
]
