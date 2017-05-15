DIAG_COEFF = 0.709  # This for diagonal vector normalization


def move_to_vec(move):
    # Normalizing the move vector
    vec = move[1][0] - move[0][0], move[1][1] - move[0][1]
    if vec[0] == vec[1] != 0:
        return vec[0] * DIAG_COEFF, vec[1] * DIAG_COEFF
    else:
        return vec


