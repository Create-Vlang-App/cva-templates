module main

import os

@[inline]
fn checksum(data []u8) u64 {
	mut sum := u64(0)
	for b in data {
		sum += u64(b)
	}
	return sum
}

fn main() {
	args := os.args
	payload := if args.len > 1 { args[1].bytes() } else { 'systems'.bytes() }
	println('checksum=${checksum(payload)}')
}
