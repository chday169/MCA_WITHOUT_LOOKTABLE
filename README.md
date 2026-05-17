# Geometric Marching Cubes Without Lookup Tables  
### 從 2D Marching Squares 到 3D 隱式曲面重建（無查表幾何方法）

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🧊 摘要

傳統 **Marching Cubes 演算法 (MCA)** 通常依賴預定義的 256 種拓撲情況的查詢表來從體素標量場建構等值面。雖然高效，但這種方法往往將真正的數學與幾何本質隱藏在工程化的查表操作背後。

本專案提出一種**不使用查找表**的 Marching Cubes 幾何解釋方法。其核心思想從 2D Marching Squares 演算法自然維度擴展到 3D 隱式曲面重建。

我們直接分析立方體邊上標量場值的符號變化，透過線性插值計算交點，然後幾何化地連接相鄰邊上的交點，生成局部表面片。這一視角揭示了 Marching Cubes 的真正本質不是查找表，而是：
- **符號交叉檢測**
- **隱式曲面的幾何逼近**
- **基於邊的插值**
- **局部幾何重建**

## 📐 數學原理

對於三維空間中的隱式函數：

\[
f(x,y,z) = 0
\]

定義了一個連續曲面。我們將其離散化為體素網格（立方體單元）。

每個立方體有 **8 個頂點** 和 **12 條邊**。對於一條邊，端點 \( P_1, P_2 \) 處的標量值為 \( f_1, f_2 \)。若：

- \( f_1 \cdot f_2 > 0 \)：邊與曲面無交點
- \( f_1 \cdot f_2 < 0 \)：曲面穿過該邊

交點透過線性插值計算：

\[
P = P_1 + t \cdot (P_2 - P_1), \quad t = \frac{0 - f_1}{f_2 - f_1} = \frac{f_1}{f_1 - f_2}
\]

得到的交點近似滿足 \( f(P) \approx 0 \)，因此位於隱式曲面上。

檢測完一個立方體所有邊上的交點後，我們將相鄰邊上的交點幾何連接成三角形，然後 marching 到相鄰體素，重複過程。

## 🖥️ 程式碼範例 (Python)

簡化的核心實作片段：

```python
import numpy as np

def march_cube(voxel, f, threshold=0.0):
    vertices = np.array([
        [0,0,0], [1,0,0], [1,1,0], [0,1,0],
        [0,0,1], [1,0,1], [1,1,1], [0,1,1]
    ])
    edges = [(0,1),(1,2),(2,3),(3,0),
             (4,5),(5,6),(6,7),(7,4),
             (0,4),(1,5),(2,6),(3,7)]

    intersected_edges = []
    for v1, v2 in edges:
        f1, f2 = voxel[v1], voxel[v2]
        if (f1 - threshold)*(f2 - threshold) < 0:
            t = (threshold - f1) / (f2 - f1)
            p = vertices[v1] + t*(vertices[v2] - vertices[v1])
            intersected_edges.append(p)

    # 簡單三角剖分（範例，完整實作見原始碼）
    triangles = []
    if len(intersected_edges) >= 3:
        for i in range(1, len(intersected_edges)-1):
            triangles.append([intersected_edges[0],
                              intersected_edges[i],
                              intersected_edges[i+1]])
    return triangles