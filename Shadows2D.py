from shapely.geometry import Polygon
from math import sin, cos, radians
import pygame
pygame.init()


def draw_shadows(surface, obstacles: list, view_coord: list or tuple, debug=False, rays=1000,
                 shadow_colour=(43, 43, 43)):
    """
    Draws shadows in spaces behind obstacles relative to sensor_coord.

    View point large distances from shadow edges can cause lower shadow quality,
    you can increase rays to combat this, be careful as large amounts of rays > 1500
    can cause performance issues.

    :param surface: The surface to draw the shadows on e.g. screen.
    :param obstacles: Things to block light (create shadows behind relative to view_coord)
     e.g. [((0, 0), (0, 10), (10, 10), (10, 0))].
    :param view_coord: The coordinates of the view point e.g. (30, 56).
    :param debug: Shows positions of view_coord, intersection points, rays drawn.
    :param rays: The number of rays drawn, more rays increases shadow quality.
    :param shadow_colour: The colour of the shadow e.g. (43, 43, 43), Although transparency doesn't throw an error,
    for some reason transparency doesn't change it.
    :raises ValueError: If the length of coordinates per polygon is less than two
    """

    screen_width_, screen_height_ = 800, 600

    def line_intersection(p1, p2, q1, q2):
        det_ = (p2[0] - p1[0]) * (q2[1] - q1[1]) - (p2[1] - p1[1]) * (q2[0] - q1[0])
        if det_ == 0:
            return None

        lambda_numerator = (q2[1] - q1[1]) * (q2[0] - p1[0]) + (q1[0] - q2[0]) * (q2[1] - p1[1])
        mu_numerator = (p1[1] - p2[1]) * (q2[0] - p1[0]) + (p2[0] - p1[0]) * (q2[1] - p1[1])
        lambda_param = lambda_numerator / det_
        mu_param = mu_numerator / det_

        if 0 <= lambda_param <= 1 and 0 <= mu_param <= 1:
            intersection = (p1[0] + lambda_param * (p2[0] - p1[0]), p1[1] + lambda_param * (p2[1] - p1[1]))
            return intersection
        else:
            return None

    def cast_ray(origin, angle, obstacles__):
        ray_length = 1000  # Arbitrary large value
        ray_end = (origin[0] + ray_length * cos(angle), origin[1] + ray_length * sin(angle))

        closest_intersection = None
        min_distance = float('inf')

        for obstacle in obstacles__:
            for i in range(len(obstacle)):
                p1 = obstacle[i]
                p2 = obstacle[(i + 1) % len(obstacle)]

                intersection = line_intersection(origin, ray_end, p1, p2)

                if intersection is not None:
                    distance = (origin[0] - intersection[0]) ** 2 + (origin[1] - intersection[1]) ** 2
                    if distance < min_distance:
                        closest_intersection = intersection
                        min_distance = distance

        return closest_intersection

    def draw_lidar_map(sensor_pos_, obstacles_, angle_range, num_rays_):
        out = []
        for i in range(num_rays_):
            angle = radians(sensor_pos_[2] - angle_range / 2 + (angle_range * i / num_rays_))
            intersection = cast_ray(sensor_pos_[:2], angle, obstacles_)

            if intersection is not None:
                out.append(intersection)
        return out
    sensor_angle = pygame.time.get_ticks() % 360
    sensor_pos = (view_coord[0], view_coord[1], sensor_angle)
    det = Polygon(draw_lidar_map(sensor_pos, obstacles, 360, rays))
    s = Polygon([(0, 0), (screen_width_, 0), (screen_width_, screen_height_), (0, screen_height_)])
    result_polygons = s.difference(det)

    if isinstance(result_polygons, Polygon):
        result_polygons = [result_polygons]
    else:
        result_polygons = list(result_polygons.geoms)  # Convert MultiPolygon to list

    for result_polygon in result_polygons:
        result_polygon_coords = list(result_polygon.exterior.coords)
        pygame.draw.polygon(surface, shadow_colour, result_polygon_coords)

    if debug:
        for point in det.exterior.coords:
            pygame.draw.circle(surface, (0, 255, 0), point, 1, 1)
            pygame.draw.line(surface, (0, 0, 255), view_coord, point)
        pygame.draw.circle(surface, (255, 0, 0), sensor_pos[:2], 5, 0)
