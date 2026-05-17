"""
🧊 Marching Cubes Surface Extraction (No Lookup Table)
Designed by C.H. (戴清河) — July 14, 2025
"""
🧊 Marching Cubes Surface Extraction (No Lookup Table)
Designed by C.H. (戴清河) — July 14, 2025

This script demonstrates a minimal implementation of Marching Cubes for extracting 3D surfaces from implicit functions — without relying on predefined lookup tables. Great for educational platforms like Scratch, TurboWarp, or standalone Python environments.
"""
🧊 Marching Cubes Surface Extraction (No Lookup Table)
Designed by C.H. (戴清河) — July 14, 2025

This script demonstrates a minimal implementation of the Marching Cubes algorithm for extracting 3D surfaces from implicit functions — without relying on predefined lookup tables. It’s ideal for educational platforms like Scratch, TurboWarp, or Python environments, thanks to its modular logic and visual clarity.

✨ Features:
- Extracts surface triangles from implicit 3D functions `f(x, y, z)`
- Detects edge sign changes to locate surface crossings
- Triangulates intersection points using a radial fan (lookup-free)
- Visualizes from multiple viewpoints using `matplotlib`
- Easily adaptable for teaching geometry in both text-based and block-based platforms

🎮 Scratch & TurboWarp Compatibility:
The core algorithm — edge scanning, sign detection, and triangulation — can be restructured using Scratch blocks or TurboWarp logic. With simple list structures, broadcasts, and custom blocks, it’s possible to visualize sliced surfaces or animate traversal for educational demonstrations.

📈 Supported Surfaces:
Use `iprob = 0` for Sphere, `iprob = 1` for Hyperboloid

📦 How to Run:
1. Install Python 3.8+ if you don’t have it
2. Install required libraries:
   pip install numpy matplotlib
3. Run this script:
   python mcs_combined_viewer.py

🖼️ Save plots via the viewer’s floppy disk icon (🖫), or drag to rotate and explore interactively

📷 Preview: See `sphere_view.png` and `hyperboloid_view.png` in this folder

📄 LICENSE: MIT License — See below in this script

👨‍💻 Author: C.H. (戴清河)
🗓️ Date: July 14, 2025
"""


📈 Supported Surfaces:
Use `iprob = 0` for Sphere, `iprob = 1` for Hyperboloid

📦 How to Run:
1. Install Python 3.8+ if you don’t have it
2. Install required libraries:
   pip install numpy matplotlib
3. Run this script in your terminal or IDE:
   python mcs_combined_viewer.py

🖼️ Save or share your plots via the viewer’s toolbar (🖫 floppy disk icon)

👨‍💻 Author: C.H. (戴清河)
🗓️ Date: July 14, 2025
"""
"""
...
👨‍💻 Author: C.H. (戴清河)
🗓️ Date: July 14, 2025

📷 Preview: See `sphere_view.png` in this folder for example results.

📄 LICENSE: MIT License — See details at the bottom of this script.
"""
"""
📄 LICENSE

MIT License

Copyright (c) 2025 C.H. (戴清河)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to deal in the Software
without restriction...

[license text continues]
"""
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random

# GUI window setup
window = tk.Tk()
window.title("Contours Methods — Designed by chday169 戴清河")
canvas = tk.Canvas(window, width=1400, height=900, bg="white")
canvas.pack()

def Mcs_no_lookup_table():
    grid_size = 30
    spacing = 1.0 / grid_size

    def f(x, y, z, r=0.49, cx=0.5, cy=0.5, cz=0.5, iprob=1):
        if iprob == 0:
            return (x - cx)**2 + (y - cy)**2 + (z - cz)**2 - r**2
        else:
            return (x - cx)**2 + (y - cy)**2 - 2*(z - cz)**2 - r**2

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
                        p = cube_vertices[a] + t * (cube_vertices[b] - cube_vertices[a])
                        points.append(p)

                # Remove near duplicates
                filtered = []
                eps = 1e-5
                for p in points:
                    if all(np.linalg.norm(p - q) > eps for q in filtered):
                        filtered.append(p)

                if len(filtered) >= 3:
                    col = [random.random() for _ in range(3)]
                    for m in range(1, len(filtered) - 1):
                        triangles.append([filtered[0], filtered[m], filtered[m + 1]])
                        colors.append(col)

    # Plot setup
    fig = plt.figure(figsize=(16, 14))
    all_coords = np.array([pt for tri in triangles for pt in tri])
    min_bounds, max_bounds = all_coords.min(axis=0), all_coords.max(axis=0)

    def draw_view(ax, title, elev, azim):
        ax.set_title(title)
        ax.view_init(elev=elev, azim=azim)
        ax.add_collection3d(Poly3DCollection(triangles, facecolors=colors,
                                             edgecolor='k', linewidths=0.2, alpha=0.9))
        ax.set_xlim(min_bounds[0] - 0.25, max_bounds[0] + 0.25)
        ax.set_ylim(min_bounds[1] - 0.25, max_bounds[1] + 0.25)
        ax.set_zlim(min_bounds[2] - 0.25, max_bounds[2] + 0.25)

    views = [("3D View", 20, 30), ("Front View", 10, -90),
             ("Side View", 10, 0), ("Top View", 90, -90)]

    for i, (title, elev, azim) in enumerate(views):
        draw_view(fig.add_subplot(2, 2, i + 1, projection='3d'), title, elev, azim)

    plt.tight_layout()
    plt.show()

# Menu setup
menu = tk.Menu(window)
tools_menu = tk.Menu(menu, tearoff=0)
tools_menu.add_command(label='論壇****Mcs_no_lookup_table****', command=Mcs_no_lookup_table)
menu.add_cascade(label='Tools', menu=tools_menu)
window.config(menu=menu)

canvas.mainloop()

"""📌 Note: After launching the app, use the "Tools → 論壇****Mcs_no_lookup_table****" menu to begin visualization.

****