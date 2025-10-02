from tkinter import *
from Class.Class import Block, Wall, Hole

root = Tk()
root.title("Оптимизация каменной кладки")
root.geometry("1500x800")

width_screen = 1400
height_screen = 750
margin_line_bottom = 10
margin_line_left = 10
margin_line_right = 10
null_level = height_screen - margin_line_bottom

width_block = 150
height_block = 80

wall = Wall(width_screen - margin_line_left - margin_line_right, height_screen - margin_line_bottom)
hole = Hole(600, 290, 300, 450)

c = Canvas(width=width_screen, height=height_screen, bg='white')


def create_limit():
    # bottom line
    c.create_line(0, null_level, width_screen, null_level)
    # left line
    c.create_line(margin_line_left, 0, margin_line_left, height_screen)
    # right line
    c.create_line(width_screen - margin_line_right, 0, width_screen - margin_line_right, height_screen)


def create_hole(hole_for_create):
    c.create_line(hole_for_create.x, hole_for_create.y2, hole_for_create.x, hole_for_create.y)
    c.create_line(hole_for_create.x, hole_for_create.y, hole_for_create.x2, hole_for_create.y)
    c.create_line(hole_for_create.x2, hole_for_create.y2, hole_for_create.x2, hole_for_create.y)



def get_width_block_with_check_overflowing(check_previous_row_blocks, current_x):
    for check_block in check_previous_row_blocks:
        current_overflowing = check_block.x - (current_x + width_block)
        if abs(current_overflowing) < min_overflowing:
            if current_overflowing >= 0:
                return width_block - (min_overflowing - abs(current_overflowing))
            else:
                return width_block - abs(current_overflowing) - min_overflowing
    return width_block

create_limit()
create_hole(hole)

full_block = Block(0, 0, width_block, height_block, width_block, width_block)

used_blocks = []

x = margin_line_left
width_wall = width_screen - margin_line_left - margin_line_right

min_overflowing = 50 # минимальное значение перевязки швов
start_overflowing = min_overflowing # стартовая перевязка швов (с края отступаем на 30)
previous_row_blocks = [] # блоки предыдущего ряда

j = 1 # задаем начальный ряд блоков
while j < 10: # пока не закончатся все ряды

    if j != 1: # если не первый ряд
        previous_row_blocks = []
        last_block_y = used_blocks[-1].y
        for block in used_blocks:
            if block.y == last_block_y:
                previous_row_blocks.append(block)

        start_previous_block = previous_row_blocks[0]
        if start_previous_block.x2 == x + width_block:
            used_blocks.append(Block(x, null_level-(height_block * j), width_block - start_overflowing, height_block, width_block, height_block))
            x = used_blocks[-1].x2

    while x < width_wall-width_block:
        bottom_block = null_level-(height_block * (j - 1))
        if hole.x < x + width_block < hole.x2 and hole.y < bottom_block: # если блок не попадает на проем и низ блока ниже верха проема
            used_blocks.append(
                Block(x, null_level - (height_block * j), hole.x - x, height_block, width_block, height_block))
            if bottom_block - hole.y < height_block:
                x = x + hole.x - x
            else:
                x = hole.x2

            if bottom_block - hole.y < height_block and hole.x <= x <= hole.x2:
                while x < hole.x2 - width_block:
                    used_blocks.append(Block(x, null_level - (height_block * j), width_block, height_block - (bottom_block - hole.y), width_block, height_block))
                    x += width_block
                last_block_x = used_blocks[-1].x2
                if last_block_x != hole.x2:
                    used_blocks.append(
                        Block(last_block_x, null_level - (height_block * j), hole.x2 - last_block_x,
                              height_block - (bottom_block - hole.y), width_block, height_block))
                    x = hole.x2

        if j != 1 and x == hole.x2:
            for block in previous_row_blocks:
                if block.x == x:
                    start_previous_block = block
                    if start_previous_block.x2 == x + width_block:  # если блок не равен по длине находящемуся под ним
                        used_blocks.append(
                            Block(x, null_level - (height_block * j), width_block - start_overflowing,
                                  height_block,
                                  width_block, height_block))
                        x = used_blocks[-1].x2

        used_blocks.append(Block(x, null_level-(height_block * j), get_width_block_with_check_overflowing(previous_row_blocks, x), height_block, width_block, height_block))
        x += get_width_block_with_check_overflowing(previous_row_blocks, x)

    last_block_x = used_blocks[-1].x2
    right_border_screen_x = width_screen - margin_line_right
    if last_block_x != right_border_screen_x:
        used_blocks.append(Block(last_block_x, null_level-(height_block * j), right_border_screen_x - last_block_x,
                                 height_block, width_block, height_block))
        j += 1
        x = margin_line_left

print(used_blocks[-1])

#k = 0
for block in used_blocks:
    c.create_rectangle(block.x, block.y, block.x2, block.y2)
    # Подпись для блока
    if block.width > 15 and block.height > 15:
        c.create_text(block.x + block.width / 2, block.y + block.height / 2,
                      text=f"{block.width}x{block.height}", font=("Arial", 7))
        # c.create_text(block.x + block.width / 2, block.y + block.height / 2,
        #               text=f"№{k} {block.width}x{block.height}", font=("Arial", 7))
    # k += 1

c.pack()
root.mainloop()
