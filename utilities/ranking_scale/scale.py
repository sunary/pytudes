__author__ = 'sunary'


import math


def standard_competition_ranking(sequence):
    """
    Examples:
        >>> standard_competition_ranking([1, 2, 2, 4])
        [1, 2, 2, 4]
    """
    len_sequence = len(sequence)

    order = get_order(sequence)
    sequence = sorted(sequence)
    index = [1] * len_sequence

    len_same_ranking = 1
    for i in range(1, len_sequence):
        if sequence[i] == sequence[i - 1]:
            index[i] = index[i - 1]
            len_same_ranking += 1
        else:
            index[i] = index[i - 1] + len_same_ranking
            len_same_ranking = 1

    ranking = [1] * len_sequence
    for i in range(len_sequence):
        ranking[i] = index[order[i] - 1]

    return ranking


def modified_competition_ranking(sequence):
    """
    Examples:
        >>> modified_competition_ranking([1, 2, 2, 4])
        [1, 3, 3, 4]
    """
    len_sequence = len(sequence)

    order = get_order(sequence)
    sequence = sorted(sequence)
    index = [1] * len_sequence

    len_same_ranking = 1
    first_value = True
    for i in range(1, len_sequence):
        if sequence[i] == sequence[i - 1]:
            index[i] = index[i - 1]
            len_same_ranking += 1
            if i == len_sequence - 1:
                value_same_ranking = index[i] + len_same_ranking - 1
                for j in range(i - len_same_ranking + 1, i + 1):
                    index[j] = value_same_ranking
        else:
            index[i] = index[i - 1] + len_same_ranking
            if first_value:
                value_same_ranking = 1
                first_value = False
            else:
                value_same_ranking = index[i] - 1
            for j in range(i - len_same_ranking, i):
                index[j] = value_same_ranking

            if i == len_sequence - 1:
                index[i] = len_sequence
            else:
                len_same_ranking = 1

    ranking = [1] * len_sequence
    for i in range(len_sequence):
        ranking[i] = index[order[i] - 1]

    return ranking


def dense_ranking(sequence):
    """
    Examples:
        >>> dense_ranking([1, 2, 2, 4])
        [1, 2, 2, 3]
    """
    len_sequence = len(sequence)

    order = get_order(sequence)
    sequence = sorted(sequence)
    index = [1] * len_sequence

    for i in range(1, len_sequence):
        if sequence[i] == sequence[i - 1]:
            index[i] = index[i - 1]
        else:
            index[i] = index[i - 1] + 1

    ranking = [1] * len_sequence
    for i in range(len_sequence):
        ranking[i] = index[order[i] - 1]

    return ranking


def ordinal_ranking(sequence):
    """
    Examples:
        >>> ordinal_ranking([1, 2, 2, 4])
        [1, 2, 3, 4]
    """
    return get_order(sequence)


def fractional_ranking(sequence):
    """
    Examples:
        >>> fractional_ranking([1, 2, 2, 4])
        [1.0, 2.5, 2.5, 4.0]
    """
    len_sequence = len(sequence)

    order = get_order(sequence)
    sequence = sorted(sequence)
    index = order[::]

    len_same_ranking = 1
    for i in range(1, len_sequence):
        if sequence[i] == sequence[i - 1]:
            len_same_ranking += 1
            if i == len(sequence) - 1:
                value_same_ranking = sum([x + 1 for x in range(i - len_same_ranking + 1, i + 1)])*1.0/len_same_ranking
                for j in range(i - len_same_ranking + 1, i + 1):
                    index[j] = value_same_ranking
        else:
            value_same_ranking = sum([x + 1 for x in range(i - len_same_ranking, i)])*1.0/len_same_ranking
            for j in range(i - len_same_ranking, i):
                index[j] = value_same_ranking

            if i == len_sequence - 1:
                index[i] = len_sequence * 1.0
            else:
                len_same_ranking = 1

    ranking = [1] * len_sequence
    for i in range(len_sequence):
        ranking[i] = index[order[i] - 1]

    return ranking


def get_order(sequence):
    """
    Examples:
        >>> get_order([5, 3, 7, 2])
        [3, 2, 4, 1]
    """
    len_sequence = len(sequence)
    order = [0] * len_sequence
    mark_ordered = [False] * len_sequence

    sorted_sequence = sorted(sequence)
    for i in range(len_sequence):
        for j in range(len_sequence):
            if not mark_ordered[j] and sequence[i] == sorted_sequence[j]:
                order[i] = j + 1
                mark_ordered[j] = True
                break
    return order


def percentile(sequence):
    max_sequence = max(sequence)
    return [x*100.0/max_sequence for x in sequence]


def minmax(sequence):
    min_sequence = sequence[0]
    max_sequence = sequence[0]
    for x in sequence[1:]:
        if min_sequence > x:
            min_sequence = x
        elif max_sequence < x:
            max_sequence = x
    return min_sequence, max_sequence


def scale_data(data, data_range=(-12, 15), feature_range=(0, 100)):
    """
    Scaling a data point to feature_range using data_range

    Args:
        data (float): a data point to be scaled
        data_range (tuple): the tuple of (min, max) range represents the data value range
        feature_range (tuple): the tuple of (min, max) range to scale the column to

    Returns:
        scaled data
    """
    if data >= 1.0:
        data = math.log10(data) - data_range[0]
    elif -1 <= data < 1.0:
        data = -data_range[0]
    else:
        data = -math.log10(math.fabs(data)) - data_range[0]

    scaled_data = feature_range[0] + data * (feature_range[1] - feature_range[0]) / (data_range[1] - data_range[0])

    if scaled_data < feature_range[0]:
        return feature_range[0]
    elif scaled_data > feature_range[1]:
        return feature_range[1]
    else:
        return scaled_data


if __name__ == '__main__':
    import doctest
    doctest.testmod()
