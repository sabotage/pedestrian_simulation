using System;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

/// <summary>
/// 行人仿真数据加载器 - 用于Unity VR项目
/// 将Python仿真导出的JSON数据加载到Unity场景中
/// </summary>
public class SimulationDataLoader : MonoBehaviour
{
    [Header("数据设置")]
    [Tooltip("仿真数据JSON文件路径")]
    public TextAsset simulationDataFile;
    
    [Header("预制体")]
    [Tooltip("行人预制体")]
    public GameObject pedestrianPrefab;
    
    [Tooltip("墙体材质")]
    public Material wallMaterial;
    
    [Tooltip("出口标识预制体")]
    public GameObject exitMarkerPrefab;
    
    [Header("可视化设置")]
    [Tooltip("正常状态颜色")]
    public Color normalColor = Color.green;
    
    [Tooltip("恐慌状态颜色")]
    public Color panicColor = Color.red;
    
    [Tooltip("疏散状态颜色")]
    public Color evacuatingColor = Color.yellow;
    
    [Tooltip("回放速度倍数")]
    [Range(0.1f, 5.0f)]
    public float playbackSpeed = 1.0f;
    
    [Tooltip("显示轨迹")]
    public bool showTrajectories = true;
    
    [Header("VR设置")]
    [Tooltip("场景缩放比例")]
    public float sceneScale = 1.0f;
    
    // 数据结构
    private SimulationData data;
    private Dictionary<int, GameObject> pedestrianObjects = new Dictionary<int, GameObject>();
    private Dictionary<int, LineRenderer> trajectoryLines = new Dictionary<int, LineRenderer>();
    private int currentFrame = 0;
    private float frameTimer = 0f;
    private bool isPlaying = false;
    
    void Start()
    {
        LoadSimulationData();
        SetupScene();
    }
    
    void Update()
    {
        if (isPlaying && data != null && data.frames.Count > 0)
        {
            frameTimer += Time.deltaTime * playbackSpeed;
            
            if (frameTimer >= data.metadata.dt)
            {
                frameTimer = 0f;
                UpdateFrame();
            }
        }
    }
    
    /// <summary>
    /// 加载仿真数据
    /// </summary>
    void LoadSimulationData()
    {
        if (simulationDataFile == null)
        {
            Debug.LogError("未指定仿真数据文件!");
            return;
        }
        
        try
        {
            string jsonText = simulationDataFile.text;
            data = JsonUtility.FromJson<SimulationData>(jsonText);
            Debug.Log($"成功加载仿真数据: {data.frames.Count} 帧");
        }
        catch (Exception e)
        {
            Debug.LogError($"加载仿真数据失败: {e.Message}");
        }
    }
    
    /// <summary>
    /// 设置场景元素
    /// </summary>
    void SetupScene()
    {
        if (data == null) return;
        
        // 创建墙体
        foreach (var obstacle in data.obstacles)
        {
            CreateWall(obstacle.vertices);
        }
        
        // 创建出口标识
        foreach (var exit in data.exits)
        {
            CreateExitMarker(exit.position, exit.width);
        }
        
        Debug.Log("场景设置完成");
    }
    
    /// <summary>
    /// 创建墙体
    /// </summary>
    void CreateWall(List<Vector2> vertices)
    {
        if (vertices.Count < 3) return;
        
        GameObject wallObj = new GameObject("Wall");
        wallObj.transform.parent = transform;
        
        // 创建3D墙体
        MeshFilter meshFilter = wallObj.AddComponent<MeshFilter>();
        MeshRenderer meshRenderer = wallObj.AddComponent<MeshRenderer>();
        
        Mesh mesh = new Mesh();
        
        // 将2D顶点转换为3D (添加高度)
        float wallHeight = 3.0f;
        Vector3[] vertices3D = new Vector3[vertices.Count * 2];
        
        for (int i = 0; i < vertices.Count; i++)
        {
            Vector2 v = vertices[i] * sceneScale;
            vertices3D[i] = new Vector3(v.x, 0, v.y);
            vertices3D[i + vertices.Count] = new Vector3(v.x, wallHeight, v.y);
        }
        
        // 创建三角形
        List<int> triangles = new List<int>();
        for (int i = 0; i < vertices.Count; i++)
        {
            int next = (i + 1) % vertices.Count;
            
            // 墙面
            triangles.Add(i);
            triangles.Add(i + vertices.Count);
            triangles.Add(next);
            
            triangles.Add(next);
            triangles.Add(i + vertices.Count);
            triangles.Add(next + vertices.Count);
        }
        
        mesh.vertices = vertices3D;
        mesh.triangles = triangles.ToArray();
        mesh.RecalculateNormals();
        
        meshFilter.mesh = mesh;
        
        if (wallMaterial != null)
        {
            meshRenderer.material = wallMaterial;
        }
        
        // 添加碰撞体
        wallObj.AddComponent<MeshCollider>();
    }
    
    /// <summary>
    /// 创建出口标识
    /// </summary>
    void CreateExitMarker(Vector2 position, float width)
    {
        if (exitMarkerPrefab == null)
        {
            // 使用简单的立方体作为出口标识
            GameObject marker = GameObject.CreatePrimitive(PrimitiveType.Cube);
            marker.name = "Exit";
            marker.transform.parent = transform;
            marker.transform.position = new Vector3(position.x * sceneScale, 0.5f, position.y * sceneScale);
            marker.transform.localScale = new Vector3(width * sceneScale, 1f, 0.5f);
            
            Renderer renderer = marker.GetComponent<Renderer>();
            renderer.material.color = Color.cyan;
            
            // 添加发光效果
            renderer.material.EnableKeyword("_EMISSION");
            renderer.material.SetColor("_EmissionColor", Color.cyan * 0.5f);
        }
        else
        {
            GameObject marker = Instantiate(exitMarkerPrefab, transform);
            marker.transform.position = new Vector3(position.x * sceneScale, 0, position.y * sceneScale);
        }
    }
    
