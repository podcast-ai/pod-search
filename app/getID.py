from getSimilarity import calc_score


def get_matching_file_name(save_path, query_text: str) -> str:
    """Return the file name of the best match for the input."""
    with open(save_path, "r") as file:
        # Generate the dict in {audioID: Trans}
        d = dict([line.strip().split(",") for line in file])
        # Generate the dict in {ID: Score}
        for id in d:
            d[id] = calc_score(query_text, d[id])
        # Sort the {ID: Score} and pick the highest value
        sort_orders = sorted(d.items(), key=lambda x: x[1], reverse=True)
        # retreive the audioID by the highest similarity value
        file_name = sort_orders[0][0]
        return file_name
