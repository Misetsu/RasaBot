import pickle


def eng(name):
    with open('actions/dict_place.pkl', 'rb') as f:
        dict_place = pickle.load(f)

    try:
        place = dict_place[name]
    except KeyError:
        place = "null"

    return place
