def get_center(bbox):

    x1, y1, x2, y2 = bbox

    center_x = (x1 + x2) / 2
    center_y = (y1 + y2) / 2

    return center_x, center_y


def get_position(
    bbox,
    image_width,
    image_height
):

    center_x, center_y = get_center(bbox)

    # Horizontal position
    if center_x < image_width / 3:
        horizontal = "left"

    elif center_x < (2 * image_width / 3):
        horizontal = "center"

    else:
        horizontal = "right"

    # Vertical position
    if center_y < image_height / 3:
        vertical = "top"

    elif center_y < (2 * image_height / 3):
        vertical = "middle"

    else:
        vertical = "bottom"

    return f"{vertical}-{horizontal}"