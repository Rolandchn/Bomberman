
import math

if __name__ == "__main__":
    valued_grid = []

    map_size = 15
    nb_grid = (13, 13)

    valued_grid.append([0 for i in range(map_size)])
    valued_grid.append([0 for i in range(map_size)])

    nb_row, nb_column = nb_grid

    column_increment = 0
    row_increment = 0

    for row_value in range(math.ceil(nb_row / 2)):
        buff = [0, 0]
        
        for column_value in range(math.ceil(nb_column / 2)):
            buff.insert(len(buff) // 2, column_value * 100 + column_increment)
            buff.insert(len(buff) // 2, column_value * 100 + column_increment)

        if nb_column % 2 != 0:
            buff.pop(len(buff) // 2)

        valued_grid.insert(len(valued_grid) // 2, buff)
        valued_grid.insert(len(valued_grid) // 2, buff)

        column_increment += 100
        row_increment += 100

    if nb_row % 2 != 0:
        valued_grid.pop(len(valued_grid) // 2)

    for _ in valued_grid:
        print(_)