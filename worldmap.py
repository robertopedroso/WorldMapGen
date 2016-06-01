from PIL import Image, ImageDraw
from noise import snoise2
import itertools
import random
import math

def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def radial_gradient(size):
    cx = cy = size / 2 - 1
    return [[dist(x, y, cx, cy) / (size / 2) for x in range(size)] for y in range(size)]

def noise_tile(x, y, seed):
    nx = float(x) / size - 0.5
    ny = float(y) / size - 0.5
    return snoise2(nx, ny, octaves=8, base=seed)

def normalize(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

def generate_heightmap(size, seed):
    hm = [[noise_tile(x, y, seed) for x in range(size)] for y in range(size)]

    # normalize to [0, 1]
    heights = list(itertools.chain.from_iterable(hm))
    xmin, xmax = min(heights), max(heights)
    return [[normalize(hm[y][x], xmin, xmax) for x in range(size)] for y in range(size)]

def point2square(x, y, scale):
    x *= scale
    y *= scale
    return [(x, y), (x+scale, y+scale)]

def generate_map(size, seed):
    gradient = radial_gradient(size)
    heightmap = generate_heightmap(size, seed)

    for y in range(size):
        for x in range(size):
            heightmap[y][x] -= gradient[y][x]

    return heightmap

def mapdata2png(mapdata, size, scale):
    im = Image.new('RGB', (size*scale, size*scale))
    draw = ImageDraw.Draw(im)

    for y in range(size):
        for x in range(size):
            square = point2square(x, y, scale)
            color = (0, 0, 0) if mapdata[y][x] > 0 else (255, 255, 255)
            draw.rectangle(square, fill=color)

    im.save('out.png', "PNG")

if __name__ == "__main__":
    size, scale, seed = 256, 5, random.randint(0, 255)
    worldmap = generate_map(size, seed)
    mapdata2png(worldmap, size, scale)
