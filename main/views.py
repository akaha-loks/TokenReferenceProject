from django.shortcuts import render, get_object_or_404
from .models import Post, Token
from django.db.models import Q

def post_list(request, token_id=None):
    tokens = Token.objects.all()
    query = request.GET.get('q', '')

    posts = Post.objects.all()

    if token_id:
        posts = posts.filter(token_id=token_id)

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        )

    return render(request, 'posts/post_list.html', {
        'posts': posts,
        'tokens': tokens,
        'selected_token': token_id,
        'query': query,
    })

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})

