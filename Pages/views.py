from random import choice, sample

from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.db.models import QuerySet
from django.shortcuts import render, redirect

# Create your views here.
from Licencjat.settings import STATICFILES_DIRS
from Models.models import PhotoModel, UserModel, SelectionModel, AlgorithmModel
from Pages import algorithms
from .apps import get_client_ip
from numpy import zeros


def homepageView(request, *args, **kwargs):
    user_ip = get_client_ip(request)
    context = {}
    if not UserModel.objects.filter(ip__exact=user_ip):
        user_model_instance = UserModel()
        user_model_instance.ip = user_ip
        user_model_instance.save()
        photos = sample(list(PhotoModel.objects.all()), 100)
        for photo in photos:
            SelectionModel.objects.create(user=user_model_instance, photo=photo)
    else:
        user_model_instance = UserModel.objects.filter(ip__exact=user_ip)[
            0]
    if not user_model_instance.has_finished:
        selection = \
            SelectionModel.objects.filter(user__exact=user_model_instance,
                                          selection=None)[0]
        if request.method == 'POST':
            if 'likebutton' in request.POST:
                selection.selection = True
            elif 'dislikebutton' in request.POST:
                selection.selection = False
            user_model_instance.selection_count += 1
            user_model_instance.save()
            selection.save()
            if user_model_instance.selection_count == 100:
                user_model_instance.has_finished = True
                user_model_instance.save()
                return redirect("results")
            selection = SelectionModel.objects.filter(
                user__exact=user_model_instance,
                selection=None)[0]
        context["photo_loc"] = "img/" + selection.photo.file
        context["selections_left"] = "Zostało Ci " + str(
            100 - int(
                user_model_instance.selection_count)) + " zdjęć do wybrania."
        return render(request, "index.html", context)
    else:
        return redirect("results")


