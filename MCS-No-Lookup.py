"""
...
👨‍💻 Author: C.H. (戴清河)
🗓️ Date: July 14, 2025

📷 Preview: See `sphere_view.png` in this folder for example results.

📄 LICENSE: MIT License — See details at the bottom of this script.
"""

# [Your full program code here]

"""
📄 LICENSE

MIT License

Copyright (c) 2025 C.H. (戴清河)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction...

[license text continues]
"""

import numpy
import matplotlib
from matplotlib.lines import Line2D
import tkinter
import tkinter as tk
import math
import os, sys
import numpy as np
try:
    window = tk.Tk()
except:
    window = tk.tk()
window.title("Contours methods : designed by chday169戴清河")
canvas = tk.Canvas(window, width=1400, height=900, bg="white")
canvas.pack()

def Mcs_no_lookup_table():
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    import random
    iprob=1
    grid_size = 30
    spacing = 1.0 / grid_size

    # Define implicit function for sphere
    def f(x, y, z, r=0.49, cx=0.5, cy=0.5, cz=0.5,iprob=iprob):
        if iprob==0:
            return (x - cx)**2 + (y - cy)**2 + (z - cz)**2 - r**2
        else:
            return (x - cx) ** 2 + (y - cy) ** 2 - 2*(z - cz) ** 2 - r ** 2
    # Vertex offsets (base = 0)
    cube_vertex_offsets = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
    ])

    edge_to_vertex = [(0, 1), (1, 2), (2, 3), (3, 0),
                      (4, 5), (5, 6), (6, 7), (7, 4),
                      (0, 4), (1, 5), (2, 6), (3, 7)]

    triangles = []
    colors = []

    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(grid_size):
                origin = np.array([i, j, k]) * spacing
                cube_vertices = origin + cube_vertex_offsets * spacing
                values = [f(*v) for v in cube_vertices]
                points = []

                for a, b in edge_to_vertex:
                    va, vb = values[a], values[b]
                    if va * vb < 0:
                        t = va / (va - vb)
                        pa, pb = cube_vertices[a], cube_vertices[b]
                        p = pa + t * (pb - pa)
                        points.append(p)

                # Remove duplicates
                filtered = []
                eps = 1e-5
                for p in points:
                    if all(np.linalg.norm(p - q) > eps for q in filtered):
                        filtered.append(p)

                # Create triangles
                if len(filtered) >= 3:
                    color = [random.random() for _ in range(3)]
                    for m in range(1, len(filtered) - 1):
                        v0, v1, v2 = filtered[0], filtered[m], filtered[m + 1]
                        triangles.append([v0, v1, v2])
                        colors.append(color)

    # Setup 3D plots
    fig = plt.figure(figsize=(16, 14))
    all_coords = np.array([pt for tri in triangles for pt in tri])
    min_bounds = all_coords.min(axis=0)
    max_bounds = all_coords.max(axis=0)

    def draw_view(ax, title, elev, azim):
        ax.set_title(title)
        ax.view_init(elev=elev, azim=azim)
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors,
                                             edgecolor='k', linewidths=0.2, alpha=0.9))
        ax.set_xlim(min_bounds[0] - 0.25, max_bounds[0] + 0.25)
        ax.set_ylim(min_bounds[1] - 0.25, max_bounds[1] + 0.25)
        ax.set_zlim(min_bounds[2] - 0.25, max_bounds[2] + 0.25)

    draw_view(fig.add_subplot(2, 2, 1, projection='3d'), "3D View", 20, 30)
    draw_view(fig.add_subplot(2, 2, 2, projection='3d'), "Front View", 10, -90)
    draw_view(fig.add_subplot(2, 2, 3, projection='3d'), "Side View", 10, 0)
    draw_view(fig.add_subplot(2, 2, 4, projection='3d'), "Top View", 90, -90)

    plt.tight_layout()
    suffix = "sphere" if iprob == 0 else "hyperboloid"
    fig.savefig(f"{suffix}_view.png", dpi=300)
    plt.show()


    # Run the simplified version






menu = tk.Menu(window)
menu_import_menu = tk.Menu(menu, tearoff=0)
tools_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='tools ', menu=tools_menu)
tools_menu.add_command(label='論壇****Mcs_no_lookup_table****',command=Mcs_no_lookup_table)
window.config(menu=menu)
canvas.mainloop()