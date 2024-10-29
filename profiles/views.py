# from django.shortcuts import render, redirect, reverse, get_object_or_404
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# from django.db.models import Q

# from .models import Profile

# # Create your views here.


def profile_list(request):
    users = User.objects.all()
    return users
