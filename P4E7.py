points = {
    (0, 1): 2,
    (0, 2): 3.8,
    (0, 3): 2.7,
    (1, 2): 2.5,
    (1, 3): 4.1,
    (2, 3): 3.9,
}
coordinates = [0, 1, 3, 2, 0, 2]
def calculate_distance(coordinates, total = 0):
    for ave in range(len(coordinates) - 1):
        point1 = [coordinates[ave], coordinates[ave + 1]]
        point1.sort()
        if tuple(point1) in points:
            distance = points[tuple(point1)]
            total += distance
        print(tuple(point1))
        print(point1)
    return total
result = calculate_distance(coordinates)
print(result)