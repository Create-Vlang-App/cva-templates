// Run from template root: v run examples/example.v
module main

import mylib

fn main() {
	println(mylib.greet('library-starter'))
	println(mylib.add(10, 32))
}
