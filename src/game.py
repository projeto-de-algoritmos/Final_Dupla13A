import copy
import math
import random
import sys
import colors
import pygame
import time
import merge_sort as mg, closest_pair_of_points as closest

size = (1366, 768)
spacing = 80
starting_x = abs((((size[0] - 20) // spacing) * spacing) - size[0]) / 2
starting_y = abs((((size[1] - 20) // spacing) * spacing) - size[1]) / 2
clock = pygame.time.Clock()

rad = math.pi / 180
strong_connected = False
animation_frames = {}

pygame.init()

screen = pygame.display.set_mode(size)
screen.fill(colors.BLACK)

pygame.display.set_caption("Runner")
icon = pygame.image.load('../images/game/runners.png')
menu = pygame.image.load('../images/game/menu.png')
icon_big = pygame.transform.scale(icon, (80, 80))
pygame.display.set_icon(icon)

font = pygame.font.SysFont('default', 150)
cost_font = pygame.font.SysFont('default', 30)

import auxiliary as aux


# auxiliary function for drawing text
def text_hollow(text_font, message, font_color):
    not_color = [c ^ 0xFF for c in font_color]
    base = text_font.render(message, 0, font_color, not_color)
    box_size = base.get_width() + 2, base.get_height() + 2
    img = pygame.Surface(box_size, 16)
    img.fill(not_color)
    base.set_colorkey(0)
    img.blit(base, (0, 0))
    img.blit(base, (2, 0))
    img.blit(base, (0, 2))
    img.blit(base, (2, 2))
    base.set_colorkey(0)
    base.set_palette_at(1, not_color)
    img.blit(base, (1, 1))
    img.set_colorkey(not_color)
    return img


# auxiliary function for drawing text
def text_outline(text_font, message, font_color, outline_color):
    base = text_font.render(message, 0, font_color)
    outline = text_hollow(text_font, message, outline_color)
    img = pygame.Surface(outline.get_size(), 16)
    img.blit(base, (1, 1))
    img.blit(outline, (0, 0))
    img.set_colorkey(0)
    return img


def game_win_text(player):
    win_text = text_outline(font, str(player) + " WINS!", colors.WHITE, colors.BLACK)
    screen.blit(win_text, (270, 300))


def text_objects(text, text_font):
    text_surface = text_font.render(text, True, colors.NODE)
    return text_surface, text_surface.get_rect()


# creates a button
def button(msg, x, y, w, h, ic, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, (ic[0] - 20, ic[1] - 20, ic[2] - 20), (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x, y, w, h))

    small_text = pygame.font.SysFont("default", 20)
    text_surf, text_rect = text_objects(msg, small_text)
    text_rect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(text_surf, text_rect)


def menu_game_window():
    menu_game = True

    while menu_game:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        screen.fill(colors.WHITE)
        screen.blit(menu, (0, 0))

        button('START', 590, 550, 200, 100, colors.BRIGHT_GREEN, game_loop)
        pygame.display.update()
        clock.tick(15)


def restart_game_window(player):
    restart_game = True

    while restart_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        game_win_text(player)
        button('RESTART', 510, 450, 100, 50, colors.GREEN, game_loop)
        button('QUIT', 750, 450, 100, 50, colors.RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def quit_game():
    pygame.quit()
    sys.exit()


def interface(player, player_2, deposit):
    pygame.draw.rect(screen, colors.WHITE, (588, 0, 200, 94))
    pygame.draw.rect(screen, colors.BLACK, (593, 0, 190, 89))
    pygame.draw.rect(screen, colors.WHITE, (688, 0, 5, 94))
    icon1 = pygame.image.load("../images/player1/player1_1.png")
    icon1 = pygame.transform.scale(icon1, (22, 22))
    icon1 = icon1.convert()
    icon1.set_colorkey((0, 0, 0))
    screen.blit(icon1, (600, 5))
    icon2 = pygame.image.load("../images/player2/player2_1.png")
    icon2 = pygame.transform.scale(icon2, (22, 22))
    icon2 = icon2.convert()
    icon2.set_colorkey((0, 0, 0))
    screen.blit(icon2, (700, 5))
    goal1 = text_outline(pygame.font.SysFont('default', 25),
                         'G: ' + str(deposit.player1_value) + "/" + str(deposit.goal), colors.WHITE, colors.BLACK)
    screen.blit(goal1, (608, 70))
    goal2 = text_outline(pygame.font.SysFont('default', 25),
                         'G: ' + str(deposit.player2_value) + "/" + str(deposit.goal), colors.WHITE, colors.BLACK)
    screen.blit(goal2, (705, 70))
    cargo1 = text_outline(pygame.font.SysFont('default', 25),
                          'L: ' + str(player.current_load) + "/" + str(player.max_load), colors.WHITE, colors.BLACK)
    screen.blit(cargo1, (613, 40))
    cargo2 = text_outline(pygame.font.SysFont('default', 25),
                          'L: ' + str(player_2.current_load) + "/" + str(player_2.max_load), colors.WHITE, colors.BLACK)
    screen.blit(cargo2, (708, 40))
    points1 = text_outline(pygame.font.SysFont('default', 25),
                           'P: ' + str(player.value), colors.WHITE, colors.BLACK)
    screen.blit(points1, (635, 8))
    points2 = text_outline(pygame.font.SysFont('default', 25),
                           'P: ' + str(player_2.value), colors.WHITE, colors.BLACK)
    screen.blit(points2, (735, 8))


def update(graph, player, player_2, deposit):
    screen.fill(colors.BLACK)
    draw_walls(graph)
    player.rect[0] += player.movement[0]
    player.rect[0] -= player.movement[1]
    player.rect[1] += player.movement[2]
    player.rect[1] -= player.movement[3]
    player_2.rect[0] += player_2.movement[0]
    player_2.rect[0] -= player_2.movement[1]
    player_2.rect[1] += player_2.movement[2]
    player_2.rect[1] -= player_2.movement[3]
    image = pygame.transform.rotate(player.image, player.angle)
    screen.blit(image, (player.rect[0], player.rect[1]))
    image2 = pygame.transform.rotate(player_2.image, player_2.angle)
    screen.blit(image2, (player_2.rect[0], player_2.rect[1]))
    interface(player, player_2, deposit)
    draw_circle(deposit, colors.EXIT)
    for item in graph.itens:
        if time.perf_counter() - item.time_of_creation > random.uniform(10.0, 12.0):
            graph.itens.remove(item)
            graph.item_positions.pop((item.rect[0], item.rect[1]))
            continue
        screen.blit(item.item_image, item)


# stores nodes and positions
class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.positions = dict()
        self.item_positions = dict()
        self.itens = []

    def add_nodes(self, node, pos):
        self.nodes.add(node)
        self.positions[pos] = node


class Node(object):
    def __init__(self):
        self.rect = None
        self.neighbours = set()
        # used to ensure graph is strongly connected
        self.strong = False


class Player(object):
    def __init__(self):
        self.image = None
        self.items = []
        self.max_load = 30
        self.current_load = 0
        self.value = 0
        self.angle = 0
        self.position = random_pos()
        self.movement = [0, 0, 0, 0]
        self.rect = pygame.Rect(self.position[0], self.position[1], 20, 20)


class Deposit(object):
    def __init__(self):
        self.color = colors.EXIT
        self.position = random_pos()
        self.player1_value = 0
        self.player2_value = 0
        self.goal = 100


class Item(object):
    def __init__(self):
        self.rect = pygame.Rect(0, 0, 20, 20)
        self.time_of_creation = time.perf_counter()
        self.item_image = None
        self.weight = 0
        self.value = 0
        item = {
            "apple": aux.apple,
            "banana": aux.banana,
            "cherry": aux.cherry,
            "key": aux.key,
            "orange": aux.orange,
            "pear": aux.pear,
            "strawberry": aux.strawberry
        }
        itens = ["apple", "banana", "cherry", "key", "orange", "pear", "strawberry"]
        chances = [0.1, 0.25, 0.1, 0.2, 0.25, 0.25, 0.2]
        item[random.choices(itens, chances)[0]](self)


# shortest path function
def dijkstra(graph, start, goal):
    unseen_nodes = dict.fromkeys(graph.nodes, 0)
    shortest_distance = {}
    predecessor = {}
    path = []
    infinity = 9999999

    for node in unseen_nodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseen_nodes:
        min_node = None
        for node in unseen_nodes:
            if min_node is None:
                min_node = node
            elif shortest_distance[node] < shortest_distance[min_node]:
                min_node = node

        for neighbour, weight in min_node.neighbours.items():
            if weight + shortest_distance[min_node] < shortest_distance[neighbour]:
                shortest_distance[neighbour] = weight + shortest_distance[min_node]
                predecessor[neighbour] = min_node
        unseen_nodes.pop(min_node)

    current_node = goal
    while current_node != start:
        path.insert(0, current_node)
        current_node = predecessor[current_node]

    return path, shortest_distance[goal]


# generates graph with random edges
def create_graph():
    pos = [starting_x, starting_y]
    graph = Graph()
    nodes = []
    while pos[1] <= size[1] - starting_y:
        node = Node()
        graph.add_nodes(node, (pos[0], pos[1]))
        nodes.append(node)
        node.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        if pos[0] == size[0] - starting_x:
            pos[0] = starting_x
            pos[1] += spacing
            continue
        pos[0] += spacing

    pos = [starting_x, starting_y]
    for node in nodes:
        if pos[1] > size[1] - starting_y:
            break
        if pos[0] > size[0] - starting_x:
            pos[0] = starting_x
            pos[1] += spacing

        if pos[0] - spacing > 0:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0] - spacing, pos[1]]
                node.neighbours.add(neighbour)
                neighbour.neighbours.add(node)
        if pos[0] + spacing < size[0]:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0] + spacing, pos[1]]
                node.neighbours.add(neighbour)
                neighbour.neighbours.add(node)
        if pos[1] - spacing > 0:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0], pos[1] - spacing]
                node.neighbours.add(neighbour)
                neighbour.neighbours.add(node)
        if pos[1] + spacing < size[1]:
            if random.randint(0, 1):
                neighbour = graph.positions[pos[0], pos[1] + spacing]
                node.neighbours.add(neighbour)
                neighbour.neighbours.add(node)

        pos[0] += spacing

    return graph


# main function to ensure strong connectivity
def strongly_connect(graph, rev_graph, start_pos):
    global strong_connected

    bfs(graph.positions[start_pos])
    bfs(rev_graph.positions[start_pos])

    update_strong_component(graph, rev_graph)

    for node in graph.nodes:
        if not node.strong:
            strong_connected = False
            break
        strong_connected = True

    if strong_connected:
        return

    fix_connectivity(graph, rev_graph)

    for node in graph.nodes:
        node.strong = False
        rev_graph.positions[node.rect[0], node.rect[1]].strong = False

    strongly_connect(graph, rev_graph, start_pos)


# reverse all edges of given graph
def reverse_graph(graph):
    rev_graph = copy.deepcopy(graph)
    for node in rev_graph.nodes:
        node.neighbours.clear()
    for node in graph.nodes:
        for neighbour in node.neighbours:
            rev_graph.positions[neighbour.rect[0], neighbour.rect[1]].neighbours.add(rev_graph.positions[node.rect[0],
                                                                                                         node.rect[1]])
    return rev_graph


# update nodes marked as strongly connected
def update_strong_component(graph, rev_graph):
    for node in graph.nodes:
        if node.strong and rev_graph.positions[node.rect[0], node.rect[1]].strong:
            continue
        else:
            node.strong = False


# fixes connectivity by generating edges between strongly connected component and other nodes
def fix_connectivity(graph, rev_graph):
    for node in graph.nodes:
        if not node.strong:
            if node.rect[0] - spacing > 0:
                if graph.positions[node.rect[0] - spacing, node.rect[1]].strong:
                    node.neighbours.add(graph.positions[node.rect[0] - spacing, node.rect[1]])
                    graph.positions[node.rect[0] - spacing, node.rect[1]].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0] - spacing, node.rect[1]])
                    rev_graph.positions[node.rect[0] - spacing, node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return
            if node.rect[0] + spacing < size[0]:
                if graph.positions[node.rect[0] + spacing, node.rect[1]].strong:
                    node.neighbours.add(graph.positions[node.rect[0] + spacing, node.rect[1]])
                    graph.positions[node.rect[0] + spacing, node.rect[1]].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0] + spacing, node.rect[1]])
                    rev_graph.positions[node.rect[0] + spacing, node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return
            if node.rect[1] - spacing > 0:
                if graph.positions[node.rect[0], node.rect[1] - spacing].strong:
                    node.neighbours.add(graph.positions[node.rect[0], node.rect[1] - spacing])
                    graph.positions[node.rect[0], node.rect[1] - spacing].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1] - spacing])
                    rev_graph.positions[node.rect[0], node.rect[1] - spacing].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return
            if node.rect[1] + spacing < size[1]:
                if graph.positions[node.rect[0], node.rect[1] + spacing].strong:
                    node.neighbours.add(graph.positions[node.rect[0], node.rect[1] + spacing])
                    graph.positions[node.rect[0], node.rect[1] + spacing].neighbours.add(node)
                    rev_graph.positions[node.rect[0], node.rect[1]].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1] + spacing])
                    rev_graph.positions[node.rect[0], node.rect[1] + spacing].neighbours.add(
                        rev_graph.positions[node.rect[0], node.rect[1]])
                    return


