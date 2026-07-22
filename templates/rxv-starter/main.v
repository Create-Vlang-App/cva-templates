module main

fn main() {
	src := Observable{values: [1, 2, 3]}
	doubled := map_values(src.values, fn (v int) int { return v * 2 })
	println('sum=${src.sum()} doubled=${doubled}')
}
