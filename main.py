# Necessary Package Imports: PIL, numpy, matplotlib
from PIL import Image
import numpy as np


def image_to_mat(filename):
    """
    A Helper function that takes an image filename, parses the image, and converts it to an array
    """
    img = Image.open(filename)
    return np.asarray(img)


def binarize(text: str):
    """
    Takes an ascii string, and converts each character to the 8-bit binary of its corresponding ascii value

    This is a Helper Function used in the function hide()
    """
    binary_str = ""
    for letter in text:
        binary = bin(ord(letter))[2:].zfill(8)
        binary_str += binary

    return binary_str


def mat_to_image(mat, filename):
    """Helper Function: Given a matrix, it converts it to the corresponding image, and saves it"""
    img = Image.fromarray(mat)
    img.save(f"output_{filename}")


def hide(img_arr, text_to_hide: str):
    """
    The Text Hiding Function
    Takes an image matrix, and the text to hide
    Hides the text in the image
    Returns the new image matrix
    """
    binary_text = binarize(text_to_hide)

    n_rows, n_cols, n_channels = img_arr.shape

    new_img_arr = np.copy(img_arr)

    index = 0

    for row in range(n_rows):
        for col in range(n_cols):
            for channel in range(n_channels):
                ip_pixel = img_arr[row, col, channel]
                ip_pixel_bin = bin(ip_pixel)
                op_lsb = binary_text[index]
                op_pixel_bin = ip_pixel_bin[:-1] + op_lsb
                op_pixel = int(op_pixel_bin, 2)
                new_img_arr[row, col, channel] = op_pixel
                index += 1
                if index == len(binary_text):
                    return new_img_arr

    return None


def stringify(bin_text: str):
    """
    Takes binary stream of data, where each byte represents a character in the ASCII representation,
    and converts it to the corresponding ascii string

    This is a Helper Function used in the function unhide()
    """
    text = ""
    i = 0

    while i < len(bin_text):
        bin_word = bin_text[i:i + 8]
        word = chr(int(bin_word, 2))
        text += word
        i += 8

    return text


def unhide(img_arr, length: int):
    """
    Takes the image array, and tries to retrieve the hidden text of length "length"
    """
    n_rows, n_cols, n_channels = img_arr.shape

    binary_text = ""
    length = length * 8

    for row in range(n_rows):
        for col in range(n_cols):
            for channel in range(n_channels):
                ip_pixel = img_arr[row, col, channel]
                ip_pixel_bin = bin(ip_pixel)
                ip_lsb = ip_pixel_bin[-1]
                binary_text += ip_lsb
                length -= 1

                if length == 0:
                    return stringify(binary_text)
    return ""


def main():
    ip_text = input("Text to hide: ")
    img_arr = image_to_mat(filename='souradip.png')
    op_img_arr = hide(img_arr=img_arr, text_to_hide=ip_text)
    mat_to_image(op_img_arr, 'souradip.png')

    new_img_arr = image_to_mat(filename='output_souradip.png')
    text = unhide(new_img_arr, len(ip_text))
    print(f"The Hidden Text is: {text}")


if __name__ == "__main__":
    main()