# TODO: REFACTOR
def resultsView(request, *args, **kwargs):
    user_ip = get_client_ip(request)
    context = {}
    if not UserModel.objects.filter(ip__exact=user_ip):
        redirect('home')
    else:
        user_model_instance = UserModel.objects.filter(ip__exact=user_ip)[
            0]
        if not user_model_instance.has_finished:
            redirect('home')
    if not AlgorithmModel.objects.filter(user__exact=user_model_instance):
        for x in AlgorithmModel.TYPE_CHOICES:
            AlgorithmModel.objects.create(user=user_model_instance, type=x[0])
    if not user_model_instance.has_finished_results:
        algorithm = \
            AlgorithmModel.objects.filter(user__exact=user_model_instance,
                                          selection=None)[
                0]
        if algorithm.type == '1' and algorithm.photo is None:
            algorithms.linear_adding_algorithm(user_model_instance, algorithm)
        elif algorithm.type == '2' and algorithm.photo is None:
            algorithms.exponential_adding_algorithm(user_model_instance,
                                                    algorithm)
        elif algorithm.type == '3' and algorithm.photo is None:
            algorithms.selection_average_algorithm(user_model_instance,
                                                   algorithm)
        elif algorithm.type == '4' and algorithm.photo is None:
            algorithms.average_human_offset_algorithm(user_model_instance,
                                                      algorithm)
        elif algorithm.type == '5' and algorithm.photo is None:
            algorithms.attribute_weights_on_test_sample_algorithm(
                user_model_instance,
                algorithm)
        elif algorithm.type == '6' and algorithm.photo is None:
            algorithms.exponential_attribute_weights_on_test_sample_algorithm(
                user_model_instance, algorithm)
        elif algorithm.type == '7' and algorithm.photo is None:
            algorithms.average_landmarks(
                user_model_instance, algorithm)
        elif algorithm.type == '8' and algorithm.photo is None:
            algorithms.eawots_average_landmarks(
                user_model_instance, algorithm)
        if request.method == 'POST':
            if 'likebutton' in request.POST:
                algorithm.selection = True
            elif 'dislikebutton' in request.POST:
                algorithm.selection = False
            algorithm.save()
            if not AlgorithmModel.objects.filter(
                    user__exact=user_model_instance):
                user_model_instance.has_finished_results = True
                user_model_instance.save()
                user_photos = AlgorithmModel.objects.filter(
                    user__exact=user_model_instance)

                user_photos = AlgorithmModel.objects.filter(
                    user__exact=user_model_instance)
                user_photos = list(user_photos)
                for i, alg in enumerate(user_photos):
                    user_photos[i] = "img/" + alg.photo.file
                context["liked_list"] = user_photos
                return render(request, "thankyou.html", context)
            try:
                algorithm = \
                    AlgorithmModel.objects.filter(
                        user__exact=user_model_instance,
                        selection=None)[0]
                if algorithm.type == '1' and algorithm.photo is None:
                    algorithms.linear_adding_algorithm(user_model_instance,
                                                       algorithm)
                elif algorithm.type == '2' and algorithm.photo is None:
                    algorithms.exponential_adding_algorithm(user_model_instance,
                                                            algorithm)
                elif algorithm.type == '3' and algorithm.photo is None:
                    algorithms.selection_average_algorithm(user_model_instance,
                                                           algorithm)
                elif algorithm.type == '4' and algorithm.photo is None:
                    algorithms.average_human_offset_algorithm(
                        user_model_instance,
                        algorithm)
                elif algorithm.type == '5' and algorithm.photo is None:
                    algorithms.attribute_weights_on_test_sample_algorithm(
                        user_model_instance,
                        algorithm)
                elif algorithm.type == '6' and algorithm.photo is None:
                    algorithms.exponential_attribute_weights_on_test_sample_algorithm(
                        user_model_instance, algorithm)
                elif algorithm.type == '7' and algorithm.photo is None:
                    algorithms.average_landmarks(
                        user_model_instance, algorithm)
                elif algorithm.type == '8' and algorithm.photo is None:
                    algorithms.eawots_average_landmarks(
                        user_model_instance, algorithm)
            except:
                user_model_instance.has_finished_results = True
                user_model_instance.save()
        context["photo_loc"] = "img/" + algorithm.photo.file
        return render(request, "results.html", context)
    else:
        user_photos = AlgorithmModel.objects.filter(
            user__exact=user_model_instance)
        user_photos = list(user_photos)
        for i, alg in enumerate(user_photos):
            user_photos[i] = "img/" + alg.photo.file
        context["liked_list"] = user_photos
        return render(request, "thankyou.html", context)


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
        meal_data = PhotoModel()
        meal_data.file = f_name
        meal_data.set_attributes([int(x) for x in attr_list[x]])
        meal_data.set_landmarks(land_list[x])
        meal_data.save()
    return redirect("home")


@login_required
def chartView(request, *args, **kwargs):
    labels = []
    users = UserModel.objects.all()
    for name in AlgorithmModel.TYPE_CHOICES:
        labels.append(name)
    all_to_add = []
    for user in users:
        if user.has_finished_results:
            algorithms = list(AlgorithmModel.objects.filter(user__exact=user))
            all_to_add.append(algorithms)
    data = list(zeros(len(labels)))
    for user_sel_set in all_to_add:
        for i, alg in enumerate(user_sel_set):
            if alg.selection:
                data[i] += 1
    data_raw = data
    data = [(x / len(all_to_add)) * 100 for x in data]
    return render(request, 'charts.html', {
        'UniqueValidUsers': len(all_to_add),
        'DataRaw': data_raw,
        'labels': labels,
        'data': data,
    })


@login_required
def fixView(request, *args, **kwargs):
    users = UserModel.objects.filter(has_finished=True, selection_count=100,
                                     has_finished_results=False)
    users = list(users)
    for user in users:
        try:
            AlgorithmModel.objects.filter(user__exact=user, selection=None)[0]
        except:
            user.has_finished_results = True
            user.save()
    return redirect("home")
