import numpy as np

class Node:
    """
    Nodeのインデックス，座標および境界条件をまとめておくクラス（2次元用）

    Attributes:
        id(int): Nodeのインデックス番号（重複不可）
        x, y(float): Nodeのx,y座標
    """
    def __init__(self, idx, x, y):
        self.id = idx
        self.x = x
        self.y = y

    def __str__(self):
        return 'Node {}: x {}, y {}'.format(self.id, self.x, self.y)

class Element:
    """
    四角形１次要素Elementのインデックス，要素内のNode情報および要素の厚みをまとめておくクラス

    Attributes:
        id(int): Elementのインデックス番号（重複不可）
        node([int, int, int, int]): 要素内のNodeのインデックスのリスト（左下から反時計回りで指定）
        thickness(float): Elementの厚み
        xy(ndarray(size:2, 4)):Element内のNodeのxy座標まとめ
    """
    def __init__(self, idx, node_idxs, thickness):
        self.id = idx
        self.node = node_idxs
        self.thickness = thickness
        self.xy = None

    def __str__(self):
        return 'Element{}: Node{}, Thickness:{}'.format(self.id, self.node, self.thickness)

    def get_coordination(self, nodes_dict):
        """
        要素の各節点のx, y座標を求めてself.xyに代入
        Args:
            node_dict({Node.id: Node}): Nodeの辞書
        """

        res = []
        for node_idx in self.node:
            res.append([nodes_dict[node_idx].x, nodes_dict[node_idx].y])
        self.xy = np.array(res)

class Mesh:
    """
    NodeオブジェクトとElementオブジェクトをまとめておくクラス
    Attributes:
        nodes([Node.id: Node}): Nodeの辞書
        elements(list): Elementのリスト
    """

    def __init__(self, nodes_dict, elements):
        self.nodes = nodes_dict
        self.elements = elements
        self.get_element_coord()

    def get_element_coord(self):
        for elm in self.elements:
            elm.get_coordination(self.nodes)

mesh_size = 2.
length = 10.
height = 10.

# Nodeの作成
num_mesh_len = int(length / mesh_size)
num_mesh_hei = int(height / mesh_size)
if num_mesh_len == 0:
    num_mesh_len = 1
if num_mesh_hei == 0:
    num_mesh_hei = 1
x = np.linspace(0, length, num_mesh_len + 1)
y = np.linspace(0, height, num_mesh_hei + 1)
X, Y = np.meshgrid(x, y)
X = X.ravel()
Y = Y.ravel()

nodes_dict = {}
for i, coord in enumerate(zip(X, Y)):
    nodes_dict[i] = Node(i, coord[0], coord[1])

for node in nodes_dict.values():
    print(node)

thickness = 1.

# Elementの作成
node_idx = 0
elem_idx = 0
elems = []
for i in range(num_mesh_hei):
    for j in range(num_mesh_len + 1):
        if (node_idx + 1) % (num_mesh_len + 1) == 0:
            node_idx += 1
            continue
        else:
            node_idxs = [node_idx, node_idx + 1,
                        node_idx + num_mesh_len + 2, node_idx + num_mesh_len + 1]
            elems.append(Element(elem_idx, node_idxs, thickness))
            node_idx += 1
            elem_idx += 1
import matplotlib.pyplot as plt
from matplotlib import patches


def create_mesh(length, height, mesh_size, thickness):
    """
    モデルを格子点に分割し、全ての点のNodeクラスおよびそれらを使用した4角形1次要素を作成する.
    ただし、モデル形状は四角形とする。

    Args:
        length, height (float): モデルの長さ、高さ
        mesh_size (float): 分割したいメッシュのサイズ
        thickness (float): 要素の厚み(今回は全て一定とする)

    Returns:
        nodes_dict ({Node.id: Node}): 作成したNodeの辞書
        elsms (list): 作成したElementクラスをまとめたリスト
    """
    # Nodeの作成
    num_mesh_len = int(length / mesh_size)
    num_mesh_hei = int(height / mesh_size)
    if num_mesh_len == 0:
        num_mesh_len = 1
    if num_mesh_hei == 0:
        num_mesh_hei = 1
    x = np.linspace(0, length, num_mesh_len + 1)
    y = np.linspace(0, height, num_mesh_hei + 1)
    X, Y = np.meshgrid(x, y)
    X = X.ravel()
    Y = Y.ravel()

    nodes_dict = {}
    for i, coord in enumerate(zip(X, Y)):
        nodes_dict[i] = Node(i, coord[0], coord[1])

    # Elementの作成
    node_idx = 0
    elem_idx = 0
    elems = []
    for i in range(num_mesh_hei):
        for j in range(num_mesh_len + 1):
            if (node_idx + 1) % (num_mesh_len + 1) == 0:
                node_idx += 1
                continue
            else:
                node_idxs = [node_idx, node_idx + 1,
                             node_idx + num_mesh_len + 2, node_idx + num_mesh_len + 1]
                elems.append(Element(elem_idx, node_idxs, thickness))
                node_idx += 1
                elem_idx += 1
    return nodes_dict, elems


def plot_mesh(mesh):
    fig, ax = plt.subplots()
    for elem in mesh.elements:
        patch = patches.Polygon(xy=elem.xy, ec='black')
        ax.add_patch(patch)
        text_xy = np.mean(elem.xy, axis=0)
        ax.text(text_xy[0], text_xy[1], elem.id, fontsize=12, va='center', ha='center')
    for node in mesh.nodes.values():
        ax.scatter(node.x, node.y, fc='black', s=100)
        ax.text(node.x, node.y, node.id, fontsize=8, color='white', va='center', ha='center')
    ax.autoscale()
    ax.set_aspect('equal', 'box')
    plt.show()


# モデル、要素サイズ定義
MESH_SIZE = 5.
LENGTH = 10.
HEIGHT = 10.
THICKNESS = 1.

nodes_dict, elems = create_mesh(LENGTH, HEIGHT, MESH_SIZE, THICKNESS)
mesh = Mesh(nodes_dict, elems)
for node in mesh.nodes.values():
    print(node)
for elem in mesh.elements:
    print(elem)

plot_mesh(mesh)