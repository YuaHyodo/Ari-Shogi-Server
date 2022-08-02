def update_rate(result, rate1, rate2):
    k = 32
    games = sum(result)
    r = result[0] / games
    w1 = 1.0 / (10 ** ((rate2 - rate1) / 400) + 1)
    w2 = 1.0 / (10 ** ((rate1 - rate2) / 400) + 1)
    new_rate1 = rate1 + k * (result[0] - games * w1)
    new_rate2 = rate2 + k * (result[1] - games * w2)
    return new_rate1, new_rate2
