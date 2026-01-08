extends GutTest
## Unit tests for CollectibleComponent
##
## Tests collectible pickup behavior, scoring, auto-collection,
## delays, and edge cases

var collectible_scene: PackedScene
var collectible: CollectibleComponent
var test_collector: Node2D


func before_each() -> void:
	# Create a test collector (simulates player)
	test_collector = Node2D.new()
	test_collector.add_to_group("player")
	add_child_autofree(test_collector)
	
	# Create collectible component
	collectible = CollectibleComponent.new()
	add_child_autofree(collectible)


func after_each() -> void:
	# Cleanup happens automatically with autofree
	pass


# ============================================================================
# BASIC COLLECTION TESTS
# ============================================================================

func test_collectible_initializes_with_defaults() -> void:
	assert_eq(collectible.collectible_type, "coin", "Should default to coin type")
	assert_eq(collectible.point_value, 10, "Should default to 10 points")
	assert_true(collectible.auto_collect, "Should auto-collect by default")
	assert_true(collectible.destroy_on_collect, "Should destroy on collect by default")
	assert_false(collectible.is_collected, "Should not be collected initially")


func test_manual_collection() -> void:
	var signal_emitted := false
	var emitted_collector = null
	
	collectible.collected.connect(func(collector):
		signal_emitted = true
		emitted_collector = collector
	)
	
	collectible.collect(test_collector)
	
	assert_true(signal_emitted, "Should emit collected signal")
	assert_eq(emitted_collector, test_collector, "Should pass collector in signal")
	assert_true(collectible.is_collected, "Should mark as collected")


func test_cannot_collect_twice() -> void:
	var collection_count := 0
	var failure_count := 0
	
	collectible.collected.connect(func(_collector): collection_count += 1)
	collectible.collection_failed.connect(func(_collector, _reason): failure_count += 1)
	
	collectible.collect(test_collector)
	collectible.collect(test_collector)
	
	assert_eq(collection_count, 1, "Should only collect once")
	assert_eq(failure_count, 1, "Should emit failure on second attempt")


func test_collection_failure_reason() -> void:
	var failure_reason := ""
	
	collectible.collection_failed.connect(func(_collector, reason: String):
		failure_reason = reason
	)
	
	collectible.collect(test_collector)
	collectible.collect(test_collector)
	
	assert_eq(failure_reason, "already_collected", "Should provide correct failure reason")


# ============================================================================
# AUTO-COLLECTION TESTS
# ============================================================================

func test_auto_collection_on_body_entered() -> void:
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	# Simulate body entering
	collectible._on_body_entered(test_collector)
	
	assert_true(signal_emitted, "Should auto-collect when player enters")


func test_auto_collection_respects_groups() -> void:
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	# Create a non-player body
	var enemy := Node2D.new()
	enemy.add_to_group("enemy")
	add_child_autofree(enemy)
	
	collectible._on_body_entered(enemy)
	
	assert_false(signal_emitted, "Should not collect from non-player groups")


func test_auto_collection_disabled() -> void:
	collectible.auto_collect = false
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	collectible._on_body_entered(test_collector)
	
	assert_false(signal_emitted, "Should not auto-collect when disabled")


# ============================================================================
# COLLECTION DELAY TESTS
# ============================================================================

func test_collection_with_delay() -> void:
	collectible.collection_delay = 0.5
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	collectible.collect(test_collector)
	
	# Should not emit immediately
	assert_false(signal_emitted, "Should not collect immediately with delay")
	assert_true(collectible.is_collected, "Should mark as collected immediately")
	
	# Wait for delay
	await wait_seconds(0.6)
	
	assert_true(signal_emitted, "Should collect after delay")


func test_collection_without_delay() -> void:
	collectible.collection_delay = 0.0
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	collectible.collect(test_collector)
	
	assert_true(signal_emitted, "Should collect immediately without delay")


# ============================================================================
# DESTROY BEHAVIOR TESTS
# ============================================================================

func test_destroy_on_collect() -> void:
	# Create a parent node for the collectible
	var parent := Node2D.new()
	add_child_autofree(parent)
	
	var test_collectible := CollectibleComponent.new()
	parent.add_child(test_collectible)
	test_collectible.destroy_on_collect = true
	
	test_collectible.collect(test_collector)
	
	# Wait for queue_free to process
	await wait_frames(2)
	
	assert_true(parent.is_queued_for_deletion(), "Should destroy parent on collect")


func test_no_destroy_on_collect() -> void:
	var parent := Node2D.new()
	add_child_autofree(parent)
	
	var test_collectible := CollectibleComponent.new()
	parent.add_child(test_collectible)
	test_collectible.destroy_on_collect = false
	
	test_collectible.collect(test_collector)
	
	await wait_frames(2)
	
	assert_false(parent.is_queued_for_deletion(), "Should not destroy parent when disabled")


# ============================================================================
# GETTER TESTS
# ============================================================================

func test_get_type() -> void:
	collectible.collectible_type = "gem"
	assert_eq(collectible.get_type(), "gem", "Should return collectible type")


func test_get_value() -> void:
	collectible.point_value = 50
	assert_eq(collectible.get_value(), 50, "Should return point value")


# ============================================================================
# CUSTOM COLLECTOR GROUPS TESTS
# ============================================================================

func test_multiple_collector_groups() -> void:
	collectible.collector_groups = ["player", "ally"]
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	var ally := Node2D.new()
	ally.add_to_group("ally")
	add_child_autofree(ally)
	
	collectible._on_body_entered(ally)
	
	assert_true(signal_emitted, "Should collect from any allowed group")


func test_empty_collector_groups() -> void:
	collectible.collector_groups = []
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	collectible._on_body_entered(test_collector)
	
	assert_false(signal_emitted, "Should not collect with empty groups array")


# ============================================================================
# EDGE CASES
# ============================================================================

func test_collect_with_null_collector() -> void:
	var signal_emitted := false
	collectible.collected.connect(func(_collector): signal_emitted = true)
	
	collectible.collect(null)
	
	assert_true(signal_emitted, "Should handle null collector gracefully")
