from PIL import Image, ImageFont, ImageDraw
from letter_coords_calculator import *


def make_image(wordle_list: list) -> Image:
    """Makes an image from wordle data

    Args:
        wordle_list (list): a list, consisting of 6 elements. Each element is also a list with this structure: [str word, int letter_state, int letter_state, int letter_state, int letter_state, int letter_state]. Letter states - 0: letter is grey, 1: letter is yellow, 2: letter is green.

    Returns:
        Image: the generated image
    """

    main_image = Image.open(r"./images/main.png")
    grey_image = Image.open(r"./images/grey.png")
    yellow_image = Image.open(r"./images/yellow.png")
    green_image = Image.open(r"./images/green.png")
    letter_images = [grey_image, yellow_image, green_image]

    drawer = ImageDraw.Draw(main_image)
    font = ImageFont.truetype("font.ttf", 60)

    text_color = (255, 255, 255)
    outline_color = (0, 0, 0)

    row = 0
    for word in wordle_list:
        if word[0] != "":
            for column in range(5):
                letter_state = word[1+column]
                main_image.paste(letter_images[letter_state], get_letter_image_coords(column, row))
                w, h = drawer.textsize(word[0][column], font=font)
                drawer.text(get_letter_font_coords(column, row, w, h), word[0][column], fill=text_color, stroke_width = 3, stroke_fill=outline_color, font=font)
        row += 1

    return main_image

