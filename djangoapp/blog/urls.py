import blog.views as blog
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', blog.index, name='index'),
    path('post/<slug:slug>/', blog.post, name='post'),
    path('page/', blog.page, name='page'),
]
