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
完整 Python 程式請見 marching_cubes_no_lut.py。

📸 執行結果
演算法成功提取隱式曲面，完全不使用查詢表。以下為兩個範例的輸出圖形。

球體 (Sphere)
x
2
+
y
2
+
z
2
−
0.49
=
0
x 
2
 +y 
2
 +z 
2
 −0.49=0

https://images/sphere.png

雙曲面 (Hyperboloid)
x
2
+
y
2
−
2
z
2
−
0.49
=
0
x 
2
 +y 
2
 −2z 
2
 −0.49=0

https://images/hyperboloid.png

圖片為 Matplotlib 產生的四視角合成圖（3D視角、前視、側視、俯視）。

🎮 與 Scratch / TurboWarp 的整合
核心邏輯——邊掃描、符號檢測、三角化——可以重構成 Scratch 積木或 TurboWarp 邏輯。利用清單、廣播與自訂積木，可以在教學環境中展示切片曲面或動畫遍歷，非常適合推廣數學與視覺化教育。

🚀 如何執行
安裝 Python 3.8+

安裝相依套件：

bash
pip install numpy matplotlib
執行腳本：

bash
python marching_cubes_no_lut.py
彈出的視窗會顯示 3D 曲面，可使用滑鼠拖曳旋轉視角。

📂 專案結構
text
MCA-WITHOUT-LOOKUPTABLE/
├── images/
│   ├── author.jpg               (作者照片)
│   ├── sphere.png               (球體成果圖)
│   └── hyperboloid.png          (雙曲面成果圖)
├── marching_cubes_no_lut.py     (主要演算法實作)
├── extended_abstract.html       (英文擴展摘要)
├── about-me.html                (作者介紹，中英文)
├── README.md                    (本檔)
└── LICENSE                      (MIT 授權)
👤 作者
<img src="images/author.jpg" alt="C.H. Tai" width="100" style="border-radius: 50%;" onerror="this.style.display='none'; this.insertAdjacentHTML('afterend', '<span style="display:inline-block; width:100px; height:100px; border-radius:50%; background:#2c7da0; color:white; text-align:center; line-height:100px; font-size:2rem;">CT</span>');">

戴清河 (C.H. Day(chday169))
土木及水利工程技師 (退休)
喜愛分享數學概念、工程實用程式與 3D 數學製圖。
📄 關於作者 (更多詳情)

📄 授權
MIT License。詳見 LICENSE 檔案。

🔗 引用
若在學術或教育工作中參考本方法，建議引用：

C.H. Tai. Geometric Marching Cubes Without Lookup Tables: From 2D Marching Squares to 3D Implicit Surface Reconstruction. GitHub repository, 2026. https://github.com/chday169/MCA_WITHOUT_LOOKTABLE

保持好奇 · 享受幾何
Stay curious · Enjoy geometry

text

---

## ✅ 最後確認步驟

1. **在您的 GitHub 倉庫根目錄**中，確認有以下檔案（名稱完全一致）：
   - `.nojekyll` (空白)
   - `index.html`
   - `about-me.html`
   - `extended_abstract.html`
   - `README.md`
   - `marching_cubes_no_lut.py` (您原本的程式)

2. **確認 `images/` 資料夾**內有三個檔案，檔名**完全小寫**：
   - `author.jpg`
   - `sphere.png`
   - `hyperboloid.png`

3. **等待 2 分鐘**後，用無痕模式訪問：
   - 首頁：`https://chday169.github.io/MCA_WITHOUT_LOOKTABLE/`
   - 作者頁：`https://chday169.github.io/MCA_WITHOUT_LOOKTABLE/about-me.html`
   - 摘要頁：`https://chday169.github.io/MCA_WITHOUT_LOOKTABLE/extended_abstract.html`

所有圖片應該都能正常顯示，數學公式也能渲染。

如果還有任何一個圖片顯示破裂，請在瀏覽器按 `F12` → 點選 `Network` 標籤 → 重新整理頁面 → 查看是哪個檔案回傳 404，然後回報給我那個檔案名稱，我再協助您確認。