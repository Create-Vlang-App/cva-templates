module main

import vtl

fn tensor_size() int {
	t := vtl.from_1d([1, 2, 3]) or { panic(err) }
	return t.size
}

fn main() {
	println('vtl tensor size=${tensor_size()}')
}
