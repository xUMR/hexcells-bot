from pyautogui import *
from time import sleep
import sys

# tested on windowed 1280x720

w, h = size()
cell_offset = None
cell_offset_small = (36.75, 20.8)
cell_offset_big = (55, 31)  # for the first 12 levels
cell_color = (255, 175, 41)  # FFAF29
color_white = (255, 255, 255)
img_cell = "hexcells-cell"
img_rema = None
img_rema_small = "hexcells-rema-small"
img_rema_big = "hexcells-rema-big"  # for the first 12 levels
sleep_duration_menu = 2
sleep_duration_level = 3
menu_pos = None
retry_pos = None
restart_pos = None
next_level_pos = None
end_game_pos = None
unlimited_pos_1 = None
unlimited_pos_2 = None
is_unlimited = False
init_complete = False


def img(filename):
    return "img/{}.png".format(filename)


def add_pos(v1, x=0, y=0):
    return (v1[0] + x, v1[1] + y)


def init():
    global img_cell, img_rema
    global menu_pos, retry_pos, restart_pos, next_level_pos, end_game_pos
    global unlimited_pos_1, unlimited_pos_2, init_complete

    if not init_complete:
        img_cell = img(img_cell)

    menu_pos = add_pos(find_rema(), -1109)
    retry_pos = add_pos(menu_pos, 315, 560)
    restart_pos = add_pos(menu_pos, 550, 335)
    next_level_pos = add_pos(menu_pos, 780, 565)
    end_game_pos = add_pos(menu_pos, 560, 565)
    unlimited_pos_1 = add_pos(menu_pos, 400, 185)  # random seed
    unlimited_pos_2 = add_pos(menu_pos, 555, 585)  # infinity
    init_complete = True


def alternator():
    """Yields 1, -1, 2, -2, 3, -3, 4, -4, 5, -5..."""
    i = 0
    while True:
        i += 1
        yield i
        yield -i


def in_x_range(x):
    return x > 0 and x < w


def next_x(start_x, nums):
    x = round(start_x + next(nums) * cell_offset[0])
    # prevents cells being ignored
    # in case the first cell is too far left or right
    if in_x_range(x):
        return x
    else:
        x_ = round(start_x + next(nums) * cell_offset[0])
        return x_ if in_x_range(x_) else x


def search_horizontal(start, width, image, cells=set()):
    x, y = [round(i) for i in start]
    nums = alternator()
    while in_x_range(x):
        xy = (x, y)
        if image.getpixel(xy) == cell_color:
            cells.add(xy)
        x = next_x(start[0], nums)


def find_cells():
    image = screenshot()
    image_pos = locate(img_cell, image)
    if image_pos is None:
        print("No cells found, terminating...")
        exit()

    x, y = center(image_pos)
    if cell_offset == cell_offset_big:
        y += 10
    cells = set()
    while y < h:
        search_horizontal((x, y), w, image, cells)
        y += cell_offset[1]
    return cells


def find_info_cells(cells):
    image = screenshot()
    info_cells = set()
    for cell in cells:
        pixelMatchesColor
        if image.getpixel((cell)) == cell_color:
            info_cells.add(cell)
    return info_cells


def hover_menu():
    moveTo(menu_pos)
    sleep(.75)  # wait for the hovered cell's color to change


def menu():
    hover_menu()
    click()
    sleep(sleep_duration_menu)


def menu_end_game():
    click(end_game_pos)
    sleep(sleep_duration_menu)


def restart():
    menu()
    click(restart_pos)
    sleep(sleep_duration_menu)


def retry():
    sleep(sleep_duration_menu)
    click(retry_pos)
    sleep(sleep_duration_level)


def next_level_available():
    return pixelMatchesColor(next_level_pos[0], next_level_pos[1], color_white)


def next_level(end_game=True):
    print("Proceeding to the next level in...")
    countdown(sleep_duration_level)
    print("")

    if is_unlimited:
        if end_game:
            menu_end_game()
        click(unlimited_pos_1)
        click(unlimited_pos_2)
    else:
        click(next_level_pos)
    sleep(sleep_duration_level)


def click_cells(cells, info_cells):
    # left click "mine" cells
    # right click "info" cells
    for cell in cells:
        button = 'right' if cell in info_cells else 'left'
        click(cell, button=button)


def solve():
    # in case the window is moved or a different cell-sized level is entered
    init()

    # move the cursor away
    hover_menu()

    # store coordinates of all cells in a set (all cells)
    print("Searching for cells...")
    cells = find_cells()
    print("Found {}.".format(len(cells)))

    # click each of them once
    for cell in cells:
        click(cell)

    # move the cursor away
    hover_menu()

    # store the remaining orange cells' ("info" cells) coordinates
    print("Searching for info cells...")
    info_cells = find_info_cells(cells)
    print("Found {}.".format(len(info_cells)))

    # cell data is available, restart
    restart()

    click_cells(cells, info_cells)

    sleep(sleep_duration_menu)
    return (cells, info_cells)


def countdown(n):
    for i in range(n, 0, -1):
        print("\r{}        ".format(i), end="")
        sleep(1)
    print("\rWaited {} seconds.".format(n))


def unlimited_mode():
    global is_unlimited
    is_unlimited = True
    while True:
        solve()
        next_level()


def unlimited_fast():
    global is_unlimited
    is_unlimited = True
    cells, info_cells = solve()
    while True:
        retry()
        print("Solving again...")
        click_cells(cells, info_cells)


def regular_mode():
    while True:
        solve()
        if not next_level_available():
            menu_end_game()
            print("Select next level and press Enter key to continue...")
            input()
            continue

        next_level()


def find_rema():
    """Return center of img_rema"""
    global cell_offset, img_rema

    ss = screenshot()
    location = locate(img(img_rema_big), ss)
    if location is not None:
        img_rema = img_rema_big
        cell_offset = cell_offset_big
        return center(location)

    location = locate(img(img_rema_small), ss)
    if location is not None:
        img_rema = img_rema_small
        cell_offset = cell_offset_small
        return center(location)

    else:
        print("Make sure the game window isn't obscured "
              "and the fade-in animation is complete.")
        exit()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "-u":
            unlimited_mode()
        elif sys.argv[1] == "-f":
            unlimited_fast()
        else:
            regular_mode()
    else:
        regular_mode()


if __name__ == '__main__':
    main()
