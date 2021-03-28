from django.shortcuts import render


# Create your views here.

def homepageView(request, *args, **kwargs):
    if request.user.is_authenticated:
        context = {"user": request.user, "userType": request.user.type}
    else:
        context = {}
    return render(request, "index.html", context)
