from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib import messages
from .models import *
from .forms import *

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
        return redirect('website:index')
    
@require_http_methods(["GET", "POST"])
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "successfully")
            return redirect('website:index')
        else:
            messages.error(request, "fail")
            return render(request, 'create_post.html', {'form': form})
    else:
        form = PostForm()
        return render(request, 'create_post.html', {'form': form})

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
        return redirect('website:index')  # redirect instead of render

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Update successfully")
            return redirect('website:index')
        else:
            messages.error(request, "Update failed. Check the data.")
    else:
        form = PostForm(instance=post)  # Correct usage of ModelForm with instance

    return render(request, 'create_post.html', {'form': form})

