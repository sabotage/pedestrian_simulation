using UnityEngine;
using UnityEngine.UI;
using TMPro;

/// <summary>
/// Unity UI控制面板
/// 用于控制仿真回放和显示统计信息
/// </summary>
public class SimulationUIController : MonoBehaviour
{
    [Header("引用")]
    public SimulationDataLoader dataLoader;
    
    [Header("UI元素 - 控制按钮")]
    public Button playButton;
    public Button pauseButton;
    public Button stopButton;
    public Button restartButton;
    
    [Header("UI元素 - 速度控制")]
    public Slider speedSlider;
    public TextMeshProUGUI speedText;
    
    [Header("UI元素 - 信息显示")]
    public TextMeshProUGUI timeText;
    public TextMeshProUGUI pedestrianCountText;
    public TextMeshProUGUI panicCountText;
    public TextMeshProUGUI averageSpeedText;
    
    [Header("UI元素 - 选项")]
    public Toggle showTrajectoriesToggle;
    public Slider sceneScaleSlider;
    
    void Start()
    {
        if (dataLoader == null)
        {
            dataLoader = FindObjectOfType<SimulationDataLoader>();
        }
        
        SetupButtons();
        SetupSliders();
        SetupToggles();
    }
    
    void Update()
    {
        UpdateStatistics();
    }
    
    /// <summary>
    /// 设置按钮事件
    /// </summary>
    void SetupButtons()
    {
        if (playButton != null)
        {
            playButton.onClick.AddListener(OnPlayClicked);
        }
        
        if (pauseButton != null)
        {
            pauseButton.onClick.AddListener(OnPauseClicked);
        }
        
        if (stopButton != null)
        {
            stopButton.onClick.AddListener(OnStopClicked);
        }
        
        if (restartButton != null)
        {
            restartButton.onClick.AddListener(OnRestartClicked);
        }
    }
    
    /// <summary>
    /// 设置滑块事件
    /// </summary>
    void SetupSliders()
    {
        if (speedSlider != null)
        {
            speedSlider.minValue = 0.1f;
            speedSlider.maxValue = 5.0f;
            speedSlider.value = 1.0f;
            speedSlider.onValueChanged.AddListener(OnSpeedChanged);
        }
        
        if (sceneScaleSlider != null)
        {
            sceneScaleSlider.minValue = 0.5f;
            sceneScaleSlider.maxValue = 3.0f;
            sceneScaleSlider.value = 1.0f;
            sceneScaleSlider.onValueChanged.AddListener(OnScaleChanged);
        }
    }
    
    /// <summary>
    /// 设置开关事件
    /// </summary>
    void SetupToggles()
    {
        if (showTrajectoriesToggle != null)
        {
            showTrajectoriesToggle.isOn = true;
            showTrajectoriesToggle.onValueChanged.AddListener(OnTrajectoriesToggled);
        }
    }
    
    /// <summary>
    /// 更新统计信息显示
    /// </summary>
    void UpdateStatistics()
    {
        if (dataLoader == null) return;
        
        // 这里需要从SimulationDataLoader获取当前统计信息
        // 可以添加一个GetCurrentStats()方法到SimulationDataLoader
        
        if (timeText != null)
        {
            // 示例：显示当前帧时间
            timeText.text = $"时间: {Time.time:F1}s";
        }
    }
    
    // 按钮回调
    void OnPlayClicked()
    {
        dataLoader?.Play();
        Debug.Log("播放仿真");
    }
    
    void OnPauseClicked()
    {
        dataLoader?.Pause();
        Debug.Log("暂停仿真");
    }
    
    void OnStopClicked()
    {
        dataLoader?.Stop();
        Debug.Log("停止仿真");
    }
    
    void OnRestartClicked()
    {
        dataLoader?.Restart();
        Debug.Log("重新开始");
    }
    
    void OnSpeedChanged(float value)
    {
        dataLoader?.SetPlaybackSpeed(value);
        
        if (speedText != null)
        {
            speedText.text = $"{value:F1}x";
        }
    }
    
    void OnScaleChanged(float value)
    {
        if (dataLoader != null)
        {
            dataLoader.sceneScale = value;
        }
    }
    
