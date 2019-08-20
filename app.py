import pandas as pd
import numpy as np
from tabulate import tabulate

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


dataset = None
preview_dataset = None


def prepare_datasets():
    global dataset, preview_dataset

    nrows, ncols = [], []
    pre_rows, pre_cols = [], []

    # Initalize table
    change = False
    for i in range(1, 257):
        led_max_count = i % 16

        if (led_max_count != 0):
            nrows.append(str(i-1))
            # pre_rows.append('.')
            pre_rows.append('')
        else:
            nrows.append(str(i-1))
            # pre_rows.append('.')
            pre_rows.append('')

            if(change):
                ncols.append(nrows[::-1])
                change = False
            else:
                ncols.append(nrows)
                change = True
            pre_cols.append(pre_rows)

            nrows = []
            pre_rows = []

    matrix_data = np.column_stack(ncols)
    dataset = pd.DataFrame({0: matrix_data[:, 0], 1: matrix_data[:, 1], 2: matrix_data[:, 2], 3: matrix_data[:, 3],
                            4: matrix_data[:, 4], 5: matrix_data[:, 5], 6: matrix_data[:, 6], 7: matrix_data[:, 7],
                            8: matrix_data[:, 8], 9: matrix_data[:, 9], 10: matrix_data[:, 10], 11: matrix_data[:, 11],
                            12: matrix_data[:, 12], 13: matrix_data[:, 13], 14: matrix_data[:, 14], 15: matrix_data[:, 15]})

    preview_data = np.column_stack(pre_cols)
    preview_dataset = pd.DataFrame({0: preview_data[:, 0], 1: preview_data[:, 1], 2: preview_data[:, 2], 3: preview_data[:, 3],
                                    4: preview_data[:, 4], 5: preview_data[:, 5], 6: preview_data[:, 6], 7: preview_data[:, 7],
                                    8: preview_data[:, 8], 9: preview_data[:, 9], 10: preview_data[:, 10], 11: preview_data[:, 11],
                                    12: preview_data[:, 12], 13: preview_data[:, 13], 14: preview_data[:, 14], 15: preview_data[:, 15]})

    return dataset, preview_dataset


def accdata(row, col, value='', preview=False):
    global dataset, preview_dataset
    if (value != '' and preview):
        preview_dataset.iloc[row, col] = 'O'

        return dataset.iloc[row, col], preview_dataset.iloc[row, col]

    if (preview):
        return dataset.iloc[row, col], preview_dataset.iloc[row, col]

    return dataset.iloc[row, col]


def shift_object(x=0, y=0, shiftobject=None):
    for obj in shiftobject:
        print(obj)
        if(x != 0):
            obj[0] = obj[0] + x

        if(y != 0):
            obj[1] = obj[1] + y

    return shiftobject


def draw_frame():
    # Rahmen
    for i in range(16):
        accdata(0, i, value='O', preview=True)
        print("Setting pixel:", accdata(0, i))
    for i in range(16):
        accdata(i, 0, value='O', preview=True)
        print("Setting pixel:", accdata(i, 0))
    for i in range(16):
        accdata(15, i, value='O', preview=True)
        print("Setting pixel:", accdata(15, i))
    for i in range(16):
        accdata(i, 15, value='O', preview=True)
        print("Setting pixel:", accdata(i, 15))


def getnumbers(number=None):

    zero = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0], [10, 0], [11, 0], [11, 0], [
        11, 1], [11, 2], [11, 3], [11, 4], [10, 4], [9, 4], [9, 4], [7, 4], [6, 4], [5, 4], [4, 4], [3, 4], [2, 4], [1, 4], [0, 4], [0, 3], [0, 2], [0, 1]]

    one = [[0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4],
           [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4]]

    two = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [3, 4], [4, 4], [5, 4], [6, 4], [6, 0], [
        6, 1], [6, 2], [6, 3], [6, 4], [7, 0], [8, 0], [9, 0], [10, 0], [11, 4], [11, 3], [11, 2], [11, 1], [11, 0]]

    five = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [
        6, 1], [6, 2], [6, 3], [6, 4], [7, 4], [8, 4], [9, 4], [10, 4], [11, 4], [11, 3], [11, 2], [11, 1], [11, 0]]

    six = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], [8, 0], [
        9, 0], [10, 0], [11, 0], [11, 1], [11, 2], [11, 3], [11, 4], [10, 4], [9, 4], [8, 4], [7, 4], [6, 4], [6, 3], [6, 2], [6, 1]]

    if (number == 0):
        return zero
    if (number == 1):
        return one
    if (number == 2):
        return two
    if (number == 5):
        return five
    if (number == 6):
        return six


def draw_number(number0=None, number1=None, number2=None):
    if (number1 != None and number2 != None):
        number1 = shift_object(2, 2, getnumbers(number1))
        number2 = shift_object(2, 9, getnumbers(number2))

        for pixel in number1:
            accdata(pixel[0], pixel[1], bcolors.FAIL+'O'+bcolors.ENDC, preview=True)
        for pixel2 in number2:
            accdata(pixel2[0], pixel2[1], 'O', preview=True)


def main():
    global dataset, preview_dataset
    # dataset, preview_dataset = prepare_datasets()
    prepare_datasets()

    # FULL DATASET
    # print(dataset)
    draw_frame()
    draw_number(number1=5, number2=5)

    # PRETTY PRINT DATASET
    print(tabulate(preview_dataset, headers='keys',
                   tablefmt='fancy_grid', stralign='center'))


if __name__ == "__main__":
    main()
