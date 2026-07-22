module operators

import ulises_jeremias.rxv

// sum_of_even_squares sums n^2 for even n in 1..max_n.
pub fn sum_of_even_squares(max_n int) int {
	mut obs := rxv.range(1, max_n)
	mut evens := obs.filter(fn (v int) bool {
		return v % 2 == 0
	})
	mut squares := rxv.map_[int, int](mut evens, fn (v int) ?int {
		return v * v
	})
	mut reduced := rxv.reduce_[int, int](mut squares, 0, fn (acc int, val int) int {
		return acc + val
	})
	mut out := [0]
	done := reduced.for_each(fn [mut out] (v int) {
		out[0] = v
	}, fn (e IError) {}, fn () {})
	_ = <-done
	return out[0]
}
