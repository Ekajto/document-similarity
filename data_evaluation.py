from nltk import edit_distance


def calculate_similarity(replaced_tokens_list):
    # Get the length of the list
    n = len(replaced_tokens_list)

    # Initialize an empty matrix
    matrix = [[0 for _ in range(n)] for _ in range(n)]

    # Loop through the list and compute the edit distance between each pair of strings
    for i in range(n):
        for j in range(n):
            # Calculate the edit distance between the ith and jth strings
            distance = edit_distance(replaced_tokens_list[i], replaced_tokens_list[j])
            # Update the matrix with the calculated distance
            matrix[i][j] = distance

    return matrix
