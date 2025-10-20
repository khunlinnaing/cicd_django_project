from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.urls import reverse
from django.contrib import messages
from .constants import INDEX_URL_NAME, CREATE_POST_URL_NAME, CREATE_POST_FORM_URL_NAME, UPDATE_POST_FORM_URL_NAME
from main.models import Post
from main.forms import PostForm

@require_GET
def index(request):
    items = Post.objects.all()
    return render(request, 'index.html', {'items': items})


@require_GET
def get_detail(request, pk):
    try:
        item = Post.objects.get(pk=pk)
        return render(request, 'detail.html', {'item': item})
    except Post.DoesNotExist:
        messages.error(request, "Id not found")
        return redirect(INDEX_URL_NAME)


@require_GET
def get_create_post(request):
    form = PostForm()
    return render(request, CREATE_POST_URL_NAME, {'form': form, 'action': CREATE_POST_FORM_URL_NAME})

@require_POST
def post_create_post(request):
    form = PostForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "successfully")
        return redirect(INDEX_URL_NAME)
    else:
        messages.error(request, "fail")
        return render(request, CREATE_POST_URL_NAME, {'form': form, 'action': CREATE_POST_FORM_URL_NAME})



@require_GET
def get_update_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        form = PostForm(instance=post)
        return render(
            request,
            CREATE_POST_URL_NAME,
            {'form': form, 'action': reverse(UPDATE_POST_FORM_URL_NAME, args=[pk])}
        )
    except Post.DoesNotExist:
        messages.error(request, "Id not found")
        return redirect(INDEX_URL_NAME)


@require_POST
def post_update_post(request, pk):
    """
    POST request:
    - form data ကို validate → success ဖြစ်ရင် DB update
    - invalid ဖြစ်ရင် error message ပြပြီး ပြန်ပြပါ
    - Post မရှိရင် redirect + message
    """
    try:
        post = Post.objects.get(pk=pk)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            messages.success(request, "Update successfully")
            return redirect(INDEX_URL_NAME)
        else:
            messages.error(request, "Update failed. Check the data.")
            return render(
                request,
                CREATE_POST_URL_NAME,
                {'form': form, 'action': UPDATE_POST_FORM_URL_NAME}
            )
    except Post.DoesNotExist:
        messages.error(request, "Id not found")
        return redirect(INDEX_URL_NAME)


