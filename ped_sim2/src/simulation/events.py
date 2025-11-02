"""
Emergency event system for dynamic scenario changes.
"""
import numpy as np
from typing import List, Dict, Callable
from enum import Enum


class EventType(Enum):
    """Types of emergency events."""
    FIRE = "fire"
    SHOOTING = "shooting"
    ENTRANCE_BLOCKED = "entrance_blocked"
    ENTRANCE_OPENED = "entrance_opened"
    EXIT_BLOCKED = "exit_blocked"
    EXIT_OPENED = "exit_opened"
    OBSTACLE_ADDED = "obstacle_added"
    OBSTACLE_REMOVED = "obstacle_removed"


class Event:
    """Represents a single emergency event."""
    
    def __init__(self, event_type: EventType, trigger_time: float, 
                 parameters: Dict = None):
        """
        Initialize an event.
        
        Args:
            event_type: Type of event
            trigger_time: Simulation time when event occurs (seconds)
            parameters: Event-specific parameters
        """
        self.event_type = event_type
        self.trigger_time = trigger_time
        self.parameters = parameters or {}
        self.triggered = False
    
    def to_dict(self) -> dict:
        """Convert event to dictionary."""
        return {
            'type': self.event_type.value,
            'trigger_time': self.trigger_time,
            'parameters': self.parameters,
            'triggered': self.triggered
        }


class EventManager:
    """Manages and triggers events during simulation."""
    
    def __init__(self):
        """Initialize event manager."""
        self.events = []
        self.event_log = []
        self.callbacks = {
            EventType.FIRE: [],
            EventType.SHOOTING: [],
            EventType.ENTRANCE_BLOCKED: [],
            EventType.ENTRANCE_OPENED: [],
            EventType.EXIT_BLOCKED: [],
            EventType.EXIT_OPENED: [],
            EventType.OBSTACLE_ADDED: [],
            EventType.OBSTACLE_REMOVED: []
        }
    
    def add_event(self, event: Event):
        """Add an event to the schedule."""
        self.events.append(event)
        # Sort by trigger time
        self.events.sort(key=lambda e: e.trigger_time)
    
    def schedule_fire(self, trigger_time: float, position: tuple, radius: float = 5.0):
        """
        Schedule a fire event.
        
        Args:
            trigger_time: When fire starts (seconds)
            position: Fire location (x, y)
            radius: Fire radius
        """
        event = Event(
            EventType.FIRE,
            trigger_time,
            {'position': position, 'radius': radius}
        )
        self.add_event(event)
    
    def schedule_shooting(self, trigger_time: float, position: tuple, radius: float = 10.0):
        """
        Schedule a shooting event.
        
        Args:
            trigger_time: When shooting occurs (seconds)
            position: Shooting location (x, y)
            radius: Panic radius
        """
        event = Event(
            EventType.SHOOTING,
            trigger_time,
            {'position': position, 'radius': radius}
        )
        self.add_event(event)
    
    def schedule_entrance_closure(self, trigger_time: float, entrance_idx: int):
        """
        Schedule entrance blocking.
        
        Args:
            trigger_time: When entrance closes (seconds)
            entrance_idx: Index of entrance to block
        """
        event = Event(
            EventType.ENTRANCE_BLOCKED,
            trigger_time,
            {'entrance_idx': entrance_idx}
        )
        self.add_event(event)
    
    def schedule_entrance_opening(self, trigger_time: float, entrance_idx: int):
        """
        Schedule entrance opening.
        
        Args:
            trigger_time: When entrance opens (seconds)
            entrance_idx: Index of entrance to open
        """
        event = Event(
            EventType.ENTRANCE_OPENED,
            trigger_time,
            {'entrance_idx': entrance_idx}
        )
        self.add_event(event)
    
    def schedule_exit_closure(self, trigger_time: float, exit_idx: int):
        """
        Schedule exit blocking.
        
        Args:
            trigger_time: When exit closes (seconds)
            exit_idx: Index of exit to block
        """
        event = Event(
            EventType.EXIT_BLOCKED,
            trigger_time,
            {'exit_idx': exit_idx}
        )
        self.add_event(event)
    
    def schedule_exit_opening(self, trigger_time: float, exit_idx: int):
        """
        Schedule exit opening.
        
        Args:
            trigger_time: When exit opens (seconds)
            exit_idx: Index of exit to open
        """
        event = Event(
            EventType.EXIT_OPENED,
            trigger_time,
            {'exit_idx': exit_idx}
        )
        self.add_event(event)
    
    def register_callback(self, event_type: EventType, callback: Callable):
        """
        Register a callback for an event type.
        
        Args:
            event_type: Type of event to listen for
            callback: Function to call when event triggers
        """
        self.callbacks[event_type].append(callback)
    
    def update(self, current_time: float):
        """
        Check and trigger events at current simulation time.
        
        Args:
            current_time: Current simulation time (seconds)
            
        Returns:
            List of triggered events
        """
        triggered_events = []
        
        for event in self.events:
            if not event.triggered and current_time >= event.trigger_time:
                event.triggered = True
                triggered_events.append(event)
                self.event_log.append({
                    'time': current_time,
                    'event': event.to_dict()
                })
                
                # Execute callbacks
                for callback in self.callbacks[event.event_type]:
                    callback(event)
        
        return triggered_events
    
    def clear_events(self):
        """Clear all scheduled events."""
        self.events = []
        self.event_log = []
    
    def get_event_log(self) -> List[dict]:
        """Get log of all triggered events."""
        return self.event_log
    
    def to_dict(self) -> dict:
        """Convert event manager state to dictionary."""
        return {
            'scheduled_events': [e.to_dict() for e in self.events],
            'event_log': self.event_log
        }
