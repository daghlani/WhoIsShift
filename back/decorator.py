from back.models import FileObj, ShiftGroup
from django.contrib.auth.models import User
from django.shortcuts import Http404, redirect
from back.logger import logger


def check_grp_owner(view_func):
    def wrap(request):
        try:
            grp_name = ShiftGroup.objects.get(owner__username=request.user)
            if request.user.is_authenticated:
                username = request.user.username
                if ShiftGroup.objects.get(pr_name=grp_name).owner == User.objects.get(username=username):
                    return view_func(request)
                else:
                    return redirect('/')
        except ShiftGroup.DoesNotExist:
            raise Http404
        except Exception as err:
            logger.error(err)

    return wrap
