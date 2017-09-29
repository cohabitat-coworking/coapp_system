from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.models import Profile


@login_required(login_url="login/")
def home(request):
    profile = Profile.objects.get(user=request.user.id)

    return render(
        request,
        'menu.html', {"profile": profile}
    )
