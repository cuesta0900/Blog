from typing import Any
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.models import Post, Page
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404
from django.views.generic import ListView, DetailView

PER_PAGE = 9

class PostListView(ListView):
    template_name = 'blog/pages/index.html'
    context_object_name = 'posts'
    paginate_by = PER_PAGE
    queryset = Post.objects.get_published()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'page_title': 'Home - '})
        return context

class PageDetailView(DetailView):
    template_name = 'blog/pages/page.html'
    model = Page
    slug_field = 'slug'
    context_object_name = 'page'
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True).first()
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page = self.get_object()
        ctx.update({'page_title': f'{page.title} - Page - '})
        return ctx

class PostDetailView(DetailView):
    template_name = 'blog/pages/post.html'
    model = Post
    context_object_name = 'post'
    #queryset = Post.objects.get_published()
    
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self._post = self.get_object()
        ctx.update({'page_title': f'{self._post.title} - Post - '})
        return ctx
            
# def post(request, slug):
#     post_obj = (
#             Post.objects.get_published()
#             .filter(slug=slug)
#             .first()
#     )
    
#     if post_obj is None:
#         raise Http404()
    
#     page_title = f'{post_obj.title} - Page - ' 
    
#     return render(
#         request,
#         'blog/pages/post.html',
#         {
#             'post': post_obj,
#             'page_title': page_title,
#         }
#     )
    
class CreatedByListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs) 
        self._temp_context: dict[str, Any] = {}
        
    def get(self, request, *args, **kwargs):
        author_pk=self.kwargs.get('author_pk')
        user = User.objects.filter(pk=author_pk).first()
        
        if user is None:
            raise Http404()
        
        self._temp_context.update({
            'author_pk': author_pk,
            'user': user
        })
        
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        author_pk = self._temp_context['author_pk']
        queryset = super().get_queryset().filter(created_by__pk = author_pk)
        return queryset
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        
        user = self._temp_context['user']
        
        user_full_name = user.username
        if user.first_name:
            user_full_name = f'{user.first_name} {user.last_name}'
        page_title = f'Posts {user_full_name} - '
        
        ctx.update({'page_title': page_title})
        return ctx

class CategoryListView(PostListView):
    allow_empty = False
    def get_queryset(self):
        return super().get_queryset().filter(category__slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].category.name} - Categoria - '
        ctx.update({'page_title': page_title})
        return ctx
        

class TagListView(PostListView):
    allow_empty = False
    def get_queryset(self):
        return super().get_queryset().filter(tags__slug=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self.object_list[0].tags.first().name} - Tag - '
        ctx.update({'page_title': page_title})
        return ctx
    
class SearchListView(PostListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._search_value: str = ''
        
    def setup(self, request, *args, **kwargs):
        self._search_value = request.GET.get('search', '').strip()
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self._search_value == '':
            return redirect('blog:index')
        return super().get(self, request, *args, **kwargs)
    
    def get_queryset(self):
        qry = super().get_queryset().filter(
            Q(title__icontains=self._search_value) |
            Q(excerpt__icontains=self._search_value) |
            Q(content__icontains=self._search_value)
        )[:PER_PAGE] 
        return qry
        
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        page_title = f'{self._search_value[:30]} - Search'
        ctx.update({'page_title': page_title, 
                    'search_value': self._search_value,})
        return ctx
    
# def search(request):
#     search_value=request.GET.get('search').strip()#nome do input
#     posts = (
#         Post.objects.get_published().
#         filter(
#             #Título contém search_value OU
#             #Excerto contém search_value OU
#             #Conteúdo contén search_value
#             Q(title__icontains=search_value) |
#             Q(excerpt__icontains=search_value) |
#             Q(content__icontains=search_value)
#         )[:PER_PAGE]
#     )
    
#     page_title = f'{search_value[:30]} - Search - ' 


#     return render(
#         request,
#         'blog/pages/index.html',
#         {
#             'page_obj': posts,
#             'search_value': search_value,
#             'page_title': page_title
#         }
#     )