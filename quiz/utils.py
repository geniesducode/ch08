def get_rank(score_percentage):
    ranks = [
        [100, "Impressionnant!", "Wow! Y a de la triche dans l'air."],
        [75, "Bravo!", "Tu en sais plus que la plupart des gens!"],
        [50, "Pas mal", "Une sur deux, c'est pas encore ça."],
        [25, "Y a du boulot...", "C'est mieux que rien."],
        [0, "Pas bravo!", "Il fallait le faire."],
    ]

    for rank in ranks:
        if rank[0] <= score_percentage:
            return {'title': rank[1], 'description': rank[2]}

    raise ValueError("Invalid score %s" % score_percentage)