def bfs(node):
    node.strong = True
    queue = [node]

    while queue:
        s = queue.pop(0)

        for neighbour in s.neighbours:
            if not neighbour.strong:
                neighbour.strong = True
                queue.append(neighbour)


def draw_walls(graph):
    for node in graph.nodes:
        left_neighbour = 0
        right_neighbour = 0
        top_neighbour = 0
        bottom_neighbour = 0
        for neighbour in node.neighbours:
            if node.rect[0] > neighbour.rect[0]:
                pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] - 20, node.rect.center[1] + 15, -45, 5))
                pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] - 20, node.rect.center[1] - 20, -45, 5))
                left_neighbour += 1
            elif node.rect[0] < neighbour.rect[0]:
                right_neighbour += 1
            elif node.rect[1] < neighbour.rect[1]:
                pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] + 14, node.rect.center[1] + 20, 5, 45))
                pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] - 20, node.rect.center[1] + 15, 5, 50))
                bottom_neighbour += 1
            elif node.rect[1] > neighbour.rect[1]:
                top_neighbour += 1

        if left_neighbour == 0:
            pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] - 20, node.rect.center[1] - 20, 5, 40))
        if right_neighbour == 0:
            pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] + 14, node.rect.center[1] - 20, 5, 40))
        if top_neighbour == 0:
            pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] - 20, node.rect.center[1] - 20, 39, 5))
        if bottom_neighbour == 0:
            pygame.draw.rect(screen, colors.WHITE, (node.rect.center[0] - 20, node.rect.center[1] + 15, 39, 5))


