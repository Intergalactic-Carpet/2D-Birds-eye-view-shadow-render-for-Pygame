# 2D-shadow-render-for-Pygame
A simple one function way to draw shadows in pygame

The only function you need is draw_shadows, documentation is in the docstring of draw_shadows but i'll provide some here.

# Documentation
Draws shadows in spaces behind obstacles relative to sensor_coord.

View point large distances from shadow edges can cause lower shadow quality,
you can increase rays to combat this, be careful as large amounts of rays (>1500)
can cause performance issues.

Parameters: 
surface - The surface to draw the shadows on e.g. screen.

obstacles: Things to block light (create shadows behind relative to view_coord)
 e.g. [((0, 0), (0, 10), (10, 10), (10, 0))].

view_coord - The coordinates of the view point e.g. (30, 56).

debug - Shows positions of view_coord, intersection points, rays drawn.

rays - The number of rays drawn, more rays increases shadow quality.

shadow_colour - The colour of the shadow e.g. (43, 43, 43), Although transparency doesn't throw an error,
for some reason transparency doesn't change it.

ValueError - If the length of coordinates per polygon is less than two.
