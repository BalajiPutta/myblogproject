from blog.models import Post
from django import template
from django.db.models import Count
register=template.Library()
@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.inclusion_tag('blog/latest123.html')
def show_latest_posts(count=3):
    latest_posts=Post.objects.order_by('-publish')[:count]
    return {'latestposts':latest_posts}

@register.simple_tag
def get_most_coomented_posts(count=3):
    return Post.objects.annotate(total_comments=Count('commentss')).order_by('-total_comments')[:count]