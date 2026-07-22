module main

import checksum
import os

fn main() {
	args := os.args
	payload := if args.len > 1 { args[1].bytes() } else { 'systems'.bytes() }
	println('checksum=${checksum.of_bytes(payload)}')
}
