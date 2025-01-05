import blog.views as blog
from django.urls import path

app_name = 'blog'

urlpatterns = [
    path('', blog.index, name='index'),
    path('post/', blog.post, name='post'),
    path('page/', blog.page, name='page'),
]
