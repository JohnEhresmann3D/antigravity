# Godot Runtime Performance Profiling Guide

## Overview

This guide covers how to monitor and profile your Godot game's performance during runtime, both in development and production environments. Runtime profiling allows you to track real-world performance metrics as players experience your game.

## Table of Contents

1. [Built-in Performance Monitoring](#built-in-performance-monitoring)
2. [Custom Performance Monitors](#custom-performance-monitors)
3. [Function-Level Profiling](#function-level-profiling)
4. [In-Game Performance Overlay](#in-game-performance-overlay)
5. [Production Monitoring](#production-monitoring)
6. [Best Practices](#best-practices)

---

## Built-in Performance Monitoring

Godot provides a `Performance` singleton with access to various runtime metrics.

### Available Metrics

```gdscript
# Frame rate metrics
var fps = Performance.get_monitor(Performance.TIME_FPS)
var frame_time = Performance.get_monitor(Performance.TIME_PROCESS)
var physics_time = Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)

# Memory metrics
var static_memory = Performance.get_monitor(Performance.MEMORY_STATIC)
var dynamic_memory = Performance.get_monitor(Performance.MEMORY_DYNAMIC)
var object_count = Performance.get_monitor(Performance.OBJECT_COUNT)
var node_count = Performance.get_monitor(Performance.OBJECT_NODE_COUNT)
var resource_count = Performance.get_monitor(Performance.OBJECT_RESOURCE_COUNT)

# Rendering metrics
var objects_drawn = Performance.get_monitor(Performance.RENDER_OBJECTS_IN_FRAME)
var draw_calls = Performance.get_monitor(Performance.RENDER_DRAW_CALLS_IN_FRAME)
var vertices_drawn = Performance.get_monitor(Performance.RENDER_VERTICES_IN_FRAME)

# Physics metrics (2D)
var active_objects_2d = Performance.get_monitor(Performance.PHYSICS_2D_ACTIVE_OBJECTS)
var collision_pairs_2d = Performance.get_monitor(Performance.PHYSICS_2D_COLLISION_PAIRS)
var islands_2d = Performance.get_monitor(Performance.PHYSICS_2D_ISLAND_COUNT)
```

### Important Notes

- **Debug vs Release**: Some monitors only work in debug builds and return 0 in release builds
- **Update Frequency**: Some metrics may have up to 1 second delay for performance reasons
- **Overhead**: Monitoring itself has minimal performance impact

---

## Custom Performance Monitors

Create game-specific metrics to track your unique systems.

### Basic Custom Monitor

```gdscript
extends Node

func _ready():
    # Register custom monitors
    Performance.add_custom_monitor("game/enemies_alive", _get_enemy_count)
    Performance.add_custom_monitor("game/gravity_zones_active", _get_gravity_zone_count)
    Performance.add_custom_monitor("game/player_velocity", _get_player_velocity)

func _get_enemy_count() -> int:
    return get_tree().get_nodes_in_group("enemies").size()

func _get_gravity_zone_count() -> int:
    return get_tree().get_nodes_in_group("gravity_zones").size()

func _get_player_velocity() -> float:
    var player = get_tree().get_first_node_in_group("player")
    if player and player.has_method("get_velocity"):
        return player.get_velocity().length()
    return 0.0
```

### Advanced Custom Monitor with Caching

```gdscript
extends Node

var _cached_enemy_count: int = 0
var _cache_timer: float = 0.0
const CACHE_INTERVAL: float = 0.5  # Update every 0.5 seconds

func _ready():
    Performance.add_custom_monitor("game/enemies_alive", _get_cached_enemy_count)

func _process(delta: float):
    _cache_timer += delta
    if _cache_timer >= CACHE_INTERVAL:
        _cached_enemy_count = get_tree().get_nodes_in_group("enemies").size()
        _cache_timer = 0.0

func _get_cached_enemy_count() -> int:
    return _cached_enemy_count
```

### Viewing Custom Monitors

In the Godot Editor:
1. Run your game
2. Open **Debugger → Monitors** tab
3. Your custom monitors appear under their category (e.g., "game/enemies_alive")

---

## Function-Level Profiling

Track execution time of specific functions to identify bottlenecks.

### Simple Function Timer

```gdscript
class_name PerformanceTimer
extends RefCounted

var start_time: int = 0
var function_name: String = ""

func _init(fname: String):
    function_name = fname
    start_time = Time.get_ticks_usec()

func stop() -> float:
    var duration = (Time.get_ticks_usec() - start_time) / 1000.0  # Convert to ms
    print("[PERF] %s took %.3f ms" % [function_name, duration])
    return duration
```

**Usage:**
```gdscript
func expensive_calculation():
    var timer = PerformanceTimer.new("expensive_calculation")
    
    # Your code here
    for i in range(10000):
        var result = sqrt(i) * PI
    
    timer.stop()
```

### Advanced Function Profiler

```gdscript
class_name FunctionProfiler
extends RefCounted

static var timings: Dictionary = {}
static var enabled: bool = true

static func profile(function_name: String, callable: Callable):
    if not enabled:
        return callable.call()
    
    var start = Time.get_ticks_usec()
    var result = callable.call()
    var duration = Time.get_ticks_usec() - start
    
    if not timings.has(function_name):
        timings[function_name] = {
            "count": 0,
            "total_time": 0,
            "max_time": 0,
            "min_time": INF,
            "avg_time": 0
        }
    
    var data = timings[function_name]
    data["count"] += 1
    data["total_time"] += duration
    data["max_time"] = max(data["max_time"], duration)
    data["min_time"] = min(data["min_time"], duration)
    data["avg_time"] = data["total_time"] / data["count"]
    
    return result

static func get_report() -> Array:
    var report = []
    for func_name in timings:
        var data = timings[func_name]
        report.append({
            "function": func_name,
            "calls": data["count"],
            "avg_ms": data["avg_time"] / 1000.0,
            "max_ms": data["max_time"] / 1000.0,
            "min_ms": data["min_time"] / 1000.0,
            "total_ms": data["total_time"] / 1000.0
        })
    
    # Sort by total time descending
    report.sort_custom(func(a, b): return a["total_ms"] > b["total_ms"])
    return report

static func print_report():
    print("\n=== Function Profiling Report ===")
    for entry in get_report():
        print("%s: %d calls, avg: %.3f ms, max: %.3f ms, total: %.3f ms" % [
            entry["function"],
            entry["calls"],
            entry["avg_ms"],
            entry["max_ms"],
            entry["total_ms"]
        ])

static func reset():
    timings.clear()

static func save_report(path: String):
    var file = FileAccess.open(path, FileAccess.WRITE)
    if file:
        file.store_string(JSON.stringify(get_report(), "\t"))
        file.close()
```

**Usage:**
```gdscript
func _physics_process(delta):
    FunctionProfiler.profile("update_player_movement", func():
        update_player_movement(delta)
    )
    
    FunctionProfiler.profile("update_enemies", func():
        update_enemies(delta)
    )

func _exit_tree():
    FunctionProfiler.print_report()
    FunctionProfiler.save_report("user://profiling_report.json")
```

---

## In-Game Performance Overlay

Create a visual overlay to display performance metrics during gameplay.

### Basic Performance HUD

```gdscript
extends CanvasLayer

@onready var fps_label = $VBoxContainer/FPSLabel
@onready var memory_label = $VBoxContainer/MemoryLabel
@onready var objects_label = $VBoxContainer/ObjectsLabel
@onready var draw_calls_label = $VBoxContainer/DrawCallsLabel

var update_interval: float = 0.5
var time_since_update: float = 0.0

func _process(delta):
    time_since_update += delta
    
    if time_since_update >= update_interval:
        update_display()
        time_since_update = 0.0

func update_display():
    # FPS
    var fps = Performance.get_monitor(Performance.TIME_FPS)
    fps_label.text = "FPS: %d" % fps
    
    # Memory (convert to MB)
    var memory = Performance.get_monitor(Performance.MEMORY_STATIC) / 1024.0 / 1024.0
    memory_label.text = "Memory: %.1f MB" % memory
    
    # Objects
    var objects = Performance.get_monitor(Performance.RENDER_OBJECTS_IN_FRAME)
    objects_label.text = "Objects: %d" % objects
    
    # Draw calls
    var draw_calls = Performance.get_monitor(Performance.RENDER_DRAW_CALLS_IN_FRAME)
    draw_calls_label.text = "Draw Calls: %d" % draw_calls
```

---

## Production Monitoring

### Performance Data Logger

```gdscript
extends Node

var performance_log: Array = []
var log_interval: float = 1.0  # Log every second
var time_since_log: float = 0.0
var max_log_entries: int = 3600  # 1 hour at 1 second intervals

func _process(delta):
    time_since_log += delta
    
    if time_since_log >= log_interval:
        log_performance_snapshot()
        time_since_log = 0.0

func log_performance_snapshot():
    var snapshot = {
        "timestamp": Time.get_ticks_msec(),
        "fps": Performance.get_monitor(Performance.TIME_FPS),
        "frame_time_ms": Performance.get_monitor(Performance.TIME_PROCESS) * 1000.0,
        "physics_time_ms": Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS) * 1000.0,
        "memory_mb": Performance.get_monitor(Performance.MEMORY_STATIC) / 1024.0 / 1024.0,
        "objects_drawn": Performance.get_monitor(Performance.RENDER_OBJECTS_IN_FRAME),
        "draw_calls": Performance.get_monitor(Performance.RENDER_DRAW_CALLS_IN_FRAME),
        "node_count": Performance.get_monitor(Performance.OBJECT_NODE_COUNT)
    }
    
    performance_log.append(snapshot)
    
    # Prevent unlimited growth
    if performance_log.size() > max_log_entries:
        performance_log.pop_front()

func save_log():
    var timestamp = Time.get_datetime_string_from_system().replace(":", "-")
    var filename = "user://performance_log_%s.json" % timestamp
    
    var file = FileAccess.open(filename, FileAccess.WRITE)
    if file:
        file.store_string(JSON.stringify(performance_log, "\t"))
        file.close()
        print("Performance log saved to: ", filename)

func get_statistics() -> Dictionary:
    if performance_log.is_empty():
        return {}
    
    var fps_values = []
    var frame_times = []
    
    for entry in performance_log:
        fps_values.append(entry["fps"])
        frame_times.append(entry["frame_time_ms"])
    
    fps_values.sort()
    frame_times.sort()
    
    return {
        "avg_fps": fps_values.reduce(func(a, b): return a + b, 0) / fps_values.size(),
        "min_fps": fps_values[0],
        "max_fps": fps_values[-1],
        "avg_frame_time": frame_times.reduce(func(a, b): return a + b, 0) / frame_times.size(),
        "p95_frame_time": frame_times[int(frame_times.size() * 0.95)],
        "p99_frame_time": frame_times[int(frame_times.size() * 0.99)]
    }

func _notification(what):
    if what == NOTIFICATION_WM_CLOSE_REQUEST:
        save_log()
```

---

## Best Practices

### 1. Systematic Measurement
- **Don't guess** where performance issues are—always measure
- Use profiling to identify actual bottlenecks before optimizing
- Profile in realistic scenarios (demanding scenes, not empty test levels)

### 2. Understanding Bottleneck Types
- **Continuous low FPS**: Slow processes running every frame
- **Intermittent spikes**: Infrequent heavy operations (loading, spawning)
- **Slow loading**: Asset loading, scene instantiation

### 3. Profiling Strategy
- Start with Godot's built-in profiler in the editor
- Add custom monitors for game-specific systems
- Use function-level profiling for suspected bottlenecks
- Profile both debug and release builds (performance differs significantly)

### 4. Monitor Key Metrics
Essential metrics to track:
- **FPS**: Target 60 FPS (16.67ms per frame) or 30 FPS (33.33ms)
- **Frame time**: Process time + Physics time should be under target
- **Memory usage**: Watch for memory leaks (continuously growing)
- **Draw calls**: Minimize for better GPU performance
- **Node count**: Too many nodes can slow scene tree processing

### 5. Optimization Workflow
1. **Profile** to identify the bottleneck
2. **Optimize** the specific bottleneck
3. **Re-profile** to measure improvement
4. **Repeat** until performance targets are met

### 6. CPU vs GPU Bottlenecks
**CPU Bottleneck** (low FPS, low GPU usage):
- Optimize scripts (cache node references, reduce iterations)
- Reduce physics calculations
- Use object pooling
- Consider multithreading for heavy computations

**GPU Bottleneck** (low FPS, high GPU usage):
- Optimize shaders
- Reduce draw calls (use MultiMesh)
- Implement LOD (Level of Detail)
- Use occlusion culling
- Reduce texture sizes

### 7. Production Considerations
- Some Performance monitors return 0 in release builds
- Custom monitors work in both debug and release
- Consider telemetry for production monitoring
- Log performance data for post-mortem analysis
- Provide in-game performance settings (quality levels)

### 8. Antigravity-Specific Monitoring
For this project, consider tracking:
- Active gravity zones
- Player velocity and state changes
- Enemy AI processing time
- Collectible spawning/despawning
- Particle system counts
- Camera transitions

---

## Example: Complete Performance Monitor for Antigravity

See `scripts/performance/runtime_performance_monitor.gd` for a complete implementation tailored to this project.

---

## Additional Resources

- [Godot Performance Documentation](https://docs.godotengine.org/en/stable/tutorials/performance/index.html)
- [Godot Profiler Guide](https://docs.godotengine.org/en/stable/tutorials/performance/using_the_profiler.html)
- [Performance Class Reference](https://docs.godotengine.org/en/stable/classes/class_performance.html)

---

## Next Steps

1. Implement `RuntimePerformanceMonitor` in your project
2. Add custom monitors for Antigravity-specific systems
3. Create an in-game debug overlay (toggle with F3)
4. Set up performance logging for playtesting sessions
5. Establish performance budgets (target FPS, max memory, etc.)
