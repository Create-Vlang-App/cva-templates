module main

fn test_sum() {
	o := Observable{values: [1, 2, 3]}
	assert o.sum() == 6
}

fn test_map_values() {
	out := map_values([1, 2], fn (v int) int { return v + 1 })
	assert out == [2, 3]
}
