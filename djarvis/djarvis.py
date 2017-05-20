import time
import turtle
import math
import pp


def distance(x1, y1, x2, y2):
    return math.sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))


def angle(dx, dy, x1, y1, x2, y2):
    s = dx * (x2 - x1) + dy * (y2 - y1)
    l = distance(x1, y1, x2, y2)
    if l == 0:
        return -3
    else:
        return s / l


def get_min(points):
    min_x = points[0][0]
    min_y = points[0][1]

    for x in points:
        if min_y > x[1] | (min_y == x[1] & min_x > x[0]):
            min_x, min_y = x
    return min_x, min_y


def next_left(x, y, dx, dy, points):
    k = -2
    for j in points:
        if k < angle(dx, dy, x, y, j[0], j[1]):
            k = angle(dx, dy, x, y, j[0], j[1])
            x1, y1 = j
    return x1, y1


def go_djarvis(points):
    result = []
    dx = -1
    dy = 0
    i = 0
    min_x, min_y = get_min(points)
    x, y = get_min(points)
    result.append((x, y))

    while (i == 0) | (x != min_x) | (y != min_y):
        i += 1
        k = -2
        for point in points:
            if k < angle(dx, dy, x, y, point[0], point[1]):
                k = angle(dx, dy, x, y, point[0], point[1])
                x1, y1 = point
        p = next_left(x, y, dx, dy, points)
        dx = (p[0] - x) / distance(x, y, p[0], p[1])
        dy = (p[1] - y) / distance(x, y, p[0], p[1])
        x, y = p
        result.append((x, y))
    return result


# ==========================
#        GRAPHICS
# ==========================


def draw_points(points):
    for x in points:
        turtle.up()
        turtle.goto(x[0], x[1])
        turtle.down()
        turtle.circle(1)
        turtle.up()


def draw_circle(points):
    turtle.goto(points[0])
    turtle.down()
    for point in points:
        turtle.goto(point)


# ============================


def demo(points):
    draw_points(points)

    print 'with paralel python'
    job_server = pp.Server(4, ppservers=())
    job1 = job_server.submit(go_djarvis, (points,), (angle, distance, get_min, next_left,), ("math",))
    print "Starting pp with", job_server.get_ncpus(), "workers"
    start = time.time()
    print "Start : %s" % start
    result = job1()
    end = time.time()
    print "End : %s" % end
    print "Time elapsed:", end - start

    draw_circle(result)

    turtle.mainloop()
