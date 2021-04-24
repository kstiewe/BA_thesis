from random import choice

from Models.models import AlgorithmModel, PhotoModel, UserModel, SelectionModel


def linear_adding_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    for selection in selections:
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
        else:
            photos_ranked = [x - y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
    photos = PhotoModel.objects.all()
    best_list = []
    biggest_score = -1000000
    for photo in photos:
        score = sum(
            [x * y for x, y in zip(photos_ranked, photo.get_attributes())])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


def exponential_adding_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    for selection in selections:
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
        else:
            photos_ranked = [x - y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
    photos = PhotoModel.objects.all()
    best_list = []
    biggest_score = -100000000000
    for photo in photos:
        score = sum(
            [x * x * x * y for x, y in
             zip(photos_ranked, photo.get_attributes())])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


def selection_average_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    for selection in selections:
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
        else:
            photos_ranked = [x - y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
    print(photos_ranked)
    photos = PhotoModel.objects.all()
    for i in range(len(photos_ranked)):
        if photos_ranked[i] > 0:
            photos_ranked[i] = 1
        else:
            photos_ranked[i] = -1
    best_list = []
    biggest_score = 0
    for photo in photos:
        score = 0
        for x, y in zip(photo.get_attributes(), photos_ranked):
            if x == y:
                score += 1
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


def average_human_offset_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    for selection in selections:
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
        else:
            photos_ranked = [x - y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
    photos = PhotoModel.objects.all()
    best_list = []
    biggest_score = -1000000
    for photo in photos:
        score = sum(
            [x * y for x, y in zip(photos_ranked, photo.get_attributes())])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


def attribute_weights_on_test_sample_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    # photos_ranked = [0] * 40
    plusone = [[0, 0]] * 40
    minusone = [[0, 0]] * 40
    for selection in selections:
        attributes = selection.photo.get_attributes()
        isliked = selection.selection
        for x in range(40):
            if attributes[x] == 1:
                plusone[x][1] += 1
                if isliked:
                    plusone[x][0] += 1
            elif attributes[x] == -1:
                minusone[x][1] += 1
                if isliked:
                    minusone[x][0] += 1
    photos = PhotoModel.objects.all()
    best_list = []
    biggest_score = -1000000
    for photo in photos:
        score = 0
        attributes = photo.get_attributes()
        for x in range(40):
            if attributes[x] == 1:
                score += attributes[x] * (plusone[x][0] / plusone[x][1])
            elif attributes[x] == -1:
                score += attributes[x] * (minusone[x][0] / minusone[x][1])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


def exponential_attribute_weights_on_test_sample_algorithm(user_model_instance,
                                                           algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    # photos_ranked = [0] * 40
    plusone = [[0, 0]] * 40
    minusone = [[0, 0]] * 40
    for selection in selections:
        attributes = selection.photo.get_attributes()
        isliked = selection.selection
        for x in range(40):
            if attributes[x] == 1:
                plusone[x][1] += 1
                if isliked:
                    plusone[x][0] += 1
            elif attributes[x] == -1:
                minusone[x][1] += 1
                if isliked:
                    minusone[x][0] += 1
    photos = PhotoModel.objects.all()
    best_list = []
    biggest_score = -1000000
    for photo in photos:
        score = 0
        attributes = photo.get_attributes()
        for x in range(40):
            if attributes[x] == 1:
                score += attributes[x] * (
                            plusone[x][0] * plusone[x][0] * plusone[x][0] /
                            plusone[x][1])
            elif attributes[x] == -1:
                score += attributes[x] * (
                            minusone[x][0] * minusone[x][0] * minusone[x][0] /
                            minusone[x][1])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()

