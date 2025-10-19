from django.shortcuts import render
from django.views.decorators.http import require_GET
from .models import Item


@require_GET
def index(request):
    items = Item.objects.all()
    return render(request, 'index.html', {'items': items})
