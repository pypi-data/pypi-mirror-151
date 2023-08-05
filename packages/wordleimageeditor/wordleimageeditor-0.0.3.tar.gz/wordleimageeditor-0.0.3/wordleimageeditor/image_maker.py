from PIL import Image, ImageFont, ImageDraw


def get_letter_image_coords(x: int, y: int) -> tuple:
    """Get image coords of a letter in pixels

    Args:
        x (int): X position of letter
        y (int): Y position of letter

    Returns:
        tuple: Coords of the letter in pixels: top left corner first and then bottom right corner.
    """
    offset_x = 30
    offset_y = 180
    coords1_x = offset_x + x * 90
    coords1_y = offset_y + y * 90
    coords2_x = coords1_x + 80
    coords2_y = coords1_y + 80
    return (coords1_x, coords1_y, coords2_x, coords2_y)


def get_letter_font_coords(x: int, y: int, w: int, h: int) -> tuple:
    """Get text coords of a letter

    Args:
        x (int): X position of letter
        y (int): Y position of letter
        w (int): Width of a letter
        h (int): Height of a letter

    Returns:
        tuple: X and y coords of the text
    """

    offset_x = 30
    offset_y = 180
    coords1_x = offset_x + x * 90 + 40 - w/2
    coords1_y = offset_y + y * 90  + 40 - h/2
    return (coords1_x, coords1_y)


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