# returns random position
def random_pos():
    random_x = 590
    random_y = 80
    while 588 < random_x < 788 and random_y < 94:
        random_x = random.randrange(starting_x, (((size[0] - 20) // spacing) * spacing), spacing)
        random_y = random.randrange(starting_y, (((size[1] - 20) // spacing) * spacing), spacing)
    return random_x, random_y


def draw_circle(node, color):
    return pygame.draw.circle(screen, color, (node.position[0] + 5, node.position[1] + 5), 10)


# ensures minimum distance between starting nodes
def min_dist(graph, player, player2, deposit):
    player_distance = dijkstra(graph, graph.positions[player.position], graph.positions[deposit.position])
    while player_distance[1] < 20:
        player.position = random_pos()
        player_distance = dijkstra(graph, graph.positions[player.position], graph.positions[deposit.position])

    player2_distance = dijkstra(graph, graph.positions[player2.position], graph.positions[deposit.position])
    while player2_distance[1] < 20:
        player2.position = random_pos()
        player2_distance = dijkstra(graph, graph.positions[player2.position], graph.positions[deposit.position])


def closest_multiple(n, x, offset):
    return (round((n - offset) / x) * x) + offset


def player_movement_control(player, graph):
    vertical_move = False
    horizontal_move = False
    target = 80
    x_offset = 43
    y_offset = 24

    closest_x = closest_multiple(player.rect.center[0], target, x_offset)
    closest_y = closest_multiple(player.rect.center[1], target, y_offset)

    if abs(player.rect.center[0] - closest_x - 5) > abs(player.rect.center[1] - closest_y - 5):
        horizontal_move = True
        vertical_move = False
    elif abs(player.rect.center[0] - closest_x) < abs(player.rect.center[1] - closest_y):
        horizontal_move = False
        vertical_move = True

    # down
    if (closest_x, closest_y + spacing) in graph.positions:
        if graph.positions[closest_x, closest_y + spacing] not in graph.positions[closest_x, closest_y].neighbours:
            if player.rect.center[1] > closest_y + 8:
                player.rect.center = (player.rect.center[0], closest_y + 8)
    elif player.rect.center[1] > closest_y + 8:
        player.rect.center = (player.rect.center[0], closest_y + 8)

    # up
    if (closest_x, closest_y - spacing) in graph.positions:
        if graph.positions[closest_x, closest_y - spacing] not in graph.positions[closest_x, closest_y].neighbours:
            if player.rect.center[1] < closest_y:
                player.rect.center = (player.rect.center[0], closest_y)
    elif player.rect.center[1] < closest_y:
        player.rect.center = (player.rect.center[0], closest_y)

    # left
    if (closest_x - spacing, closest_y) in graph.positions:
        if graph.positions[closest_x - spacing, closest_y] not in graph.positions[closest_x, closest_y].neighbours:
            if player.rect.center[0] < closest_x:
                player.rect.center = (closest_x, player.rect.center[1])
    elif player.rect.center[0] < closest_x:
        player.rect.center = (closest_x, player.rect.center[1])

    # right
    if (closest_x + spacing, closest_y) in graph.positions:
        if graph.positions[closest_x + spacing, closest_y] not in graph.positions[closest_x, closest_y].neighbours:
            if player.rect.center[0] > closest_x + 8:
                player.rect.center = (closest_x + 8, player.rect.center[1])
    elif player.rect.center[0] > closest_x + 8:
        player.rect.center = (closest_x + 8, player.rect.center[1])

    if horizontal_move:
        if player.rect.center[1] > closest_y + 8:
            player.rect.center = (player.rect.center[0], closest_y + 8)
        elif player.rect.center[1] < closest_y:
            player.rect.center = (player.rect.center[0], closest_y)
    elif vertical_move:
        if player.rect.center[0] < closest_x:
            player.rect.center = (closest_x, player.rect.center[1])
        elif player.rect.center[0] > closest_x + 8:
            player.rect.center = (closest_x + 8, player.rect.center[1])


def load_animations(path, frame_duration):
    global animation_frames
    animation_name = path.split("/")[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_duration:
        animation_frame_id = animation_name + "_" + str(n)
        img_location = path + "/" + animation_frame_id + ".png"
        animation_image = pygame.image.load(img_location)
        animation_image = pygame.transform.scale(animation_image, (22, 22))
        animation_image = animation_image.convert()
        animation_image.set_colorkey((0, 0, 0))
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1

    return animation_frame_data


animation_database = {
    "player1": load_animations("../images/player1", [10, 10, 10]),
    "player2": load_animations("../images/player2", [10, 10, 10]),
}


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame


def img_flip(player):
    if player.movement[0] == 2:
        player.angle = 0
    if player.movement[1] == 2:
        player.angle = 180
    if player.movement[2] == 2:
        player.angle = 270
    if player.movement[3] == 2:
        player.angle = 90


def dist(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def get_x_coordinates(graph, player, player2):
    temp = []
    for item in graph.itens:
        temp.append((item.rect[0], item.rect[1]))
    temp.append((player.rect[0], player.rect[1]))
    temp.append((player2.rect[0], player2.rect[1]))
    return temp


def knapsack(w, wt, val, n):
    k = [[0 for x in range(w + 1)] for x in range(n + 1)]

    for i in range(n + 1):
        for w in range(w + 1):
            if i == 0 or w == 0:
                k[i][w] = 0
            elif wt[i - 1] <= w:
                k[i][w] = max(val[i - 1] + k[i - 1][w - wt[i - 1]], k[i - 1][w])
            else:
                k[i][w] = k[i - 1][w]

    result = []
    for i in range(n, 0, -1):
        if k[i-1][w] == k[i][w]:
            continue
        else:
            result.append([wt[i-1], val[i-1]])
            w -= wt[i-1]

    return result


# detects collision using closest pair algorithm
def collision(graph, ordered_array, player, player_2):
    if graph.itens:
        pair = closest.closest_pair(ordered_array)
        p1 = pair[0]
        p2 = pair[1]
        if p1 and math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) < 15:
            if p1 == (player.rect[0], player.rect[1]) or p2 == (player.rect[0], player.rect[1]):
                for item in graph.itens:
                    if (item.rect[0], item.rect[1]) == p1 or (item.rect[0], item.rect[1]) == p2:
                        wt = []
                        vl = []
                        for element in player.items:
                            wt.append(element[0])
                            vl.append(element[1])
                        wt.append(item.weight)
                        vl.append(item.value)
                        player.current_load = 0
                        player.value = 0
                        player.items = knapsack(player.max_load, wt, vl, len(wt))
                        for element in player.items:
                            player.current_load += element[0]
                            player.value += element[1]
                        graph.itens.remove(item)
                        graph.item_positions.pop((item.rect[0], item.rect[1]))
                        break
            elif p1 == (player_2.rect[0], player_2.rect[1]) or p2 == (player_2.rect[0], player_2.rect[1]):
                for item in graph.itens:
                    if (item.rect[0], item.rect[1]) == p1 or (item.rect[0], item.rect[1]) == p2:
                        wt = []
                        vl = []
                        for element in player_2.items:
                            wt.append(element[0])
                            vl.append(element[1])
                        wt.append(item.weight)
                        vl.append(item.value)
                        player_2.current_load = 0
                        player_2.value = 0
                        player_2.items = knapsack(player_2.max_load, wt, vl, len(wt))
                        for element in player_2.items:
                            player_2.current_load += element[0]
                            player_2.value += element[1]
                        graph.itens.remove(item)
                        graph.item_positions.pop((item.rect[0], item.rect[1]))
                        break
            else:
                for item in graph.itens:
                    if (item.rect[0], item.rect[1]) == p1:
                        graph.itens.remove(item)
                        graph.item_positions.pop((item.rect[0], item.rect[1]))
                        break


# main game loop where player input is read
def game_loop():
    global animation_frames
    player1_frame = 0
    player2_frame = 0
    graph = create_graph()
    player_1 = Player()
    player_2 = Player()
    player_1.color = colors.PLAYER
    player_2.color = colors.PLAYER2
    deposit = Deposit()
    deposit.position = random_pos()
    elapsed = time.perf_counter()

    rev_graph = reverse_graph(graph)
    strongly_connect(graph, rev_graph, player_1.position)

    for node in graph.nodes:
        node.neighbours = dict.fromkeys(node.neighbours, random.randint(1, 3))

    draw_walls(graph)

    min_dist(graph, player_1, player_2, deposit)

    while True:

        if time.perf_counter() - elapsed > random.uniform(2.0, 3.0):
            x, y = random_pos()

            x = x - 5
            y = y - 5
            while (x, y) in graph.item_positions:
                x, y = random_pos()
            item = Item()
            item.rect[0] = x
            item.rect[1] = y
            graph.itens.append(item)
            graph.item_positions[x, y] = item
            elapsed = time.perf_counter()

        ordered_array = mg.merge_sort(get_x_coordinates(graph, player_1, player_2))
        collision(graph, ordered_array, player_1, player_2)

        img_flip(player_1)
        img_flip(player_2)

        player1_frame += 1
        if player1_frame >= len(animation_database["player1"]):
            player1_frame = 0
        player_img_id = animation_database["player1"][player1_frame]
        player_1.image = animation_frames[player_img_id]

        player2_frame += 1
        if player2_frame >= len(animation_database["player2"]):
            player2_frame = 0
        player_img_id = animation_database["player2"][player2_frame]
        player_2.image = animation_frames[player_img_id]

        update(graph, player_1, player_2, deposit)

        player_movement_control(player_1, graph)
        player_movement_control(player_2, graph)

        if dist(player_1.rect.center, player_2.rect.center) < 15:
            if player_1.value > player_2.value:
                restart_game_window("PLAYER 1")
            elif player_2.value > player_1.value:
                restart_game_window("PLAYER 2")
        if dist(player_1.rect.center, (deposit.position[0], deposit.position[1])) < 15:
            deposit.player1_value += player_1.value
            player_1.items.clear()
            player_1.value = 0
            player_1.current_load = 0
        if dist(player_2.rect.center, (deposit.position[0], deposit.position[1])) < 15:
            deposit.player2_value += player_2.value
            player_2.items.clear()
            player_2.value = 0
            player_2.current_load = 0
        if deposit.player1_value >= 100:
            restart_game_window("PLAYER 1")
        if deposit.player2_value >= 100:
            restart_game_window("PLAYER 2")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_1.movement[2] = 2
                if event.key == pygame.K_UP:
                    player_1.movement[3] = 2
                if event.key == pygame.K_LEFT:
                    player_1.movement[1] = 2
                if event.key == pygame.K_RIGHT:
                    player_1.movement[0] = 2
                if event.key == pygame.K_s:
                    player_2.movement[2] = 2
                if event.key == pygame.K_w:
                    player_2.movement[3] = 2
                if event.key == pygame.K_a:
                    player_2.movement[1] = 2
                if event.key == pygame.K_d:
                    player_2.movement[0] = 2
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_1.movement[2] = 0
                if event.key == pygame.K_UP:
                    player_1.movement[3] = 0
                if event.key == pygame.K_LEFT:
                    player_1.movement[1] = 0
                if event.key == pygame.K_RIGHT:
                    player_1.movement[0] = 0
                if event.key == pygame.K_s:
                    player_2.movement[2] = 0
                if event.key == pygame.K_w:
                    player_2.movement[3] = 0
                if event.key == pygame.K_a:
                    player_2.movement[1] = 0
                if event.key == pygame.K_d:
                    player_2.movement[0] = 0

        pygame.display.update()
        clock.tick(60)


def main():
    menu_game_window()
    game_loop()


if __name__ == "__main__":
    main()
