# solver.py (IDA* with Manhattan + Linear Conflict heuristic)
import sys
import math
import time
import pygame
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "100,100"

# Goal configuration
goal = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

goal_positions = {val: (i, j) for i, row in enumerate(goal) for j, val in enumerate(row)}

def read_puzzle(filename):
    with open(filename) as f:
        puzzle = [list(map(int, line.strip().split())) for line in f.readlines()[:4]]
    return puzzle

def manhattan_linear_conflict(puzzle):
    dist = 0
    for i in range(4):
        for j in range(4):
            val = puzzle[i][j]
            if val == 0:
                continue
            goal_i, goal_j = goal_positions[val]
            dist += abs(goal_i - i) + abs(goal_j - j)
            if goal_i == i:
                for k in range(j + 1, 4):
                    other = puzzle[i][k]
                    if other != 0 and goal_positions[other][0] == i and goal_positions[other][1] < goal_j:
                        dist += 2
            if goal_j == j:
                for k in range(i + 1, 4):
                    other = puzzle[k][j]
                    if other != 0 and goal_positions[other][1] == j and goal_positions[other][0] < goal_i:
                        dist += 2
    return dist

def is_goal(p):
    return p == goal

def get_neighbors(board):
    neighbors = []
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                x, y = i, j
    directions = [(-1, 0, 'up'), (1, 0, 'down'), (0, -1, 'left'), (0, 1, 'right')]
    for dx, dy, move in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < 4 and 0 <= ny < 4:
            new_board = [row[:] for row in board]
            new_board[x][y], new_board[nx][ny] = new_board[nx][ny], new_board[x][y]
            neighbors.append((new_board, move))
    return neighbors

def ida_star(start):
    threshold = manhattan_linear_conflict(start)
    path = [(start, None)]

    def search(path, g, threshold):
        node, _ = path[-1]
        f = g + manhattan_linear_conflict(node)
        if f > threshold:
            return f
        if is_goal(node):
            return "FOUND"
        min_cost = float('inf')
        for neighbor, move in get_neighbors(node):
            if any(prev[0] == neighbor for prev in path):
                continue
            path.append((neighbor, move))
            temp = search(path, g + 1, threshold)
            if temp == "FOUND":
                return "FOUND"
            if temp < min_cost:
                min_cost = temp
            path.pop()
        return min_cost

    while True:
        print(f"Searching with threshold {threshold}...")
        temp = search(path, 0, threshold)
        if temp == "FOUND":
            return [m for _, m in path[1:]]
        if temp == float('inf'):
            return None
        threshold = temp

def draw_board(screen, board, font):
    screen.fill((255, 255, 255))
    screen_width, screen_height = screen.get_size()
    board_width, board_height = 400, 400
    offset_x = (screen_width - board_width) // 2
    offset_y = (screen_height - board_height) // 2

    for i in range(4):
        for j in range(4):
            val = board[i][j]
            if val != 0:
                pygame.draw.rect(screen, (100, 149, 237), (offset_x + j * 100 + 5, offset_y + i * 100 + 5, 90, 90))
                text = font.render(str(val), True, (255, 255, 255))
                rect = text.get_rect(center=(offset_x + j * 100 + 50, offset_y + i * 100 + 50))
                screen.blit(text, rect)
    pygame.display.flip()

def apply_move(board, move):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                x, y = i, j
    dx, dy = 0, 0
    if move == 'up': dx = -1
    elif move == 'down': dx = 1
    elif move == 'left': dy = -1
    elif move == 'right': dy = 1
    nx, ny = x + dx, y + dy
    if 0 <= nx < 4 and 0 <= ny < 4:
        board[x][y], board[nx][ny] = board[nx][ny], board[x][y]
    return board

def run_gui(start_board, solution):
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("15 Puzzle Solver")
    font = pygame.font.SysFont(None, 72)
    board = [row[:] for row in start_board]
    draw_board(screen, board, font)
    index = 0
    solved = False
    print("\n✅ GUI loaded. Press SPACE to step through solution. Close the window to exit.")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE and index < len(solution):
                    move = solution[index]
                    print(f"Move {index+1}/{len(solution)}: {move}")
                    board = apply_move(board, move)
                    draw_board(screen, board, font)
                    index += 1
                elif index == len(solution):
                    print("🎉 Puzzle solved! Press close to exit.")
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No puzzle file provided. Using default test puzzle.")
        puzzle = [
            [5, 1, 2, 3],
            [6, 0, 7, 4],
            [9, 10, 11, 8],
            [13, 14, 15, 12]
        ]
    else:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print(f"Error: file '{filename}' not found.")
            sys.exit(1)
        print("Reading puzzle...")
        puzzle = read_puzzle(filename)

    print("Solving puzzle...")
    start_time = time.time()
    solution = ida_star(puzzle)
    end_time = time.time()

    if solution:
        print(f"Solved in {len(solution)} moves. Time: {end_time - start_time:.2f}s")
        with open("output.txt", "w") as f:
            for move in solution:
                f.write(move + "\n")
        run_gui(puzzle, solution)
    else:
        print("No solution found.")

