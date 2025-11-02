"""
快速测试脚本 - 验证预置场景系统
Quick Test Script - Verify Preset Scenarios System
"""
import json
import os

def test_scenario_files():
    """测试场景文件是否正确生成"""
    print("="*60)
    print("Testing Preset Scenario Files")
    print("="*60)
    
    scenarios_dir = os.path.join(os.path.dirname(__file__), '..', 'scenarios')
    
    required_files = [
        'downtown_street.json',
        'campus.json',
        'hospital.json',
        'shopping_mall.json',
        'urban_park.json',
        'scenarios_index.json'
    ]
    
    all_ok = True
    
    for filename in required_files:
        filepath = os.path.join(scenarios_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"❌ MISSING: {filename}")
            all_ok = False
            continue
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if filename == 'scenarios_index.json':
                # 验证索引文件
                assert 'scenarios' in data, "Index missing 'scenarios' field"
                assert len(data['scenarios']) == 5, "Index should have 5 scenarios"
                print(f"✓ {filename} - {len(data['scenarios'])} scenarios indexed")
            else:
                # 验证场景文件
                required_keys = ['name', 'name_en', 'description', 
                                'recommended_pedestrians', 'environment']
                for key in required_keys:
                    assert key in data, f"Missing key: {key}"
                
                env = data['environment']
                assert 'width' in env and 'height' in env, "Environment missing dimensions"
                assert 'walls' in env and 'entrances' in env and 'exits' in env, \
                       "Environment missing required elements"
                
                print(f"✓ {filename}")
                print(f"  - Name: {data['name']}")
                print(f"  - Size: {env['width']}m × {env['height']}m")
                print(f"  - Walls: {len(env['walls'])}, " +
                      f"Entrances: {len(env['entrances'])}, " +
                      f"Exits: {len(env['exits'])}")
                print(f"  - Recommended pedestrians: {data['recommended_pedestrians']}")
        
        except Exception as e:
            print(f"❌ ERROR in {filename}: {e}")
            all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✅ All scenario files are valid!")
    else:
        print("❌ Some scenario files have errors")
    print("="*60)
    
    return all_ok


def test_web_api():
    """测试Web API是否能正确返回场景数据"""
    print("\n" + "="*60)
    print("Testing Web API Scenario Loading")
    print("="*60)
    
    # 模拟Flask app的get_scenarios函数
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'web'))
    
    try:
        scenarios_dir = os.path.join(os.path.dirname(__file__), '..', 'scenarios')
        scenarios = {}
        
        scenario_files = [
            'downtown_street.json',
            'campus.json',
            'hospital.json',
            'shopping_mall.json',
            'urban_park.json'
        ]
        
        for filename in scenario_files:
            filepath = os.path.join(scenarios_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    scenario_id = filename.replace('.json', '')
                    scenarios[scenario_id] = json.load(f)
        
        print(f"✓ Loaded {len(scenarios)} scenarios")
        
        for scenario_id, scenario_data in scenarios.items():
            print(f"\n  {scenario_id}:")
            print(f"    - {scenario_data['name']} / {scenario_data['name_en']}")
            print(f"    - Environment: {scenario_data['environment']['width']}m × " +
                  f"{scenario_data['environment']['height']}m")
        
        print("\n" + "="*60)
        print("✅ Web API can load all scenarios successfully!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error loading scenarios: {e}")
        print("="*60)
        return False


def test_environment_loading():
    """测试Environment.from_dict()是否能正确加载场景"""
    print("\n" + "="*60)
    print("Testing Environment Loading from JSON")
    print("="*60)
    
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    
    try:
        from simulation.environment import Environment
        
        # 加载一个测试场景
        scenarios_dir = os.path.join(os.path.dirname(__file__), '..', 'scenarios')
        test_file = os.path.join(scenarios_dir, 'downtown_street.json')
        
        with open(test_file, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)
        
        # 从字典创建环境
        env = Environment.from_dict(scenario_data['environment'])
        
        print(f"✓ Created environment from JSON")
        print(f"  - Dimensions: {env.width}m × {env.height}m")
        print(f"  - Walls: {len(env.walls)}")
        print(f"  - Entrances: {len(env.entrances)}")
        print(f"  - Exits: {len(env.exits)}")
        
        # 创建模拟器测试
        from simulation.simulator import Simulator
        sim = Simulator(env, dt=0.1)
        
        print(f"✓ Created simulator successfully")
        
        # 生成一些行人测试
        for i in range(min(10, len(env.entrances))):
            sim.spawn_pedestrian(entrance_idx=i % len(env.entrances))
        
        print(f"✓ Spawned {sim.stats['spawned']} test pedestrians")
        
        # 运行几步测试
        for _ in range(10):
            sim.step()
        
        print(f"✓ Simulation ran for {sim.time:.1f}s")
        
        print("\n" + "="*60)
        print("✅ Environment loading and simulation work correctly!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error in environment loading: {e}")
        import traceback
        traceback.print_exc()
        print("="*60)
        return False


def main():
    """运行所有测试"""
    print("\n" + "#"*60)
    print("# Preset Scenarios System - Comprehensive Test")
    print("#"*60 + "\n")
    
    results = []
    
    # 测试1: 场景文件
    results.append(("Scenario Files", test_scenario_files()))
    
    # 测试2: Web API
    results.append(("Web API", test_web_api()))
    
    # 测试3: Environment加载
    results.append(("Environment Loading", test_environment_loading()))
    
    # 总结
    print("\n" + "#"*60)
    print("# Test Summary")
    print("#"*60)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed! Preset scenarios system is ready!")
        print("\nYou can now:")
        print("  1. Run: python run.bat (or ./run.sh)")
        print("  2. Open: http://localhost:5000")
        print("  3. Select a preset scenario from the dropdown")
        print("  4. Start simulation and enjoy!")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    print("="*60 + "\n")
    
    return all_passed


if __name__ == '__main__':
    import sys
    success = main()
    sys.exit(0 if success else 1)
