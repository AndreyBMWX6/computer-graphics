import argparse
from PIL import Image
import numpy as np


def filter(input_path, output_path):
    filename = None
    if input_path.count('/') > 0:
        filename = input_path.split('/')[-1].split('.')[0]
    elif input_path.count('\\') > 0:
        filename = input_path.split('\\')[-1].split('.')[0]
    else:
        filename = input_path.split('.')[0]

    image = Image.open(input_path).convert('L')
    image.save(output_path + f"{filename}_gray.jpg")
    data = np.array(image)

    # make borders for filter
    bordered_data = data

    # append first and last row to the begin and to the end of data array
    bordered_data = np.append([data[0]], bordered_data, axis=0)
    bordered_data = np.append(bordered_data, [data[-1]], axis=0)
    # append left column
    left_column = []

    for i in range(bordered_data.shape[0]):
        left_column.append([bordered_data[i][0]])

    np_left = np.array(left_column)

    # append right column
    right_column = []

    for i in range(bordered_data.shape[0]):
        right_column.append([bordered_data[i][-1]])

    np_right = np.array(right_column)

    bordered_data = np.append(np_left, bordered_data, axis=1)
    bordered_data = np.append(bordered_data, np_right, axis=1)

    width = bordered_data.shape[1]
    height = bordered_data.shape[0]

    filtered_data = np.zeros(data.shape, dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            if x > 0 and y > 0 and x < width - 1 and y < height - 1:
                z1 = bordered_data[y - 1][x - 1]
                z2 = bordered_data[y - 1][x]
                z3 = bordered_data[y - 1][x + 1]

                z4 = bordered_data[y][x - 1]
                z5 = bordered_data[y][x]
                z6 = bordered_data[y][x + 1]

                z7 = bordered_data[y + 1][x - 1]
                z8 = bordered_data[y + 1][x]
                z9 = bordered_data[y + 1][x + 1]

                Gx = z7 + 2 * z8 + z9 - (z1 + 2 * z2 + z3)
                Gy = z3 + 2 * z6 + z9 - (z1 + 2 * z4 + z7)
                # Multiply by 255 to better show borders
                filtered_data[y - 1][x - 1] = np.sqrt(np.power(Gx, 2) + np.power(Gy, 2))

    new_image = Image.fromarray(filtered_data)
    new_image.save(output_path + f"{filename}_filtered.jpg")
    print(f"image:{input_path} is filtered")
    print(f"result in {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Sobel filter')
    parser.add_argument('--i', type=str, help='Path to unfiltered image')
    parser.add_argument('--o', type=str, help='Path for saving filtered image')

    args = parser.parse_args()
    filter(args.i, args.o)
