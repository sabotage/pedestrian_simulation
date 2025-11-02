"""
行人运动模拟系统 - 核心模块
基于社会力模型(Social Force Model)
"""

from .pedestrian_model import (
    Pedestrian,
    PedestrianState,
    Obstacle,
    Exit,
    Event,
    EventType,
    SocialForceModel,
    SimulationEnvironment
)

__all__ = [
    'Pedestrian',
    'PedestrianState',
    'Obstacle',
    'Exit',
    'Event',
    'EventType',
    'SocialForceModel',
    'SimulationEnvironment'
]

__version__ = '1.0.0'
__author__ = 'Pedestrian Simulation Team'