    void OnTrajectoriesToggled(bool isOn)
    {
        if (dataLoader != null)
        {
            dataLoader.showTrajectories = isOn;
        }
    }
}

/// <summary>
/// VR控制器交互
/// 用于在VR环境中控制仿真
/// </summary>
public class VRSimulationController : MonoBehaviour
{
    public SimulationDataLoader dataLoader;
    
    [Header("VR设置")]
    [Tooltip("使用的VR SDK (OVR/XR)")]
    public string vrSDK = "OVR";
    
    void Update()
    {
        // OculusVR示例
        if (vrSDK == "OVR")
        {
            // 右手控制器A键 - 播放/暂停
            if (OVRInput.GetDown(OVRInput.Button.One))
            {
                TogglePlayPause();
            }
            
            // 右手控制器B键 - 重启
            if (OVRInput.GetDown(OVRInput.Button.Two))
            {
                dataLoader?.Restart();
            }
            
            // 摇杆控制速度
            Vector2 thumbstick = OVRInput.Get(OVRInput.Axis2D.PrimaryThumbstick);
            if (Mathf.Abs(thumbstick.y) > 0.5f)
            {
                float currentSpeed = dataLoader.playbackSpeed;
                currentSpeed += thumbstick.y * 0.1f * Time.deltaTime;
                dataLoader?.SetPlaybackSpeed(currentSpeed);
            }
        }
        
        // Unity XR示例
        // 可以添加其他VR SDK的支持
    }
    
    bool isPlaying = false;
    
    void TogglePlayPause()
    {
        if (isPlaying)
        {
            dataLoader?.Pause();
        }
        else
        {
            dataLoader?.Play();
        }
        isPlaying = !isPlaying;
    }
}

/// <summary>
/// 相机控制器
/// 用于在VR中移动观察点
/// </summary>
public class SimulationCameraController : MonoBehaviour
{
    [Header("移动设置")]
    public float moveSpeed = 5.0f;
    public float rotateSpeed = 100.0f;
    public float zoomSpeed = 10.0f;
    
    [Header("视角预设")]
    public Transform[] presetViews;
    private int currentViewIndex = 0;
    
    void Update()
    {
        // 键盘控制（非VR模式）
        if (!Application.isEditor) return;
        
        // WASD移动
        float h = Input.GetAxis("Horizontal");
        float v = Input.GetAxis("Vertical");
        
        Vector3 movement = new Vector3(h, 0, v) * moveSpeed * Time.deltaTime;
        transform.Translate(movement, Space.World);
        
        // QE上下移动
        if (Input.GetKey(KeyCode.Q))
        {
            transform.Translate(Vector3.down * moveSpeed * Time.deltaTime, Space.World);
        }
        if (Input.GetKey(KeyCode.E))
        {
            transform.Translate(Vector3.up * moveSpeed * Time.deltaTime, Space.World);
        }
        
        // 鼠标右键旋转
        if (Input.GetMouseButton(1))
        {
            float mouseX = Input.GetAxis("Mouse X");
            float mouseY = Input.GetAxis("Mouse Y");
            
            transform.Rotate(Vector3.up, mouseX * rotateSpeed * Time.deltaTime, Space.World);
            transform.Rotate(Vector3.left, mouseY * rotateSpeed * Time.deltaTime, Space.Self);
        }
        
        // 数字键切换预设视角
        if (Input.GetKeyDown(KeyCode.Alpha1))
        {
            SwitchToPresetView(0);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha2))
        {
            SwitchToPresetView(1);
        }
        else if (Input.GetKeyDown(KeyCode.Alpha3))
        {
            SwitchToPresetView(2);
        }
    }
    
    void SwitchToPresetView(int index)
    {
        if (presetViews != null && index < presetViews.Length)
        {
            Transform target = presetViews[index];
            transform.position = target.position;
            transform.rotation = target.rotation;
            currentViewIndex = index;
        }
    }
    
    public void NextPresetView()
    {
        if (presetViews != null && presetViews.Length > 0)
        {
            currentViewIndex = (currentViewIndex + 1) % presetViews.Length;
            SwitchToPresetView(currentViewIndex);
        }
    }
}
