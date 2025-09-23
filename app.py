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

width_block = 110
height_block = 80

wall = Wall(width_screen - margin_line_left - margin_line_right, height_screen - margin_line_bottom)
hole = Hole(600, 340, 300, 400)

c = Canvas(width=width_screen, height=height_screen, bg='white')


def create_limit():
    # bottom line
    c.create_line(0, null_level, width_screen, null_level)
    # left line
    c.create_line(margin_line_left, 0, margin_line_left, height_screen)
    # right line
    c.create_line(width_screen - margin_line_right, 0, width_screen - margin_line_right, height_screen)


def create_hole(hole):
    c.create_line(hole.x, hole.y2, hole.x, hole.y)
    c.create_line(hole.x, hole.y, hole.x2, hole.y)
    c.create_line(hole.x2, hole.y2, hole.x2, hole.y)


def check_dead_zone(x):

    return x


create_limit()
create_hole(hole)

full_block = Block(0, 0, width_block, height_block, width_block, width_block)

# for i in range(0, 11, 1):
#     c.create_rectangle(margin_line_left + (i * width_block), null_level - height_block,
#                        width_block + margin_line_left + (i * width_block), null_level)

used_blocks = []
# for i in range(height_screen, 0, -height_block):
#     used_blocks.append(full_block)
#     print(i)

x = margin_line_left
width_wall = width_screen - margin_line_left - margin_line_right

while x < width_wall-width_block:
    if hole.x < x + width_block < hole.x2:
        used_blocks.append(Block(x, null_level-height_block, hole.x - x, height_block, width_block, height_block))
        #used_blocks.append(Block(x, null_level - height_block, width_block, height_block, width_block, height_block))
        x = hole.x2

    used_blocks.append(Block(x, null_level-height_block, width_block, height_block, width_block, height_block))
    x += width_block

last_block_x = used_blocks[-1].x2
right_border_screen_x = width_screen - margin_line_right
if last_block_x != right_border_screen_x:
    used_blocks.append(Block(last_block_x, null_level-height_block, right_border_screen_x - last_block_x,
                             height_block, width_block, height_block))

print(used_blocks[-1])

for block in used_blocks:
    c.create_rectangle(block.x, block.y, block.x2, block.y2)
    # Подпись для блока
    if block.width > 20 and block.height > 15:
        c.create_text(block.x + block.width / 2, block.y + block.height / 2,
                      text=f"{block.width}x{block.height}", font=("Arial", 8))

c.pack()
root.mainloop()
