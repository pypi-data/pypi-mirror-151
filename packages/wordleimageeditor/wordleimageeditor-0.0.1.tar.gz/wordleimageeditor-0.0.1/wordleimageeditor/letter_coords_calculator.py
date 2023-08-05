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