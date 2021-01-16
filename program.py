import cv2
import random as r
from sys import argv


def get_image1():
    try:
        image = cv2.imread(argv[1])
        if image is None:
            raise Exception('Failed reading image!')
        return image
    except Exception as e:
        print(e)


def get_image2():
    try:
        image = cv2.imread(argv[2])
        if image is None:
            raise Exception('Failed reading image!')
        return image
    except Exception as e:
        print(e)


def get_text():
    try:
        with open(argv[2], 'r', encoding='utf-8') as fle:
            text = fle.read()
            if text is None or text == '':
                raise Exception('Failed reading text!')
            return text
    except Exception as e:
        print(e)


def dex_to_binary(dex_number):
    result = []
    while dex_number / 2 > 0:
        result.append(dex_number % 2)
        dex_number //= 2
    return result


def binary_to_dex(binary_number):
    result = 0
    grade = 0
    for i in binary_number:
        result += (2 ** grade) * i
        grade += 1
    return result + 1


def dex_to_binary_massive(dex_massive):
    result = []
    for x in dex_massive:
        binary_number = dex_to_binary(x)
        while len(binary_number) < 16:
            binary_number.append(0)
        result += binary_number
    return result


def hide_in_image(image, message):
    size = image.shape[:2]
    for i in range(size[0]):
        for j in range(size[1]):
            if len(message) != 0:
                image[i, j][r.randint(0, 2)] += message[0]
                del message[0]
            else:
                separate = False
                if not separate:
                    separate = True
                    image[i, j][0] += 1
                    image[i, j][1] += 1
                else:
                    image[i, j][r.randint(0, 2)] += r.choice([0, 0, 0, 1])
    return image


def find_in_image(image_got, image_key):
    size = image_got.shape[:2]
    try:
        if size != image_key.shape[:2]:
            raise Exception('Image sizes is not equal!')
        result = []
        for i in range(size[0]):
            for j in range(size[1]):
                blue = image_got[i, j][0] - image_key[i, j][0]
                green = image_got[i, j][1] - image_key[i, j][1]
                red = image_got[i, j][2] - image_key[i, j][2]
                if (blue + green + red) > 1:
                    return result
                elif blue or green or red:
                    result.append(1)
                else:
                    result.append(0)
    except Exception as e:
        print(e)


def get_text_from_binaries(binary_data):
    result = ''
    num_result = []

    while len(binary_data) > 16:
        tmp = []
        for _ in range(16):
            tmp.append(binary_data[0])
            del binary_data[0]
        num_result.append(binary_to_dex(tmp) - 1)
        result += chr(binary_to_dex(tmp) - 1)
    return result


def save_text_to_file(text_to_save):
    save_path = input('Enter path to save output text:\n')
    save_path.rstrip()
    with open(f'{save_path}\\recovered_text.txt', 'w+', encoding='utf-8') as save_file:
        save_file.write(text_to_save)
    print('Done!')


def save_image_to_file(image_to_save):
    save_path = input('Enter path to save output text:\n')
    save_path.rstrip()
    cv2.imwrite(f'{save_path}\\data_image.png', image_to_save)
    print('Done!')


if __name__ == '__main__':
    if input('1 - Hide text\n2 - Get text\n') == '1':
        key_image = get_image1()
        hide_text = get_text()

        dex_message = [ord(x) for x in hide_text]
        binary_massive = dex_to_binary_massive(dex_message)

        image_with_data = hide_in_image(key_image, binary_massive)

        save_image_to_file(image_with_data)
    else:
        data_image = get_image1()
        key_image = get_image2()

        binary_data = find_in_image(data_image, key_image)
        output_text = get_text_from_binaries(binary_data)

        save_text_to_file(output_text)
