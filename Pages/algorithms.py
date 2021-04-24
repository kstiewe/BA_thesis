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
    print(photos_ranked)
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
    print(best_list)
    return choice(best_list)


def exponential_adding_algorithm(user_model_instance, algorithm):
    pass


def selection_average_algorithm(user_model_instance, algorithm):
    pass


def average_human_offset_algorithm(user_model_instance, algorithm):
    pass


def attribute_weights_on_test_sample_algorithm(user_model_instance, algorithm):
    pass


def exponential_attribute_weights_on_test_sample_algorithm(user_model_instance,
                                                           algorithm):
    pass
