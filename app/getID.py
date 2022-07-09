from getSimilarity import calc_score


def getID(save_path, sentence):
    with open(save_path, "r") as file:
        # Generate the dict in {audioID: Trans}
        d = dict([line.strip().split(",") for line in file])
        # Generate the dict in {ID: Score}
        for id in d:
            d[id] = calc_score(sentence, d[id])
        # Sort the {ID: Score} and pick the highest value
        sort_orders = sorted(d.items(), key=lambda x: x[1], reverse=True)
        # retreive the audioID by the highest similarity value
        ID = sort_orders[0][0]
        return ID