    /// <summary>
    /// 更新当前帧
    /// </summary>
    void UpdateFrame()
    {
        if (currentFrame >= data.frames.Count)
        {
            isPlaying = false;
            Debug.Log("仿真回放完成");
            return;
        }
        
        FrameData frame = data.frames[currentFrame];
        
        // 更新现有行人，移除已离开的行人
        List<int> existingIds = new List<int>(pedestrianObjects.Keys);
        HashSet<int> currentIds = new HashSet<int>();
        
        foreach (var pedData in frame.pedestrians)
        {
            currentIds.Add(pedData.id);
            
            if (!pedestrianObjects.ContainsKey(pedData.id))
            {
                // 创建新行人
                CreatePedestrian(pedData.id);
            }
            
            // 更新行人位置和状态
            UpdatePedestrian(pedData);
        }
        
        // 移除已离开场景的行人
        foreach (int id in existingIds)
        {
            if (!currentIds.Contains(id))
            {
                RemovePedestrian(id);
            }
        }
        
        currentFrame++;
    }
    
    /// <summary>
    /// 创建行人对象
    /// </summary>
    void CreatePedestrian(int id)
    {
        GameObject ped;
        
        if (pedestrianPrefab != null)
        {
            ped = Instantiate(pedestrianPrefab, transform);
        }
        else
        {
            // 使用简单的胶囊体
            ped = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            ped.transform.localScale = new Vector3(0.6f, 0.9f, 0.6f) * sceneScale;
        }
        
        ped.name = $"Pedestrian_{id}";
        pedestrianObjects[id] = ped;
        
        // 添加轨迹线
        if (showTrajectories)
        {
            LineRenderer lineRenderer = ped.AddComponent<LineRenderer>();
            lineRenderer.startWidth = 0.05f * sceneScale;
            lineRenderer.endWidth = 0.05f * sceneScale;
            lineRenderer.material = new Material(Shader.Find("Sprites/Default"));
            lineRenderer.positionCount = 0;
            trajectoryLines[id] = lineRenderer;
        }
    }
    
    /// <summary>
    /// 更新行人状态
    /// </summary>
    void UpdatePedestrian(PedestrianData pedData)
    {
        GameObject ped = pedestrianObjects[pedData.id];
        
        // 更新位置
        Vector3 newPos = new Vector3(
            pedData.position[0] * sceneScale,
            0.9f * sceneScale,
            pedData.position[1] * sceneScale
        );
        ped.transform.position = newPos;
        
        // 更新朝向
        if (pedData.velocity[0] != 0 || pedData.velocity[1] != 0)
        {
            Vector3 direction = new Vector3(pedData.velocity[0], 0, pedData.velocity[1]);
            ped.transform.rotation = Quaternion.LookRotation(direction);
        }
        
        // 更新颜色
        Renderer renderer = ped.GetComponent<Renderer>();
        if (renderer != null)
        {
            Color color = normalColor;
            
            switch (pedData.state)
            {
                case "panic":
                    color = panicColor;
                    break;
                case "evacuating":
                    color = evacuatingColor;
                    break;
            }
            
            // 根据恐慌程度调整颜色
            color = Color.Lerp(normalColor, panicColor, pedData.panic_level);
            renderer.material.color = color;
        }
        
        // 更新轨迹
        if (showTrajectories && trajectoryLines.ContainsKey(pedData.id))
        {
            LineRenderer line = trajectoryLines[pedData.id];
            line.positionCount++;
            line.SetPosition(line.positionCount - 1, newPos);
            line.startColor = renderer.material.color;
            line.endColor = renderer.material.color;
        }
    }
    
    /// <summary>
    /// 移除行人
    /// </summary>
    void RemovePedestrian(int id)
    {
        if (pedestrianObjects.ContainsKey(id))
        {
            Destroy(pedestrianObjects[id]);
            pedestrianObjects.Remove(id);
        }
        
        if (trajectoryLines.ContainsKey(id))
        {
            trajectoryLines.Remove(id);
        }
    }
    
    // 公共控制方法
    public void Play()
    {
        isPlaying = true;
    }
    
    public void Pause()
    {
        isPlaying = false;
    }
    
    public void Stop()
    {
        isPlaying = false;
        currentFrame = 0;
        ClearAllPedestrians();
    }
    
    public void Restart()
    {
        Stop();
        Play();
    }
    
    public void SetPlaybackSpeed(float speed)
    {
        playbackSpeed = Mathf.Clamp(speed, 0.1f, 5.0f);
    }
    
    void ClearAllPedestrians()
    {
        foreach (var ped in pedestrianObjects.Values)
        {
            Destroy(ped);
        }
        pedestrianObjects.Clear();
        trajectoryLines.Clear();
    }
}

// 数据结构定义
[Serializable]
public class SimulationData
{
    public Metadata metadata;
    public List<ObstacleData> obstacles;
    public List<ExitData> exits;
    public List<FrameData> frames;
}

[Serializable]
public class Metadata
{
    public float width;
    public float height;
    public float total_time;
    public float dt;
}

[Serializable]
public class ObstacleData
{
    public List<Vector2> vertices;
}

[Serializable]
public class ExitData
{
    public Vector2 position;
    public float width;
}

[Serializable]
public class FrameData
{
    public float time;
    public List<PedestrianData> pedestrians;
}

[Serializable]
public class PedestrianData
{
    public int id;
    public float[] position;
    public float[] velocity;
    public string state;
    public float panic_level;
}
