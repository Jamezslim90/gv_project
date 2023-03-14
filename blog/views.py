from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator , EmptyPage, PageNotAnInteger 
from taggit.models import Tag
from django.db.models import Count



"""
class PostListView (ListView):
    model: Post
    context_object_name = 'post_list' 
    template_name: 'blog/post_list.html'
   
    
    def get_queryset(self):
          return Post.published.all()
"""

"""
class PostDetailView (DetailView):

    model: Post
    context_object_name = 'post' 
   
    template_name: 'blog/post_detail.html'

    def get_queryset(self):
          return Post.objects.order_by('pk')
"""

def post_list(request, tag_slug=None):
    post_list = Post.published.all()

    # All Tag Listing 
    tags = Tag.objects.all()
    querytags = tags.annotate(num_times=Count('taggit_taggeditem_items'))

    #List similar post bt tag
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    
    #Latest Post
    latest_posts = Post.published.order_by('-publish')[:4]

    # Pagination with 10 posts per page
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                 'blog/post_list.html',
                 {'posts': posts, 'querytags': querytags, 'tag': tag, 'latest_posts': latest_posts})






def post_detail(request, year, month, day, post):


        post = get_object_or_404(Post, status=Post.Status.PUBLISHED,slug=post, 
                publish__year=year,publish__month=month, publish__day=day) 

        post_tags_ids = post.tags.values_list('id', flat=True)
        similar_posts = Post.published.filter(tags__in=post_tags_ids)\
                        .exclude(id=post.id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                        .order_by('-same_tags','-publish')[:4]   

        return render(request,'blog/post_detail.html',{'post': post })
 