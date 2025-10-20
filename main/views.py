from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_POST,require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .constants import INDEX_URL_NAME, CREATE_POST_URL_NAME, CREATE_POST_FORM_URL_NAME
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
    
@csrf_protect
@require_http_methods(["GET", "POST"])
def update_post(request, pk):
    """
    Post object update view
    - GET → form with instance render
    - POST → validate, save, success/fail message, redirect
    - Post.DoesNotExist → error message, redirect to index
    """
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        messages.error(request, "Id not found")
        return redirect(INDEX_URL_NAME)  # redirect instead of render

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Update successfully")
            return redirect(INDEX_URL_NAME)
        else:
            messages.error(request, "Update failed. Check the data.")
    else:
        form = PostForm(instance=post)  # Correct usage of ModelForm with instance

    return render(request, CREATE_POST_URL_NAME, {'form': form})

