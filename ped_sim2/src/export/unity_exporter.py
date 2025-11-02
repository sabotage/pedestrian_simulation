"""
Unity VR export utilities for simulation data.
"""
import json
import numpy as np
from typing import List, Dict, Any
import os
from datetime import datetime


def convert_to_json_serializable(obj):
    """
    Convert NumPy types to JSON-serializable Python types.
    
    Args:
        obj: Object to convert
        
    Returns:
        JSON-serializable version of obj
    """
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_to_json_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_json_serializable(item) for item in obj]
    else:
        return obj


class UnityExporter:
    """Export simulation data in Unity-compatible format."""
    
    def __init__(self, output_dir: str = "exports"):
        """
        Initialize Unity exporter.
        
        Args:
            output_dir: Directory to save export files
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_simulation(self, simulator, filename: str = None) -> str:
        """
        Export complete simulation data for Unity VR.
        
        Args:
            simulator: Simulator instance with recorded data
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"simulation_{timestamp}.json"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Prepare export data
        export_data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'duration': float(simulator.time),
                'total_pedestrians': int(simulator.stats['spawned']),
                'frame_count': len(simulator.trajectory_data),
                'timestep': float(simulator.dt)
            },
            'environment': self._export_environment(simulator.environment),
            'trajectories': self._export_trajectories(simulator.trajectory_data),
            'events': self._export_events(simulator.event_manager.get_event_log()),
            'statistics': convert_to_json_serializable(simulator.stats)
        }
        
        # Convert all NumPy types to JSON-serializable types
        export_data = convert_to_json_serializable(export_data)
        
        # Write to file
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Simulation exported to: {filepath}")
        return filepath
    
    def _export_environment(self, environment) -> dict:
        """Export environment geometry."""
        return {
            'dimensions': {
                'width': float(environment.width),
                'height': float(environment.height)
            },
            'walls': [
                {
                    'start': {'x': float(w[0][0]), 'y': 0.0, 'z': float(w[0][1])},
                    'end': {'x': float(w[1][0]), 'y': 0.0, 'z': float(w[1][1])},
                    'height': 3.0  # Default wall height for Unity
                }
                for w in environment.walls
            ],
            'entrances': [
                {
                    'position': {'x': float(e['position'][0]), 'y': 0.0, 'z': float(e['position'][1])},
                    'radius': float(e['radius']),
                    'active': bool(e['active'])
                }
                for e in environment.entrances
            ],
            'exits': [
                {
                    'position': {'x': float(e['position'][0]), 'y': 0.0, 'z': float(e['position'][1])},
                    'radius': float(e['radius']),
                    'active': bool(e['active'])
                }
                for e in environment.exits
            ],
            'hazards': [
                {
                    'position': {'x': float(h['position'][0]), 'y': 0.0, 'z': float(h['position'][1])},
                    'radius': float(h['radius']),
                    'type': str(h['type']),
                    'intensity': float(h['intensity'])
                }
                for h in environment.hazard_zones
            ]
        }
    
    def _export_trajectories(self, trajectory_data: List[dict]) -> List[dict]:
        """Export pedestrian trajectories."""
        # Reorganize by pedestrian ID for easier Unity consumption
        pedestrian_trajectories = {}
        
        for frame in trajectory_data:
            for ped in frame['pedestrians']:
                ped_id = int(ped['id'])
                if ped_id not in pedestrian_trajectories:
                    pedestrian_trajectories[ped_id] = {
                        'id': ped_id,
                        'keyframes': []
                    }
                
                # Convert to Unity coordinate system (Y is up)
                pedestrian_trajectories[ped_id]['keyframes'].append({
                    'time': float(frame['time']),
                    'position': {
                        'x': float(ped['position'][0]),
                        'y': 0.9,  # Average pedestrian height
                        'z': float(ped['position'][1])
                    },
                    'velocity': {
                        'x': float(ped['velocity'][0]),
                        'y': 0.0,
                        'z': float(ped['velocity'][1])
                    },
                    'panic_level': float(ped['panic_level'])
                })
        
        return list(pedestrian_trajectories.values())
    
    def _export_events(self, event_log: List[dict]) -> List[dict]:
        """Export event timeline."""
        return [
            {
                'time': float(event['time']),
                'type': str(event['event']['type']),
                'parameters': convert_to_json_serializable(event['event']['parameters'])
            }
            for event in event_log
        ]
    
    def export_unity_scene_template(self, filename: str = "scene_template.txt") -> str:
        """
        Export a C# script template for Unity integration.
        
        Args:
            filename: Output filename
            
        Returns:
            Path to exported file
        """
        filepath = os.path.join(self.output_dir, filename)
        
        template = """using UnityEngine;
using System.Collections.Generic;
using System.IO;

public class PedestrianSimulationPlayer : MonoBehaviour
{
    [System.Serializable]
    public class SimulationData
    {
        public Metadata metadata;
        public Environment environment;
        public List<PedestrianTrajectory> trajectories;
        public List<SimEvent> events;
    }
    
    [System.Serializable]
    public class Metadata
    {
        public string export_time;
        public float duration;
        public int total_pedestrians;
        public int frame_count;
        public float timestep;
    }
    
    [System.Serializable]
    public class Environment
    {
        public Dimensions dimensions;
        public List<Wall> walls;
        public List<Zone> entrances;
        public List<Zone> exits;
        public List<Hazard> hazards;
    }
    
    [System.Serializable]
    public class Dimensions
    {
        public float width;
        public float height;
    }
    
    [System.Serializable]
    public class Wall
    {
        public Vector3Data start;
        public Vector3Data end;
        public float height;
    }
    
    [System.Serializable]
    public class Zone
    {
        public Vector3Data position;
        public float radius;
        public bool active;
    }
    
    [System.Serializable]
    public class Hazard
    {
        public Vector3Data position;
        public float radius;
        public string type;
        public float intensity;
    }
    
    [System.Serializable]
    public class Vector3Data
    {
        public float x, y, z;
        public Vector3 ToVector3() => new Vector3(x, y, z);
    }
    
    [System.Serializable]
    public class PedestrianTrajectory
    {
        public int id;
        public List<Keyframe> keyframes;
    }
    
    [System.Serializable]
    public class Keyframe
    {
        public float time;
        public Vector3Data position;
        public Vector3Data velocity;
        public float panic_level;
    }
    
    [System.Serializable]
    public class SimEvent
    {
        public float time;
        public string type;
    }
    
    public string simulationDataPath;
    public GameObject pedestrianPrefab;
    public GameObject wallPrefab;
    public float playbackSpeed = 1.0f;
    
    private SimulationData simData;
    private Dictionary<int, GameObject> pedestrianObjects = new Dictionary<int, GameObject>();
    private float currentTime = 0f;
    private bool isPlaying = false;
    
    void Start()
    {
        LoadSimulationData();
        BuildEnvironment();
    }
    
    void LoadSimulationData()
    {
        string jsonData = File.ReadAllText(simulationDataPath);
        simData = JsonUtility.FromJson<SimulationData>(jsonData);
    }
    
    void BuildEnvironment()
    {
        // Create walls
        foreach (var wall in simData.environment.walls)
        {
            Vector3 start = wall.start.ToVector3();
            Vector3 end = wall.end.ToVector3();
            Vector3 center = (start + end) / 2;
            float length = Vector3.Distance(start, end);
            
            GameObject wallObj = Instantiate(wallPrefab, center, Quaternion.identity);
            wallObj.transform.localScale = new Vector3(0.2f, wall.height, length);
            wallObj.transform.LookAt(end);
        }
    }
    
    void Update()
    {
        if (!isPlaying) return;
        
        currentTime += Time.deltaTime * playbackSpeed;
        
        foreach (var trajectory in simData.trajectories)
        {
            UpdatePedestrian(trajectory);
        }
    }
    
    void UpdatePedestrian(PedestrianTrajectory trajectory)
    {
        // Find current keyframe
        Keyframe current = null, next = null;
        
        for (int i = 0; i < trajectory.keyframes.Count - 1; i++)
        {
            if (trajectory.keyframes[i].time <= currentTime && 
                trajectory.keyframes[i + 1].time >= currentTime)
            {
                current = trajectory.keyframes[i];
                next = trajectory.keyframes[i + 1];
                break;
            }
        }
        
        if (current == null) return;
        
        // Create pedestrian if doesn't exist
        if (!pedestrianObjects.ContainsKey(trajectory.id))
        {
            GameObject ped = Instantiate(pedestrianPrefab);
            pedestrianObjects[trajectory.id] = ped;
        }
        
        // Interpolate position
        float t = (currentTime - current.time) / (next.time - current.time);
        Vector3 position = Vector3.Lerp(
            current.position.ToVector3(),
            next.position.ToVector3(),
            t
        );
        
        pedestrianObjects[trajectory.id].transform.position = position;
    }
    
    public void Play() => isPlaying = true;
    public void Pause() => isPlaying = false;
    public void Reset() => currentTime = 0f;
}
"""
        
        with open(filepath, 'w') as f:
            f.write(template)
        
        print(f"Unity script template exported to: {filepath}")
        return filepath
