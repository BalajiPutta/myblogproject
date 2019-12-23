from django.shortcuts import render,get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from blog.models import Post,Comments
from django.core.mail import send_mail
from .forms import EmailSendForm,CommentForm,SignUp_form
from django.contrib.auth.decorators import login_required
from taggit.models import Tag
@login_required
def post_list_view(request,tag_slug=None):
    post_list = Post.objects.all()
    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])
    paginator=Paginator(post_list,3)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(page_number)
    return render(request,'blog/post_list.html',{'post_list':post_list,'tag':tag,'sidebar':True})
@login_required
def post_detail_view(request,year,month,day,post):
    post1=Post.objects.get(title=post,status='published',
                           publish__year=year)
                           #publish__month=month)
                           # publish__day=day)
    commentss=post1.commentss.filter(active=True)
    csubmit=False
    current_user = request.user
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            name=current_user.username
            email=current_user.email
            comment=request.POST.get('comment')
            data=Comments(name=name,email=email,comment=comment)
            data.post=post1
            data.save()
            csubmit=True
    else:
        form=CommentForm()
    return render(request,'blog/post_detail.html',{'post2':post1,'sidebar':True,'comments':commentss,'form':form,'csubmit':csubmit})
def mail_send_view(request,id):
    post=get_object_or_404(Post,id=id,status='published')
    sent=False
    if request.method=='POST':
        form=EmailSendForm(request.POST)
        if form.is_valid():
            current_user = request.user
            cd=form.cleaned_data
            subject='{}({}) recomended you to read {}'.format(current_user.username,current_user.email,post.title)
            post_url = request.build_absolute_uri(post.get_absolute_url())
            message='Read post at:\n {}\n\n{}\'s comments:\n {}'.format(post_url,current_user.username,cd['comments'])

            send_mail(subject,message,current_user.email,[cd['to'],'pavanchaitanya9@gmail.com'])
            sent=True
    else:
        form=EmailSendForm()
    return render(request,'blog/sharebymail.html',{'form':form,'post':post,'sidebar':True,"sent":sent})


def user_post(request,author_id):
    post=Post.objects.filter(author=author_id,status='published')

    return render(request,'blog/userposts.html',{'post':post})
def signup_view(request):
    form =SignUp_form()
    if request.method=='POST':
        f=SignUp_form(request.POST)
        user=f.save()
        user.set_password(user.password)
        f.save()
        return HttpResponseRedirect('/accounts/login')
    return render(request,'blog/signup.html',{'form':form,'sidebar':False})
def logout_view(request):
    return render(request,'blog/logout.html',{'sidebar':False})


def dashboard_view(request):
    posts=Post.objects.filter(author_id=request.user.id)
    return render(request,'blog/dashboard.html',{'posts':posts,'dashboard':True})


def createpost_view(request):
    if request.method=='POST':
        title=request.POST.get('title')
        content=request.POST.get('content')
        status=request.POST.get('status')
        tag1=request.POST.get('tags')
        data=Post(title=title,slug=title.replace(" ", "-"),body=content,status=status,author_id=request.user.id)
        data.save()
        tag1=tag1.split(',')
        post=Post.objects.get(title=title,author_id=request.user.id,slug=title.replace(" ", "-"))
        print(post.publish,post.created,post.updated)
        for i in tag1:
            post.tags.add(i)
        posts = Post.objects.filter(author_id=request.user.id)
        return render(request, 'blog/dashboard.html', {'posts': posts, 'dashboard': True})

    else:
        return render(request,'blog/createpost.html')


def deletepost_view(request,slug):
    post=Post.objects.get(slug=slug,author_id=request.user.id)
    post.delete()
    posts = Post.objects.filter(author_id=request.user.id)
    return render(request, 'blog/dashboard.html', {'posts': posts, 'dashboard': True})


def updatepost_view(request,slug):
    post=Post.objects.get(slug=slug,author_id=request.user.id)
    if request.method=='POST':
        id=post.id
        title=request.POST.get('title')
        content=request.POST.get('content')
        status=request.POST.get('status')
        tag1=request.POST.get('tags')
        data=Post(id=id,title=title,created=post.created,slug=title.replace(" ", "-"),body=content,status=status,author_id=request.user.id)
        data.save()
        tag1=tag1.split(',')
        post=Post.objects.get(title=title,author_id=request.user.id,slug=title.replace(" ", "-"))
        print(post.publish, post.created, post.updated)

        for i in tag1:
            post.tags.add(i)
        posts = Post.objects.filter(author_id=request.user.id)
        return render(request, 'blog/dashboard.html', {'posts': posts, 'dashboard': True})
    else:
        return render(request,'blog/updatepost.html',{'post':post})