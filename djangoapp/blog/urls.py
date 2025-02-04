import blog.views as blog
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', blog.index, name='index'),
    path('post/<slug:slug>/', blog.post, name='post'),
    path('page/<slug:slug>/', blog.page, name='page'),
    path('created_by/<int:author_pk>/', blog.created_by, name='created_by'),
    path('category/<slug:slug>/', blog.category, name='category'),
    path('tag/<slug:slug>/', blog.tag, name='tag'),
    path('search/', blog.search, name='search'),
]
