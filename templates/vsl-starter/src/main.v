module main

fn mean(values []f64) f64 {
	if values.len == 0 {
		return 0.0
	}
	mut sum := 0.0
	for v in values {
		sum += v
	}
	return sum / f64(values.len)
}

fn main() {
	println('mean=${mean([1.0, 2.0, 3.0])}')
	println('Add vsl with: v install vsl')
}
