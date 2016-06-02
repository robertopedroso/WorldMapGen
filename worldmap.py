from PIL import Image, ImageDraw
from noise import snoise2
import itertools
import random
import math

def dist(x1, y1, x2, y2):
    """Returns the euclidean distance between two points"""
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def radial_gradient(size):
    """Returns a square matrix containing a radial gradient of the given size"""
    cx = cy = size / 2 - 1
    return [[dist(x, y, cx, cy) / (size / 1.5) for x in range(size)] for y in range(size)]

def noise_tile(x, y, seed):
    """Computes a (simplex) noise value for a given coordinate and seed"""
    nx = float(x) / size - 0.5
    ny = float(y) / size - 0.5

    e = snoise2(nx, ny, octaves=8, base=seed)
    e += 0.5 * snoise2(2*nx, 2*ny, octaves=8, base=seed)
    e += 0.25 * snoise2(4*nx, 4*ny, octaves=8, base=seed)
    return e

def normalize(x, xmin, xmax):
    """Normalizes x on [0, 1] based on min and max of x range"""
    return (x - xmin) / (xmax - xmin)

def normalize2d(lst):
    """Normalizes a square matrix on [0, 1]"""
    flat = list(itertools.chain.from_iterable(lst))
    xmin, xmax = min(flat), max(flat)
    norm = [normalize(x, xmin, xmax) for x in flat]

    rowlen = len(lst[0])
    return [norm[i:i+rowlen] for i in range(0, rowlen**2, rowlen)]

def generate_heightmap(size, seed):
    """Generates a square matrix containing elevation values from simplex noise"""
    hm = [[noise_tile(x, y, seed) for x in range(size)] for y in range(size)]
    return normalize2d(hm)

def point2square(x, y, s):
    """Returns opposite vertex coordinate list for a rectangle whose top-left
       point is (x, y) and whose sides are length s."""
    x *= s
    y *= s
    return [(x, y), (x+s, y+s)]

def generate_map(size, seed):
    """Generates a world map of a given size with a given seed"""
    gradient = radial_gradient(size)
    heightmap = generate_heightmap(size, seed)

    for y in range(size):
        for x in range(size):
            heightmap[y][x] -= gradient[y][x]

    return normalize2d(heightmap)

def get_color(h):
    """Returns appropriate biome color for given elevation"""
    if (h < 0.55): return (0, 0, 255)
    elif (h < 0.6): return (237, 201, 175)
    elif (h < 0.7): return (116, 169, 99)
    elif (h < 0.8): return (34, 139, 34)
    elif (h < 0.85): return (164, 189, 125)
    elif (h < 0.95): return (206, 210, 208)
    else: return (255, 255, 255)

def mapdata2png(mapdata, size, scale):
    """Converts a square matrix of map data to a scaled png image"""
    im = Image.new('RGB', (size*scale, size*scale))
    draw = ImageDraw.Draw(im)

    for y in range(size):
        for x in range(size):
            square = point2square(x, y, scale)
            draw.rectangle(square, fill=get_color(mapdata[y][x]))

    im.save('out.png', "PNG")

if __name__ == "__main__":
    size, scale, seed = 256, 5, random.randint(0, 255)
    worldmap = generate_map(size, seed)
    mapdata2png(worldmap, size, scale)
