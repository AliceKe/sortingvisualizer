from os import lstat
import pygame
import random
import math
pygame.init()
pygame.mixer.init(frequency=60)

#keep all styling. instantiates a class instance
class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE
    ORANGE = 255,140,0
    GOLD = 255,215,0
    LIGHTPINK = 255,182,193
    HOTPINK = 255,105,180
    RASPBERRY = 210, 31, 60
    DESIRE = 234, 60, 83
    CARMINE = 150, 0, 24

    #SHADES OF GREYS
    GRADIENTS = [
        (128, 128, 128), 
        (160, 160, 160),
        (192, 192, 192),
    ]

    REDS = [
        (210, 31, 60),
        (234, 60, 83),
        (150, 0, 24)
    ]

    FONT = pygame.font.SysFont('Verdana', 20)
    LARGE_FONT = pygame.font.SysFont('Verdana', 30)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.block_width = round((self.width -self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD ) / (self.max_val-self.min_val))
        self.start_x = self.SIDE_PAD //2
        
def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(
        f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 
        1, draw_info.ORANGE
    )
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))

    controls = draw_info.FONT.render(
        "R = Reset | SPACE = Start Sorting | A = Ascending | D = Descending", 
        1, draw_info.BLACK
    )
    center_x = draw_info.width/2 - controls.get_width()/2
    draw_info.window.blit(controls, (center_x, 55))

    sorting = draw_info.FONT.render(
        "B = Bubble Sort | I = Insertion Sort | S = Selection Sort", 
        1, draw_info.BLACK
    )
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 85))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                    draw_info.width - draw_info.SIDE_PAD, 
                    draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        color = draw_info.REDS[i % 3]

        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))
    
    if clear_bg:
        pygame.display.update()

def generate_starting_list(n, min_val, max_val):
    lst = []

    for _ in range(n):
        val = random.randint(min_val, max_val) #inclusive
        lst.append(val)

    return lst

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GOLD, j+1: draw_info.ORANGE}, True), 
                yield True #yield makes it a generator function

    return lst

def insertion_sort(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i-1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GOLD, i: draw_info.ORANGE}, True)
            yield True

    return lst

def selection_sort(draw_info, ascending = True):
    lst = draw_info.lst

    if ascending:
        for i in range(len(lst)):
            curr_min = i
            for j in range(i+1, len(lst)):
                if lst[curr_min] > lst[j]:
                    curr_min = j
            lst[i], lst[curr_min] = lst[curr_min], lst[i]
            draw_list(draw_info, {i-1: draw_info.GOLD, i: draw_info.ORANGE}, True)
            yield True
    else:
        for i in range(len(lst)-1, 0, -1):
            curr_min = i
            for j in range(i-1, 0, -1):
                if lst[curr_min] > lst[j]:
                    curr_min = j
            lst[i], lst[curr_min] = lst[curr_min], lst[i]
            draw_list(draw_info, {i-1: draw_info.GOLD, i: draw_info.ORANGE}, True)
            yield True
    
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    n = 50
    min_val = 0
    max_val = 100
    
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    pygame.mixer.music.load("./sound/water-drop.mp3")

    while run:
        clock.tick(60) #sorting speed (incr for faster sorting visualization)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
            pygame.mixer.music.play(-1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)

            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False

            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()










        








