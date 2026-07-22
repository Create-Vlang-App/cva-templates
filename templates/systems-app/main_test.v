module main

import checksum

fn test_checksum() {
	assert checksum.of_bytes('ab'.bytes()) == u64(97 + 98)
}
