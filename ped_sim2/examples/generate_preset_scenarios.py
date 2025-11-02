"""
预置场景生成器 - 创建5个复杂的城市场景
Preset Scenario Generator - Creates 5 complex urban scenarios
"""
import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.environment import Environment
from src.simulation.simulator import Simulator


class ScenarioGenerator:
    """生成预置场景的工具类"""
    
    @staticmethod
    def create_downtown_street():
        """
        场景1：繁忙十字路口 (Busy Intersection)
        - 十字路口，四个方向道路
        - 人行横道 (斑马线)
        - 红绿灯区域
        - 四角建筑物 (商店、办公楼)
        - 人数：500-1500
        """
        env = Environment(width=80, height=80)
        
        # === 外围边界 ===
        env.add_wall((0, 0), (80, 0))
        env.add_wall((80, 0), (80, 80))
        env.add_wall((80, 80), (0, 80))
        env.add_wall((0, 80), (0, 0))
        
        # === 十字路口中心区域 (30×30m) ===
        # 中心路口范围: (25, 25) 到 (55, 55)
        
        # 东西向道路边界
        env.add_wall((0, 25), (25, 25))    # 西侧上边界
        env.add_wall((55, 25), (80, 25))   # 东侧上边界
        env.add_wall((0, 55), (25, 55))    # 西侧下边界
        env.add_wall((55, 55), (80, 55))   # 东侧下边界
        
        # 南北向道路边界
        env.add_wall((25, 0), (25, 25))    # 北侧左边界
        env.add_wall((25, 55), (25, 80))   # 南侧左边界
        env.add_wall((55, 0), (55, 25))    # 北侧右边界
        env.add_wall((55, 55), (55, 80))   # 南侧右边界
        
        # === 人行横道 (斑马线) - 用短墙表示 ===
        # 北侧斑马线 (横向)
        for i in range(28, 52, 3):
            env.add_wall((i, 24), (i + 1.5, 24))
        
        # 南侧斑马线 (横向)
        for i in range(28, 52, 3):
            env.add_wall((i, 56), (i + 1.5, 56))
        
        # 西侧斑马线 (纵向)
        for i in range(28, 52, 3):
            env.add_wall((24, i), (24, i + 1.5))
        
        # 东侧斑马线 (纵向)
        for i in range(28, 52, 3):
            env.add_wall((56, i), (56, i + 1.5))
        
        # === 四角建筑物 ===
        # 西北角 - 商店
        env.add_wall((5, 5), (20, 5))
        env.add_wall((20, 5), (20, 20))
        env.add_wall((20, 20), (5, 20))
        env.add_wall((5, 20), (5, 5))
        # 商店入口
        env.add_wall((5, 10), (5, 12))
        
        # 东北角 - 办公楼
        env.add_wall((60, 5), (75, 5))
        env.add_wall((75, 5), (75, 20))
        env.add_wall((75, 20), (60, 20))
        env.add_wall((60, 20), (60, 5))
        env.add_wall((60, 10), (60, 12))
        
        # 西南角 - 餐厅
        env.add_wall((5, 60), (20, 60))
        env.add_wall((20, 60), (20, 75))
        env.add_wall((20, 75), (5, 75))
        env.add_wall((5, 75), (5, 60))
        env.add_wall((5, 65), (5, 67))
        
        # 东南角 - 银行
        env.add_wall((60, 60), (75, 60))
        env.add_wall((75, 60), (75, 75))
        env.add_wall((75, 75), (60, 75))
        env.add_wall((60, 75), (60, 60))
        env.add_wall((60, 65), (60, 67))
        
        # === 街道设施 (树木、座椅、广告牌) ===
        # 西北区域
        obstacles_nw = [(10, 23), (15, 23), (23, 10), (23, 15)]
        # 东北区域
        obstacles_ne = [(65, 23), (70, 23), (57, 10), (57, 15)]
        # 西南区域
        obstacles_sw = [(10, 57), (15, 57), (23, 65), (23, 70)]
        # 东南区域
        obstacles_se = [(65, 57), (70, 57), (57, 65), (57, 70)]
        
        for ox, oy in obstacles_nw + obstacles_ne + obstacles_sw + obstacles_se:
            env.add_wall((ox, oy), (ox + 0.8, oy))
            env.add_wall((ox + 0.8, oy), (ox + 0.8, oy + 0.8))
            env.add_wall((ox + 0.8, oy + 0.8), (ox, oy + 0.8))
            env.add_wall((ox, oy + 0.8), (ox, oy))
        
        # === 出入口 (四个方向) ===
        # 北侧 (行人从北向南)
        env.add_entrance((40, 2), radius=2.5, flow_rate=6.0)
        
        # 南侧 (行人从南向北)
        env.add_entrance((40, 78), radius=2.5, flow_rate=6.0)
        
        # 西侧 (行人从西向东)
        env.add_entrance((2, 40), radius=2.5, flow_rate=6.0)
        
        # 东侧 (行人从东向西)
        env.add_entrance((78, 40), radius=2.5, flow_rate=6.0)
        
        # 建筑物入口 (作为额外人流来源)
        env.add_entrance((3, 11), radius=1.2, flow_rate=3.0)   # 西北商店
        env.add_entrance((58, 11), radius=1.2, flow_rate=3.0)  # 东北办公楼
        env.add_entrance((3, 66), radius=1.2, flow_rate=2.5)   # 西南餐厅
        env.add_entrance((58, 66), radius=1.2, flow_rate=2.5)  # 东南银行
        
        # === 出口 (对应四个方向) ===
        env.add_exit((40, 2), radius=3.0)    # 北侧出口
        env.add_exit((40, 78), radius=3.0)   # 南侧出口
        env.add_exit((2, 40), radius=3.0)    # 西侧出口
        env.add_exit((78, 40), radius=3.0)   # 东侧出口
        
        return env
    
    @staticmethod
    def create_campus():
        """
        场景2：大学校园 (Campus)
        - 主干道 + 支路网络
        - 教学楼、宿舍、图书馆、食堂
        - 开阔绿地
        - 多个出入口
        - 人数：500-3000
        """
        env = Environment(width=120, height=100)
        
        # === 外围围墙 ===
        env.add_wall((0, 0), (120, 0))
        env.add_wall((120, 0), (120, 100))
        env.add_wall((120, 100), (0, 100))
        env.add_wall((0, 100), (0, 0))
        
        # === 主干道 (横竖交叉) ===
        # 主干道边界形成道路
        # 横向主干道 (中间)
        env.add_wall((0, 48), (120, 48))
        env.add_wall((0, 52), (120, 52))
        
        # 纵向主干道 (中间)
        env.add_wall((58, 0), (58, 100))
        env.add_wall((62, 0), (62, 100))
        
        # === 建筑物 ===
        # 左上：教学楼A
        env.add_wall((10, 10), (45, 10))
        env.add_wall((45, 10), (45, 40))
        env.add_wall((45, 40), (10, 40))
        env.add_wall((10, 40), (10, 10))
        # 入口
        env.add_wall((10, 20), (10, 25))  # 留出入口
        
        # 右上：教学楼B
        env.add_wall((70, 10), (110, 10))
        env.add_wall((110, 10), (110, 40))
        env.add_wall((110, 40), (70, 40))
        env.add_wall((70, 40), (70, 10))
        env.add_wall((70, 20), (70, 25))  # 留出入口
        
        # 左下：宿舍楼
        env.add_wall((10, 60), (45, 60))
        env.add_wall((45, 60), (45, 90))
        env.add_wall((45, 90), (10, 90))
        env.add_wall((10, 90), (10, 60))
        env.add_wall((10, 70), (10, 75))  # 入口
        
        # 右下：图书馆
        env.add_wall((70, 60), (110, 60))
        env.add_wall((110, 60), (110, 90))
        env.add_wall((110, 90), (70, 90))
        env.add_wall((70, 90), (70, 60))
        env.add_wall((90, 60), (95, 60))  # 入口
        
        # 中央：食堂
        env.add_wall((50, 30), (68, 30))
        env.add_wall((68, 30), (68, 45))
        env.add_wall((68, 45), (50, 45))
        env.add_wall((50, 45), (50, 30))
        
        # === 出入口 ===
        # 校门 (多个)
        env.add_entrance((60, 2), radius=3.0, flow_rate=10.0)    # 正门
        env.add_entrance((2, 50), radius=2.0, flow_rate=5.0)     # 西门
        env.add_entrance((118, 50), radius=2.0, flow_rate=5.0)   # 东门
        env.add_entrance((60, 98), radius=2.0, flow_rate=3.0)    # 后门
        
        # 教学楼门口 (作为中间目的地)
        env.add_entrance((8, 25), radius=1.5, flow_rate=6.0)     # 教学楼A
        env.add_entrance((68, 25), radius=1.5, flow_rate=6.0)    # 教学楼B
        env.add_entrance((8, 75), radius=1.5, flow_rate=4.0)     # 宿舍
        env.add_entrance((92, 58), radius=1.5, flow_rate=5.0)    # 图书馆
        env.add_entrance((59, 28), radius=2.0, flow_rate=7.0)    # 食堂
        
        # 出口
        env.add_exit((60, 2), radius=3.0)     # 正门出口
        env.add_exit((2, 50), radius=2.5)     # 西门出口
        env.add_exit((118, 50), radius=2.5)   # 东门出口
        env.add_exit((60, 98), radius=2.5)    # 后门出口
        
        return env
    
    @staticmethod
    def create_hospital():
        """
        场景3：医院 (Hospital)
        - 多栋建筑：急诊楼、住院楼、门诊楼
        - 连接通道
        - 救护车通道
        - 人数：500-1000
        """
        env = Environment(width=90, height=80)
        
        # === 外围边界 ===
        env.add_wall((0, 0), (90, 0))
        env.add_wall((90, 0), (90, 80))
        env.add_wall((90, 80), (0, 80))
        env.add_wall((0, 80), (0, 0))
        
        # === 急诊楼 (左下) ===
        env.add_wall((5, 50), (30, 50))
        env.add_wall((30, 50), (30, 75))
        env.add_wall((30, 75), (5, 75))
        env.add_wall((5, 75), (5, 50))
        # 急诊入口 (留空)
        env.add_wall((5, 58), (5, 62))
        
        # === 门诊楼 (中上) ===
        env.add_wall((35, 10), (70, 10))
        env.add_wall((70, 10), (70, 40))
        env.add_wall((70, 40), (35, 40))
        env.add_wall((35, 40), (35, 10))
        # 门诊大厅入口
        env.add_wall((50, 10), (55, 10))
        
        # === 住院楼 (右下) ===
        env.add_wall((60, 50), (85, 50))
        env.add_wall((85, 50), (85, 75))
        env.add_wall((85, 75), (60, 75))
        env.add_wall((60, 75), (60, 50))
        # 住院部入口
        env.add_wall((70, 50), (75, 50))
        
        # === 连接通道 ===
        # 急诊楼到门诊楼
        env.add_wall((30, 45), (35, 45))
        env.add_wall((30, 47), (35, 47))
        
        # 门诊楼到住院楼
        env.add_wall((70, 45), (60, 45))
        env.add_wall((70, 47), (60, 47))
        
        # === 救护车通道 (保持开放) ===
        env.add_wall((0, 60), (5, 60))
        env.add_wall((0, 65), (5, 65))
        
        # === 障碍物 (花坛、座椅) ===
        obstacles = [(15, 15), (20, 20), (75, 20), (15, 35), (40, 60)]
        for ox, oy in obstacles:
            env.add_wall((ox, oy), (ox + 1, oy))
            env.add_wall((ox + 1, oy), (ox + 1, oy + 1))
            env.add_wall((ox + 1, oy + 1), (ox, oy + 1))
            env.add_wall((ox, oy + 1), (ox, oy))
        
        # === 出入口 ===
        # 急诊入口 (高流量)
        env.add_entrance((3, 60), radius=2.0, flow_rate=5.0)
        
        # 正门 (门诊)
        env.add_entrance((52, 8), radius=2.5, flow_rate=6.0)
        
        # 住院部入口
        env.add_entrance((72, 48), radius=1.5, flow_rate=3.0)
        
        # 后勤入口
        env.add_entrance((88, 40), radius=1.5, flow_rate=2.0)
        
        # 出口
        env.add_exit((52, 8), radius=2.5)     # 正门出口
        env.add_exit((3, 60), radius=2.0)     # 急诊出口
        env.add_exit((88, 62), radius=2.0)    # 侧门出口
        env.add_exit((45, 78), radius=2.0)    # 后门出口
        
        return env
    
    @staticmethod
    def create_shopping_mall():
        """
        场景4：购物中心 (Shopping Mall)
        - 多层结构 (简化为单层大空间)
        - 商铺、主通道、休息区
        - 中庭区域
        - 人数：1000-5000
        """
        env = Environment(width=100, height=80)
        
        # === 外围墙体 ===
        env.add_wall((0, 0), (100, 0))
        env.add_wall((100, 0), (100, 80))
        env.add_wall((100, 80), (0, 80))
        env.add_wall((0, 80), (0, 0))
        
        # === 中庭区域 (中央开放空间) ===
        env.add_wall((35, 25), (65, 25))
        env.add_wall((65, 25), (65, 55))
        env.add_wall((65, 55), (35, 55))
        env.add_wall((35, 55), (35, 25))
        
        # === 商铺 (围绕中庭布置) ===
        # 左侧商铺
        shops_left = [
            (5, 10, 20, 15),   # (x, y, width, height)
            (5, 20, 20, 15),
            (5, 40, 20, 15),
            (5, 60, 20, 15)
        ]
        for x, y, w, h in shops_left:
            env.add_wall((x, y), (x + w, y))
            env.add_wall((x + w, y), (x + w, y + h))
            env.add_wall((x + w, y + h), (x, y + h))
            env.add_wall((x, y + h), (x, y))
            # 留出入口 (中间)
            env.add_wall((x, y + h//2 - 1), (x, y + h//2 + 1))
        
        # 右侧商铺
        shops_right = [
            (75, 10, 20, 15),
            (75, 20, 20, 15),
            (75, 40, 20, 15),
            (75, 60, 20, 15)
        ]
        for x, y, w, h in shops_right:
            env.add_wall((x, y), (x + w, y))
            env.add_wall((x + w, y), (x + w, y + h))
            env.add_wall((x + w, y + h), (x, y + h))
            env.add_wall((x, y + h), (x, y))
            env.add_wall((x + w, y + h//2 - 1), (x + w, y + h//2 + 1))
        
        # 上侧商铺
        env.add_wall((30, 5), (45, 5))
        env.add_wall((45, 5), (45, 18))
        env.add_wall((45, 18), (30, 18))
        env.add_wall((30, 18), (30, 5))
        
        env.add_wall((55, 5), (70, 5))
        env.add_wall((70, 5), (70, 18))
        env.add_wall((70, 18), (55, 18))
        env.add_wall((55, 18), (55, 5))
        
        # === 休息区 (座椅) ===
        rest_areas = [(40, 35), (55, 35), (40, 45), (55, 45)]
        for rx, ry in rest_areas:
            env.add_wall((rx, ry), (rx + 2, ry))
            env.add_wall((rx + 2, ry), (rx + 2, ry + 2))
            env.add_wall((rx + 2, ry + 2), (rx, ry + 2))
            env.add_wall((rx, ry + 2), (rx, ry))
        
        # === 出入口 ===
        # 主门
        env.add_entrance((50, 2), radius=3.0, flow_rate=15.0)
        
        # 停车场入口 (侧面)
        env.add_entrance((2, 40), radius=2.5, flow_rate=8.0)
        env.add_entrance((98, 40), radius=2.5, flow_rate=8.0)
        
        # 后门
        env.add_entrance((50, 78), radius=2.0, flow_rate=5.0)
        
        # 商铺入口 (部分作为源点)
        env.add_entrance((15, 12), radius=1.0, flow_rate=3.0)
        env.add_entrance((85, 30), radius=1.0, flow_rate=3.0)
        env.add_entrance((37, 7), radius=1.0, flow_rate=2.0)
        
        # 出口 (多个疏散口)
        env.add_exit((50, 2), radius=3.5)      # 主门
        env.add_exit((2, 40), radius=3.0)      # 西侧
        env.add_exit((98, 40), radius=3.0)     # 东侧
        env.add_exit((50, 78), radius=2.5)     # 后门
        env.add_exit((10, 5), radius=2.0)      # 安全通道1
        env.add_exit((90, 5), radius=2.0)      # 安全通道2
        env.add_exit((10, 75), radius=2.0)     # 安全通道3
        env.add_exit((90, 75), radius=2.0)     # 安全通道4
        
        return env
    
    @staticmethod
    def create_urban_park():
        """
        场景5：城市公园 (Urban Park)
        - 开放空间 + 小径网络
        - 湖泊、树木
        - 环形路径
        - 活动区
        - 人数：500-2000
        """
        env = Environment(width=100, height=100)
        
        # === 外围围栏 ===
        env.add_wall((0, 0), (100, 0))
        env.add_wall((100, 0), (100, 100))
        env.add_wall((100, 100), (0, 100))
        env.add_wall((0, 100), (0, 0))
        
        # === 中央湖泊 (不规则形状) ===
        # 湖泊边界
        lake_points = [
            (40, 40), (45, 35), (55, 35), (60, 40),
            (60, 50), (55, 55), (45, 55), (40, 50)
        ]
        for i in range(len(lake_points)):
            p1 = lake_points[i]
            p2 = lake_points[(i + 1) % len(lake_points)]
            env.add_wall(p1, p2)
        
        # === 树木 (散布) ===
        trees = [
            (10, 10), (15, 12), (20, 8), (25, 15),
            (80, 10), (85, 15), (90, 12),
            (10, 80), (15, 85), (20, 90),
            (80, 80), (85, 85), (90, 88),
            (30, 70), (70, 70), (30, 30), (70, 30),
            (15, 50), (85, 50), (50, 15), (50, 85)
        ]
        for tx, ty in trees:
            # 树木用圆形障碍表示 (简化为小方块)
            env.add_wall((tx, ty), (tx + 1, ty))
            env.add_wall((tx + 1, ty), (tx + 1, ty + 1))
            env.add_wall((tx + 1, ty + 1), (tx, ty + 1))
            env.add_wall((tx, ty + 1), (tx, ty))
        
        # === 活动舞台 (中心区域偏上) ===
        env.add_wall((45, 15), (55, 15))
        env.add_wall((55, 15), (55, 25))
        env.add_wall((55, 25), (45, 25))
        env.add_wall((45, 25), (45, 15))
        
        # === 餐车区 ===
        food_carts = [(65, 70), (70, 70), (75, 70)]
        for fx, fy in food_carts:
            env.add_wall((fx, fy), (fx + 2, fy))
            env.add_wall((fx + 2, fy), (fx + 2, fy + 2))
            env.add_wall((fx + 2, fy + 2), (fx, fy + 2))
            env.add_wall((fx, fy + 2), (fx, fy))
        
        # === 出入口 (5个公园大门) ===
        env.add_entrance((50, 2), radius=2.5, flow_rate=5.0)    # 北门
        env.add_entrance((2, 50), radius=2.5, flow_rate=4.0)    # 西门
        env.add_entrance((98, 50), radius=2.5, flow_rate=4.0)   # 东门
        env.add_entrance((25, 98), radius=2.0, flow_rate=3.0)   # 西南门
        env.add_entrance((75, 98), radius=2.0, flow_rate=3.0)   # 东南门
        
        # 活动区入口
        env.add_entrance((50, 13), radius=2.0, flow_rate=6.0)   # 舞台前
        
        # 出口
        env.add_exit((50, 2), radius=3.0)    # 北门
        env.add_exit((2, 50), radius=3.0)    # 西门
        env.add_exit((98, 50), radius=3.0)   # 东门
        env.add_exit((25, 98), radius=2.5)   # 西南门
        env.add_exit((75, 98), radius=2.5)   # 东南门
        
        return env


def generate_all_scenarios():
    """生成所有5个场景的配置文件"""
    import json
    
    scenarios = {
        'downtown_street': {
            'name': '繁忙街道 (Downtown Street)',
            'name_en': 'Downtown Street',
            'description': '双向马路，人行横道，公交站，地铁出口。人数500-1500，模拟交通信号异常、道路施工、火灾等突发事件。',
            'description_en': 'Busy street with crosswalks, bus stops, subway exits. 500-1500 pedestrians. Simulates traffic signal failures, road construction, fires.',
            'recommended_pedestrians': 1000,
            'environment': None
        },
        'campus': {
            'name': '大学校园 (Campus)',
            'name_en': 'University Campus',
            'description': '主干道网络，教学楼、宿舍、图书馆、食堂。人数500-3000，模拟上课高峰、火灾疏散、主门封闭。',
            'description_en': 'Campus with main roads, academic buildings, dorms, library, cafeteria. 500-3000 pedestrians. Simulates class rush, fire evacuation, gate closure.',
            'recommended_pedestrians': 2000,
            'environment': None
        },
        'hospital': {
            'name': '医院 (Hospital)',
            'name_en': 'Hospital',
            'description': '急诊楼、住院楼、门诊楼。人数500-1000，模拟火灾疏散、电梯停用、急救通道阻塞。',
            'description_en': 'Emergency, inpatient, outpatient buildings. 500-1000 pedestrians. Simulates fire evacuation, elevator failure, blocked emergency routes.',
            'recommended_pedestrians': 800,
            'environment': None
        },
        'shopping_mall': {
            'name': '购物中心 (Shopping Mall)',
            'name_en': 'Shopping Mall',
            'description': '多层商场，商铺、休息区、中庭。人数1000-5000，模拟火灾、扶梯停用、突发惊恐事件。',
            'description_en': 'Multi-level mall with shops, rest areas, atrium. 1000-5000 pedestrians. Simulates fire, escalator failure, panic events.',
            'recommended_pedestrians': 3000,
            'environment': None
        },
        'urban_park': {
            'name': '城市公园 (Urban Park)',
            'name_en': 'Urban Park',
            'description': '开放空间，湖泊、树木、活动区。人数500-2000，模拟活动结束大规模撤离、突发雷雨、恐慌事件。',
            'description_en': 'Open space with lake, trees, event area. 500-2000 pedestrians. Simulates mass exodus after events, sudden rain, panic.',
            'recommended_pedestrians': 1500,
            'environment': None
        }
    }
    
    # 创建每个场景
    generator = ScenarioGenerator()
    
    env1 = generator.create_downtown_street()
    scenarios['downtown_street']['environment'] = env1.to_dict()
    
    env2 = generator.create_campus()
    scenarios['campus']['environment'] = env2.to_dict()
    
    env3 = generator.create_hospital()
    scenarios['hospital']['environment'] = env3.to_dict()
    
    env4 = generator.create_shopping_mall()
    scenarios['shopping_mall']['environment'] = env4.to_dict()
    
    env5 = generator.create_urban_park()
    scenarios['urban_park']['environment'] = env5.to_dict()
    
    # 保存到文件
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'scenarios')
    os.makedirs(output_dir, exist_ok=True)
    
    for scenario_id, scenario_data in scenarios.items():
        filepath = os.path.join(output_dir, f'{scenario_id}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(scenario_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Created scenario: {filepath}")
    
    # 创建场景索引文件
    index = {
        'scenarios': [
            {
                'id': sid,
                'name': sdata['name'],
                'name_en': sdata['name_en'],
                'description': sdata['description'],
                'recommended_pedestrians': sdata['recommended_pedestrians']
            }
            for sid, sdata in scenarios.items()
        ]
    }
    
    index_path = os.path.join(output_dir, 'scenarios_index.json')
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Created scenario index: {index_path}")
    
    print(f"\n{'='*60}")
    print("所有5个场景已成功创建！")
    print("All 5 scenarios created successfully!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    generate_all_scenarios()
