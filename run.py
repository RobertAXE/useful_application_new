import sys
import heapq


def parse_input(lines):
    depth = len(lines) - 3
    hallway = tuple("." for _ in range(11))

    rooms = []
    for i in range(4):
        room = []
        for j in range(depth):
            room.append(lines[2 + j][3 + 2 * i])
        rooms.append(tuple(room))

    return (hallway, tuple(rooms)), depth


def is_goal(state, depth):
    hallway, rooms = state
    for i in range(4):
        target = chr(ord("A") + i)
        for pod in rooms[i]:
            if pod != target:
                return False
    return True


def path_clear(hallway, start, end):
    if start < end:
        rng = range(start + 1, end + 1)
    else:
        rng = range(end, start)

    for i in rng:
        if hallway[i] != ".":
            return False
    return True


def moves_from_room(state, depth):
    ROOM_POS = [2, 4, 6, 8]
    HALL_VALID = [0, 1, 3, 5, 7, 9, 10]
    COST = {"A": 1, "B": 10, "C": 100, "D": 1000}

    hallway, rooms = state
    moves = []

    for r in range(4):
        room = rooms[r]


        top_idx = None
        pod = None
        for i in range(depth):
            if room[i] != ".":
                top_idx = i
                pod = room[i]
                break

        if pod is None:
            continue


        ok = True
        for p in room:
            if p != "." and (ord(p) - ord("A")) != r:
                ok = False
                break
        if ok:
            continue

        pos = ROOM_POS[r]
        cost_per_step = COST[pod]


        for direction in (-1, 1):
            cur = pos
            while 0 <= cur + direction < 11:
                cur += direction
                if hallway[cur] != ".":
                    break
                if cur not in HALL_VALID:
                    continue

                steps = top_idx + 1 + abs(cur - pos)
                move_cost = steps * cost_per_step

                new_hallway = list(hallway)
                new_rooms = [list(x) for x in rooms]

                new_hallway[cur] = pod
                new_rooms[r][top_idx] = "."

                new_state = (tuple(new_hallway), tuple(tuple(x) for x in new_rooms))
                moves.append((new_state, move_cost))
    return moves


def moves_from_hallway(state, depth):
    ROOM_POS = [2, 4, 6, 8]
    COST = {"A": 1, "B": 10, "C": 100, "D": 1000}
    hallway, rooms = state
    moves = []

    for i in range(11):
        pod = hallway[i]
        if pod == ".":
            continue

        r = ord(pod) - ord("A")
        room = rooms[r]


        wrong_inside = False
        for p in room:
            if p != "." and p != pod:
                wrong_inside = True
                break
        if wrong_inside:
            continue

        room_pos = ROOM_POS[r]
        if not path_clear(hallway, i, room_pos):
            continue


        for d in range(depth - 1, -1, -1):
            if room[d] == ".":
                depth_idx = d
                break

        steps = abs(i - room_pos) + depth_idx + 1
        move_cost = steps * COST[pod]

        new_hallway = list(hallway)
        new_rooms = [list(x) for x in rooms]

        new_hallway[i] = "."
        new_rooms[r][depth_idx] = pod

        new_state = (tuple(new_hallway), tuple(tuple(x) for x in new_rooms))
        moves.append((new_state, move_cost))

    return moves


def possible_moves(state, depth):
    moves = moves_from_hallway(state, depth)
    if moves:
        return moves
    return moves_from_room(state, depth)


def dijkstra(start, depth):
    pq = []
    heapq.heappush(pq, (0, start))
    best = {start: 0}

    while pq:
        cost, state = heapq.heappop(pq)

        if best[state] != cost:
            continue

        if is_goal(state, depth):
            return cost

        for new_state, move_cost in possible_moves(state, depth):
            new_cost = cost + move_cost

            if new_cost < best.get(new_state, 10**15):
                best[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))

    return None


def solve(lines):
    start, depth = parse_input(lines)
    result = dijkstra(start, depth)
    return result


def main():
    lines = []
    for line in sys.stdin:
        lines.append(line.rstrip('\n'))

    result = solve(lines)
    print(result)

# иии?
# main
if __name__ == '__main__':
    main()
