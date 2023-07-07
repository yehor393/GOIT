def split_list(grade):
    average = 0
    for ava in grade:
        average =+ ava
    min = []
    max = []
    if grade < average:
        min.add(grade) 
    else:
        max.add(grade) 
    point = (min, max)
    return point