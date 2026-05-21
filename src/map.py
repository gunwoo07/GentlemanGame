from src.config import *

def get_pos(ix, iy):
    x = ix*TILE_SIZE + TILE_SIZE/2 + MARGIN
    y = iy*TILE_SIZE + TILE_SIZE/2 + MARGIN
    return x, y

def get_pos_lefttop(ix, iy):
    x = ix*TILE_SIZE + MARGIN
    y = iy*TILE_SIZE + MARGIN
    return x, y

game_map = [
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
]

def find_shortest_path(game_map):
    rows = len(game_map)
    cols = len(game_map[0])

    start = None
    end = None

    # 시작점(2), 도착점(3) 찾기
    for y in range(rows):
        for x in range(cols):
            if game_map[y][x] == 2:
                start = (x, y)
            elif game_map[y][x] == 3:
                end = (x, y)

    if start is None or end is None:
        return []

    # BFS용 리스트
    queue = [start]
    visited = [start]

    # 이전 좌표 저장
    prev = {}

    # 상하좌우
    directions = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0)
    ]

    while len(queue) > 0:

        x, y = queue.pop(0)

        # 도착
        if (x, y) == end:
            break

        for dx, dy in directions:

            nx = x + dx
            ny = y + dy

            # 맵 밖
            if nx < 0 or ny < 0 or nx >= cols or ny >= rows:
                continue

            # 벽
            if game_map[ny][nx] == 1 or game_map[ny][nx] == 4:
                continue

            # 방문 안 했으면
            if (nx, ny) not in visited:

                visited.append((nx, ny))
                queue.append((nx, ny))

                # 어디서 왔는지 저장
                prev[(nx, ny)] = (x, y)

    # 길 없음
    if end not in visited:
        return []

    # 경로 복원
    path = []

    cur = end

    while cur != start:
        path.append([cur[0], cur[1]])
        cur = prev[cur]

    path.append([start[0], start[1]])

    path.reverse()

    return path

