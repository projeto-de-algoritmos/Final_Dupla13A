import copy
import math
import random
import sys
import colors
import pygame

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
screen.fill(colors.WHITE)

pygame.display.set_caption("Runner")
icon = pygame.image.load('src/images/runners.png')
menu = pygame.image.load('src/images/menu.png')
icon_big = pygame.transform.scale(icon, (80, 80))
pygame.display.set_icon(icon)

font = pygame.font.SysFont('default', 150)
cost_font = pygame.font.SysFont('default', 30)


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


def game_win_text():
    win_text = text_outline(font, 'YOU WIN!', colors.WHITE, colors.BLACK)
    screen.blit(win_text, (430, 300))


def game_lose_text():
    win_text = text_outline(font, 'YOU LOSE!', colors.WHITE, colors.BLACK)
    screen.blit(win_text, (410, 300))


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


def restart_game_window():
    restart_game = True

    while restart_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

        button('RESTART', 510, 450, 100, 50, colors.GREEN, game_loop)
        button('QUIT', 750, 450, 100, 50, colors.RED, quit_game)

        pygame.display.update()
        clock.tick(15)


def quit_game():
    pygame.quit()
    sys.exit()


def update(graph, player, player_2, deposit):
    screen.fill(colors.WHITE)
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
    for node in graph.nodes:
        if deposit.position == (node.rect[0], node.rect[1]):
            draw_circle(node, colors.EXIT)


# stores nodes and positions
class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.positions = dict()

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
    def __init__(self, action):
        self.image = None
        self.angle = 0
        self.position = random_pos()
        self.movement = [0, 0, 0, 0]
        self.rect = pygame.Rect(self.position[0], self.position[1], 20, 20)


class Deposit(object):
    def __init__(self):
        self.color = colors.EXIT
        self.position = random_pos()


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
                pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] - 20, node.rect.center[1] + 15, -45, 5))
                pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] - 20, node.rect.center[1] - 20, -45, 5))
                left_neighbour += 1
            elif node.rect[0] < neighbour.rect[0]:
                right_neighbour += 1
            elif node.rect[1] < neighbour.rect[1]:
                pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] + 14, node.rect.center[1] + 20, 5, 45))
                pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] - 20, node.rect.center[1] + 15, 5, 50))
                bottom_neighbour += 1
            elif node.rect[1] > neighbour.rect[1]:
                top_neighbour += 1

        if left_neighbour == 0:
            pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] - 20, node.rect.center[1] - 20, 5, 40))
        if right_neighbour == 0:
            pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] + 14, node.rect.center[1] - 20, 5, 40))
        if top_neighbour == 0:
            pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] - 20, node.rect.center[1] - 20, 39, 5))
        if bottom_neighbour == 0:
            pygame.draw.rect(screen, colors.NODE, (node.rect.center[0] - 20, node.rect.center[1] + 15, 39, 5))


# returns random position
def random_pos():
    return (random.randrange(starting_x, (((size[0] - 20) // spacing) * spacing), spacing),
            random.randrange(starting_y, (((size[1] - 20) // spacing) * spacing), spacing))


def draw_circle(node, color):
    return pygame.draw.circle(screen, color, node.rect.center, 10)


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
        if player.rect.center[1] > closest_y+8:
            player.rect.center = (player.rect.center[0], closest_y+8)
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
    "player1": load_animations("images/player1", [10, 10, 10]),
    "player2": load_animations("images/player2", [10, 10, 10]),
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


# main game loop where player input is read
def game_loop():
    global animation_frames
    player1_frame = 0
    player2_frame = 0
    graph = create_graph()
    player_1 = Player("player1")
    player_2 = Player("player2")
    player_1.color = colors.PLAYER
    player_2.color = colors.PLAYER2
    deposit = Deposit()
    deposit.position = random_pos()

    rev_graph = reverse_graph(graph)
    strongly_connect(graph, rev_graph, player_1.position)

    for node in graph.nodes:
        node.neighbours = dict.fromkeys(node.neighbours, random.randint(1, 3))

    draw_walls(graph)

    min_dist(graph, player_1, player_2, deposit)

    while True:

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_1.movement = [0, 0, 2, 0]
                if event.key == pygame.K_UP:
                    player_1.movement = [0, 0, 0, 2]
                if event.key == pygame.K_LEFT:
                    player_1.movement = [0, 2, 0, 0]
                if event.key == pygame.K_RIGHT:
                    player_1.movement = [2, 0, 0, 0]
                if event.key == pygame.K_s:
                    player_2.movement = [0, 0, 2, 0]
                if event.key == pygame.K_w:
                    player_2.movement = [0, 0, 0, 2]
                if event.key == pygame.K_a:
                    player_2.movement = [0, 2, 0, 0]
                if event.key == pygame.K_d:
                    player_2.movement = [2, 0, 0, 0]
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
