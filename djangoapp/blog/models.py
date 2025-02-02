from django.db import models
from utils.rands import slugify_new
from django.contrib.auth.models import User
from utils.images import resize_image
from django_summernote.models import AbstractAttachment
from django.urls import reverse


# Create your models here.
class PostAttachment(AbstractAttachment): #model para redimensionar imagem no summernote
    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
            
        current_file_name = str(self.file.name) #Pega o nome do file atual
        super_save = super().save(args, kwargs) # armazena salvamento em variável

        file_changed = False
        if self.file: #Se tiver um file
            file_changed = current_file_name != self.file.name #True se o file foi mudado
        
        if file_changed: #se foi mudado faz o redimensionamento da imagem
            resize_image(self.file, 900, True, 70) #importado do images.py    
        
        return super_save #Salva
    

class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        unique=True, default=None, 
        null=True, blank=True, 
        max_length=255,
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=40)
    slug = models.SlugField(
        unique=True, default=None, 
        null=True, blank=True, 
        max_length=255,
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.name)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Page(models.Model):
    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default=" ", 
        null=False, blank=True, 
        max_length=255,
    )
    is_published = models.BooleanField(default=False,
    help_text='Se marcado, página será exibida')
    content = models.TextField()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

class PostManager(models.Manager):
    def get_published(self):
        return self.filter(is_published=True).order_by('-pk')

class Post(models.Model):
    class Meta:
            verbose_name = 'Post'
            verbose_name_plural = 'Posts'
            
    objects = PostManager()
    
    title = models.CharField(max_length=65,)
    slug = models.SlugField(
        unique=True, default=" ", 
        null=False, blank=True, 
        max_length=255,
    )
    excerpt = models.CharField(max_length=150,
        help_text='Um breve resumo do conteúdo do post')
    is_published = models.BooleanField(default=False,
    help_text='Se marcado, post será exibido')
    content = models.TextField()
    cover = models.ImageField(upload_to='posts/%Y/%m/', blank=True, default='')
    cover_in_post_content = models.BooleanField(default=True,
        help_text='Exibir imagem de capa também dentro do conteúdo do post?')
    created_at = models.DateTimeField(auto_now_add=True)#Cadastra no horário de criação
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_created_by'
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True, null=True,
        related_name='post_updated_by'
    )
    updated_at = models.DateTimeField(auto_now=True)#Altera data
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None
    )
    tags = models.ManyToManyField(Tag, blank=True, default='')
    
    def get_absolute_url(self):
        if not self.is_published:
            return reverse('blog:index')
        return reverse('blog:post', args=(self.slug,))
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.title)
        
        current_cover_name = str(self.cover.name) #Pega o nome do cover atual
        super_save = super().save(args, kwargs) # armazena salvamento em variável

        cover_changed = False
        if self.cover: #Se tiver um cover
            cover_changed = current_cover_name != self.cover.name #True se o cover foi mudado
        
        if cover_changed: #se foi mudado faz o redimensionamento da imagem
            resize_image(self.cover, 900, True, 70) #importado do images.py    
        
        return super_save #Salva
    
    def __str__(self):
        return self.title