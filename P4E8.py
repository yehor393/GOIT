terra = [[1, 2, 5, 10], [2, 10, 2], [1, 3, 1]]
power = 1

def game(terra, power):
    for i in terra:
        for u in i:
            if power >= u:
                power += u
            elif power < u:
                break
    return power
print(game(terra, power))