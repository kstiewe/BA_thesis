from random import choice

from Models.models import PhotoModel, SelectionModel

PHOTOS = PhotoModel.objects.all()


# DONE
# TODO: REFACTOR
def linear_adding_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    for selection in selections:
        # IF SELECTION IS TRUE
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
        else:
            photos_ranked = [x - y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
    best_list = []
    biggest_score = -1000000
    for photo in PHOTOS:
        score = sum(
            [x * y for x, y in zip(photos_ranked, photo.get_attributes())])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


# DONE
# TODO: REFACTOR
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
    best_list = []
    biggest_score = -100000000000
    for photo in PHOTOS:
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


# DONE
# TODO: REFACTOR
def selection_average_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    liked = 0
    for selection in selections:
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
            liked += 1
    if liked > 0:
        for i in range(len(photos_ranked)):
            photos_ranked[i] /= liked
    best_list = []
    biggest_score = -1000000
    for photo in PHOTOS:
        score = sum(
            [x * y for x, y in zip(photos_ranked, photo.get_attributes())])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


# DONE
# TODO: REFACTOR
def average_human_offset_algorithm(user_model_instance, algorithm):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    photos_ranked = [0] * 40
    average_human = [0] * 40
    for photo in PHOTOS:
        average_human = [x + y for x, y in zip(average_human,
                                               photo.get_attributes())]
    photos_len = len(PHOTOS)
    for i in range(len(photos_ranked)):
        average_human[i] = average_human[i] / photos_len + 1
    for selection in selections:
        if selection.selection:
            photos_ranked = [x + y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
        else:
            photos_ranked = [x - y for x, y in zip(photos_ranked,
                                                   selection.photo.get_attributes())]
    best_list = []
    biggest_score = -10000000
    for photo in PHOTOS:
        score = sum(
            [x * (y / z) for x, y, z in
             zip(photos_ranked, photo.get_attributes(), average_human) if
             z > 0])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


# DONE
# TODO: REFACTOR
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
    best_list = []
    biggest_score = -1000000
    for photo in PHOTOS:
        score = 0
        attributes = photo.get_attributes()
        for x in range(40):
            if attributes[x] == 1:
                score += (plusone[x][0] / plusone[x][1])
            elif attributes[x] == -1:
                score += (minusone[x][0] / minusone[x][1])
        if score > biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


# DONE
# TODO: REFACTOR
def exponential_attribute_weights_on_test_sample_algorithm(user_model_instance,
                                                           algorithm,
                                                           added_landmarks=False):
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
    best_list = []
    biggest_score = -1000000
    for photo in PHOTOS:
        score = 0
        attributes = photo.get_attributes()
        for x in range(40):
            if attributes[x] == 1:
                score += (plusone[x][0] * plusone[x][0] * plusone[x][0] /
                          plusone[x][1])
            elif attributes[x] == -1:
                score += (minusone[x][0] * minusone[x][0] * minusone[x][0] /
                          minusone[x][1])
        if score > biggest_score:
            biggest_score = score
            if added_landmarks:
                if len(best_list) == 100:
                    best_list.pop(0)
                best_list.append(photo)
            else:
                best_list = [photo]

        elif score == biggest_score:
            if len(best_list) == 100:
                best_list.pop(0)
            best_list.append(photo)
    if added_landmarks:
        return best_list
    algorithm.photo = choice(best_list)
    algorithm.save()


# DONE
# TODO: REFACTOR
def average_landmarks(user_model_instance, algorithm, __photos=PHOTOS):
    selections = SelectionModel.objects.filter(user__exact=user_model_instance)
    __average_landmarks = [0] * 10
    liked = 0
    for selection in selections:
        if selection.selection:
            __average_landmarks = [x + y for x, y in zip(__average_landmarks,
                                                         selection.photo.get_landmarks())]
            liked += 1
    if liked > 0:
        for i in range(len(__average_landmarks)):
            __average_landmarks[i] /= liked
    best_list = []
    biggest_score = 1000000000
    for photo in __photos:
        score = sum(
            [abs(x - y) for x, y in
             zip(__average_landmarks, photo.get_landmarks())])
        if score < biggest_score:
            biggest_score = score
            best_list = [photo]
        elif score == biggest_score:
            best_list.append(photo)
    algorithm.photo = choice(best_list)
    algorithm.save()


# DONE
# TODO: REFACTOR
def eawots_average_landmarks(user_model_instance, algorithm):
    eawots_photos = exponential_attribute_weights_on_test_sample_algorithm(
        user_model_instance, algorithm, added_landmarks=True)
    average_landmarks(user_model_instance, algorithm, __photos=eawots_photos)
