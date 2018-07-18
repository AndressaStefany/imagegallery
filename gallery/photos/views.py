from django.shortcuts import render
import os # os.getcwd()

from .models import Images


def index(request):
    latest_image_list = Images.objects.order_by('-date')[:5]
    context = {'latest_image_list': latest_image_list}
    print(os.getcwd())
    return render(request, 'photos/index.html', context)
