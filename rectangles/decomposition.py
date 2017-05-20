import bisect
import turtle


class Edge:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_horizontal(self):
        return self.y1 == self.y2

    def is_vertical(self):
        return self.x1 == self.x2


class Rectangle:
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    def __str__(self):
        return "Rectangle(" + str(self.left) + ", " + str(self.right) + ", " + str(self.up) + ", " + str(self.down) + ")"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.left == other.left and self.right == other.right and\
                   self.up == self.up and self.down == other.down
        else:
            False

    def __ne__(self, other):
        return not self.__eq__(other)

def cover(edges, y1, y2):
    pos = bisect.bisect_left(edges, y1, 0, len(edges))
    if pos == len(edges) or edges[pos] != y1:
        edges.insert(pos, y1)
    else:
        edges.remove(y1)

    pos = bisect.bisect_left(edges, y2, 0, len(edges))
    if pos == len(edges) or edges[pos] != y2:
        edges.insert(pos, y2)
    else:
        edges.remove(y2)

    return edges


def make_rectangles(edges):
    if len(edges) == 0:
        raise ValueError("At least one edge must be provided")
    rectangles = []
    current_rectangles = []
    sorted_edges = sorted(edges, key=lambda edge: (edge.x2, edge.x1, edge.y1))
    current_left = sorted_edges[0].x1
    for i in range(len(sorted_edges)):
        if sorted_edges[i].x2 > current_left:
            for j in range(0, len(current_rectangles), 2):
                rectangles.append(Rectangle(current_left, sorted_edges[i].x2,
                                            current_rectangles[j + 1], current_rectangles[j]))
            current_left = sorted_edges[i].x2
        if sorted_edges[i].is_vertical():
            cover(current_rectangles, sorted_edges[i].y1, sorted_edges[i].y2)

    return rectangles


# ==========================
#     GRAPHICS
# ==========================


def draw_polygon(edges):
    for edge in edges:
        turtle.up()
        turtle.goto(edge.x1, edge.y1)
        turtle.down()
        turtle.circle(1)
        turtle.goto(edge.x2, edge.y2)


def draw_rectangles(rectangles):
    for rectangle in rectangles:
        turtle.up()
        turtle.goto(rectangle.left, rectangle.down)
        turtle.down()
        turtle.goto(rectangle.left, rectangle.up)
        turtle.goto(rectangle.right, rectangle.up)
        turtle.goto(rectangle.right, rectangle.down)
        turtle.goto(rectangle.left, rectangle.down)


def demo(edges):
    rectangles = make_rectangles(edges)
    for r in rectangles:
        print(r)

    draw_polygon(edges)
    draw_rectangles(rectangles)

    turtle.mainloop()

print [Rectangle(0,0,0,0)]