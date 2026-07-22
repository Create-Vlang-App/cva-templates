module main

pub struct Observable {
pub:
	values []int
}

pub fn (o Observable) sum() int {
	mut total := 0
	for v in o.values {
		total += v
	}
	return total
}

pub fn map_values(values []int, f fn (int) int) []int {
	mut out := []int{len: values.len}
	for i, v in values {
		out[i] = f(v)
	}
	return out
}
