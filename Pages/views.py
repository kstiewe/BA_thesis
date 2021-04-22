from random import choice

from django.core.files import File
from django.db.models import QuerySet
from django.shortcuts import render, redirect

# Create your views here.
from Licencjat.settings import STATICFILES_DIRS
from Models.models import PhotoModel, UserModel, SelectionModel


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def homepageView(request, *args, **kwargs):
    user_ip = get_client_ip(request)
    context = {}
    photolist = list(PhotoModel.objects.all())
    if not list(UserModel.objects.filter(ip__exact=user_ip)):
        user_model_instance = UserModel()
        user_model_instance.ip = user_ip
    else:
        user_model_instance = list(UserModel.objects.filter(ip__exact=user_ip))[
            0]
    user_model_instance.save()
    if not user_model_instance.has_finished:
        if list(SelectionModel.objects.filter(selection=None,
                                              user__exact=user_model_instance)):
            selection = list(SelectionModel.objects.filter(selection=None,
                                                           user__exact=user_model_instance))[
                0]
            photo = selection.photo
        else:
            photo = choice(photolist)
            selection = SelectionModel()
            selection.photo = photo
            selection.user = user_model_instance
        if request.method == 'POST' and 'likebutton' in request.POST:
            selection.selection = True
            user_model_instance.selection_count += 1
        if request.method == 'POST' and 'dislikebutton' in request.POST:
            selection.selection = False
            user_model_instance.selection_count += 1
        if user_model_instance.selection_count == 100:
            user_model_instance.has_finished = True
        user_model_instance.save()
        selection.save()
        if request.method == 'POST':
            photo = choice(photolist)
            selection = SelectionModel()
            selection.photo = photo
            selection.user = user_model_instance
        context["photo_loc"] = "img/" + photo.file
        return render(request, "index.html", context)
    else:
        return render(request, "base.html", context)


def mealsView(request, *args, **kwargs):
    land_loc = STATICFILES_DIRS[0] + "/landmarks.txt"
    land_list = []
    attr_loc = STATICFILES_DIRS[0] + "/attributes.txt"
    attr_list = []
    with open(land_loc, encoding='utf-8') as f:
        for line in f.readlines():
            temp = list(line.rstrip().split()[1:])
            temp = [int(x) for x in temp]
            land_list.append(temp)
    with open(attr_loc, encoding='utf-8') as f:
        for line in f.readlines():
            attr_list.append(list(line.rstrip().split()))
    for x in range(100):  # 202599
        f_name = attr_list[x].pop(0)
        meal_data = PhotoModel()
        meal_data.file = f_name
        meal_data.set_attributes([int(x) for x in attr_list[x]])
        meal_data.set_landmarks(land_list[x])
        meal_data.save()
    return redirect("home")
