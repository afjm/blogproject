from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from blog.models import Post
from .forms import CommentForm


@require_POST
def comment(request, post_pk):
    # 获取被评论的文章
    post = get_object_or_404(Post, pk=post_pk)

    # Django将用户提供的数据封装在request.POST中, 这是一个类字典对象
    form = CommentForm(request.POST)

    if form.is_valid():
        comment_obj = form.save(commit=False)
        comment_obj.post = post
        comment_obj.save()

        messages.add_message(request, messages.SUCCESS, '评论发表成功！', extra_tags='success')
        return redirect(post)

    # context = {
    #     'post': post,
    #     'form': form,
    # }
    messages.add_message(request, messages.ERROR, '评论发表失败！请修改表单中的错误后重新提交。', extra_tags='danger')
    return render(request, 'comments/preview.html', {
        'post': post,
        'form': form,
    })
