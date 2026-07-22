module tensor

import vtl

// size_of_demo returns the size of a small 1D tensor.
pub fn size_of_demo() int {
	t := vtl.from_1d([1, 2, 3]) or { panic(err) }
	return t.size
}
