from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt

num_points_in_dataset = 4

# should be more than 2
assert(num_points_in_dataset > 2)

# generate the points
# points = np.random.rand(num_points_in_dataset, 2)
# this script does not use numpy, so convert them to regular
# lists after that

points = [[1, 1], [2, 3], [2, 2], [5, 5]]

#points = [[1, 1], [2, 2], [1, 2], [2, 1]]

print ("The points")
for point in points:
    print(point)
print()

# Build a convex hull from points. Hull indices are sorted
# counter-clockwise in the resulting object.

hull = ConvexHull(points)
print ("The convex hull constits of the following points (in indices)")
for i in hull.vertices:
    print(i)
print()

# The idea of the algorithm is to create a better point representation
# of the initial convex hull, and then build multiple
# Bezier curves from them. Here is the article that I learned this from
# http://www.malinc.se/m/MakingABezierSpline.php

# Generate the better grid first
# todo use enumerates & similar things
print("Generating more granular control points")
print()

granular_points = []

for i in range(len(hull.vertices)):
    # Split the segment of the convex hull, which is generated by
    # the current (i-th) and the next point in it, into three equal
    # segments.
    j = (hull.vertices[ (i + 1) % len(hull.vertices) ])
    i = (hull.vertices[ i ])

    dx = (points[i][0] - points[j][0]) / 3
    dy = (points[i][1] - points[j][1]) / 3

    print(f"Processing the following segment: {i} -> {j}")
    print(f"Obtained the dx: {dx}, dy: {dy}")
    print("Building the following intermediate control points")
    print(f"{points[i][0] - dx}, {points[i][1] - dy}")
    print(f"{points[i][0] - dx * 2}, {points[i][1] - dy * 2}")
    print()

    granular_points.append([points[i][0], points[i][1]])
    granular_points.append([points[i][0] - dx, points[i][1] - dy])
    granular_points.append([points[i][0] - 2 * dx, points[i][1] - 2 * dy])

assert(len(granular_points) == len(hull.vertices) * 3)

print("The resulting granular points are")
print(granular_points)
print()

print("Approximating the convex hull using cubic Bezier splines")
print()

# Weights should be either four x-values of the points that
# are used to build this Bezier curve, or their y-values.
# Some more intuition behind the function. It starts at w[0],
# is controlled by w[1] and w[2], and ends at w[3]. For more
# understanding, read this: https://pomax.github.io/bezierinfo/

# To draw the line, pass the weights w[] as the x-values or y-values
# of the four points used to build the Bezier curve, then iterate,
# for example, in a for-loop, varying `t` from 0 to 1 with a small
# step. To get more granular curve, decrease the step.

def bezier_cubic(t, w : []):

    print(f"T = {t}")

    t2 = t * t
    t3 = t2 * t
    mt = 1 - t
    mt2 = mt * mt
    mt3 = mt2 * mt
    return w[0] * mt3 + 3 * w[1] * mt2 * t + \
        3 * w[2] * mt * t2 + w[3] * t3

plot_points = []

# I know it is ugly....
i = 0
while (i < len(granular_points)):
    print(f'Building the bezier curve from the points {i} to {i + 3}')
    wx = [
        granular_points[i][0],
        granular_points[(i + 1) % len(granular_points)][0],
        granular_points[(i + 2) % len(granular_points)][0],
        granular_points[(i + 3) % len(granular_points)][0]
    ]
    wy = [
        granular_points[i][1],
        granular_points[(i + 1) % len(granular_points)][1],
        granular_points[(i + 2) % len(granular_points)][1],
        granular_points[(i + 3) % len(granular_points)][1]
    ]
    print(f'The weights are: {wx}, {wy}')
    print()

#    exit()

    plt.scatter(wx, wy, color = 'red')

    for t in range(1, 100):
        x = bezier_cubic(t / 100, wx)
        y = bezier_cubic(t / 100, wy)
        plot_points.append([x, y])

    i += 3

xvals = [p[0] for p in plot_points]
yvals = [p[1] for p in plot_points]

print(xvals)
print(yvals)

plt.scatter(xvals, yvals, color = 'blue')
plt.show()
