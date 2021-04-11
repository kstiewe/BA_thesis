from django.core.files import File
from django.shortcuts import render, redirect

# Create your views here.
from Licencjat.settings import STATICFILES_DIRS
from Models.models import PhotoModel


def homepageView(request, *args, **kwargs):
    if request.user.is_authenticated:
        context = {"user": request.user}
    else:
        context = {}
    return render(request, "index.html", context)


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
    for x in range(202599):  # 202599
        f_name = attr_list[x].pop(0)
        meal_data = PhotoModel(
            file=File(
                open(
                    "C:/Users/kryst/PycharmProjects/BA_thesis/img_align_celeba/" + f_name,
                    'rb'))
        )
        meal_data.set_attributes([int(x) for x in attr_list[x]])
        meal_data.set_landmarks(land_list[x])
        meal_data.file.name = f_name
        meal_data.save()
    return redirect("home")
