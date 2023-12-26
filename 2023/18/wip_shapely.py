import shapely
directions = { '0': 1, 'R': 1, '1': 1j, 'D': 1j, '2': -1, 'L': -1, '3': -1j, 'U': -1j, }

def main(data, variant=False):
    points = [row.split()[:2] for row in data.split('\n')]
    points = [(color[7], int(color[2:2+5], 16)) for color in [row.split()[2] for row in data.split('\n')]] if variant else points
    vertices = [0j]
    for dir, n in points: vertices.append(vertices[-1] + directions[dir] * int(n))

    inner_area = shapely.area(shapely.Polygon((v.real, v.imag) for v in vertices))
    edges = sum(0.5 * (abs(edge.real) + abs(edge.imag)) for edge in 
                (vertices[i] - vertices[(i + 1) % len(vertices)] for i in range(len(vertices))))
    corners = 4 * 0.25
    return int(inner_area + edges + corners)


data_test = open('input-sample.txt', 'r').read().strip()
print(main(data_test))
print(main(data_test, variant=True))

data = open('input.txt', 'r').read().strip()
print(main(data))
print(main(data, variant=True))

