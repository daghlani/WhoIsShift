from back.models import FileObj, ShiftGroup
from django.contrib.auth.models import User
from django.shortcuts import Http404, redirect


def check_grp_owner(view_func):
    def wrap(request):
        grp_name = ShiftGroup.objects.get(owner__username=request.user)
        if request.user.is_authenticated:
            username = request.user.username
            if ShiftGroup.objects.get(name=grp_name).owner == User.objects.get(username=username):
                return view_func(request)
            else:
                return redirect('/')

    return wrap
