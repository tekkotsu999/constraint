import numpy as np
from scipy.optimize import minimize
from copy import deepcopy
import matplotlib.pyplot as plt

####################################################################################

# 座標を持つPointクラスを定義します。
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
# 2つのPointインスタンスを結ぶLineクラスを定義します。
# Lineインスタンスはその長さも計算します。
class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.length = self.calculate_length()

    # Lineインスタンスの長さを計算するメソッドです。
    def calculate_length(self):
        return np.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)


####################################################################################

# FixedPointConstraintクラスは、ある点が固定されていることを表現します。
# ポイントのインデックスを引数として取り、そのポイントの位置を最適化変数から取得する
class FixedPointConstraint:
    def __init__(self, point_idx):
        self.point_idx = point_idx
        self.initial_point = points[point_idx]

    # 初期位置からの変位を計算します。制約としてはこの変位が0であるべきです。
    def __call__(self, points_flat):
        current_point = Point(*points_flat[self.point_idx * 2: self.point_idx * 2 + 2])
        diff_vector =  np.array([self.initial_point.x, self.initial_point.y]) - np.array([current_point.x,current_point.y])
        return np.linalg.norm(diff_vector)


# FixedLengthConstraintクラスは、ある線の長さが固定されていることを表現します。
# ポイントのインデックスと初期の長さを引数として取り、そのラインの現在の長さを最適化変数から計算する
class FixedLengthConstraint:
    def __init__(self, point1_idx, point2_idx, initial_length):
        self.point1_idx = point1_idx
        self.point2_idx = point2_idx
        self.initial_length = initial_length

    # 線の現在の長さと初期の長さとの差を計算します。制約としてはこの差が0であるべきです。
    def __call__(self, points_flat):
        point1 = Point(*points_flat[self.point1_idx * 2: self.point1_idx * 2 + 2])
        point2 = Point(*points_flat[self.point2_idx * 2: self.point2_idx * 2 + 2])
        current_length = Line(point1, point2).length
        return current_length - self.initial_length


####################################################################################

# 目標点までの距離を計算する関数を生成します。これが最小化の対象となります。
def target_point_distance(target_point_index, target_position):
    def distance(points_flat):
        moving_point_position = points_flat[target_point_index * 2: target_point_index * 2 + 2]
        diff_vector = moving_point_position - np.array([target_position.x, target_position.y])
        return np.linalg.norm(diff_vector)
    return distance


####################################################################################

# 目標点への移動を試みる関数です。
def move_point(target_point, target_position, constraints):
    initial_points_flat = []
    for point in points:
        initial_points_flat.extend([point.x, point.y])
    initial_points_flat = np.array(initial_points_flat)

    target_point_index = points.index(target_point)
    target_distance = target_point_distance(target_point_index, target_position)

    constraints_for_optimization = []
    for c in constraints:
        constraint_dict = {'type': 'eq', 'fun': c}
        constraints_for_optimization.append(constraint_dict)

    res = minimize(target_distance, initial_points_flat, constraints=constraints_for_optimization, method='SLSQP')
    print(res)

    # 初期座標を抽出
    initial_x_values = [point.x for point in points]
    initial_y_values = [point.y for point in points]

    # 初期座標をプロット
    plt.figure()
    plt.scatter(initial_x_values, initial_y_values)
    plt.plot(initial_x_values, initial_y_values, linestyle='dashed', label='Initial Position')

    updated_points_flat = res.x
    updated_points = []
    for i in range(0, len(updated_points_flat), 2):
        updated_points.append(Point(updated_points_flat[i], updated_points_flat[i+1]))
    
    
    # 結果の座標を抽出
    x_values = [point.x for point in updated_points]
    y_values = [point.y for point in updated_points]

    # 結果をプロット
    plt.scatter(x_values, y_values)
    plt.plot(x_values, y_values)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Point Movement')
    plt.legend()
    plt.grid(True)
    plt.show()

    return updated_points

####################################################################################

# 例1
# 初期座標と目標座標を設定します。
a = Point(200, 100)
b = Point(200, 300)
c = Point(500, 400)
d = Point(500, 100)
points =[a,b,c,d]

ab = Line(a, b)
bc = Line(b, c)
cd = Line(c, d)
lines = [ab,bc,cd]

# 固定ポイントと固定長さの制約を定義します。ポイントのインデックスとラインの初期長さを使用します。
constraints = [
    FixedPointConstraint(0),
    FixedPointConstraint(3),
    FixedLengthConstraint(0, 1, ab.length),
    FixedLengthConstraint(1, 2, bc.length),
    FixedLengthConstraint(2, 3, cd.length)]

# 目標点
target_position = Point(600, 300)

# 点cを目標点に移動させます。
new_points = move_point(c, target_position, constraints)

# 新しい座標を表示します。
for point in new_points:
    print(point)


####################################################################################


print("n")

# 例2
a = Point(2, 2)
b = Point(5, 3)
points = [a, b]
ab = Line(a, b)
constraints = [FixedPointConstraint(0), FixedLengthConstraint(0, 1, ab.length)]
target_position = Point(5, 6)

new_points = move_point(b, target_position, constraints)
for point in new_points:
    print(point)