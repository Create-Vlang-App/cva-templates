module main

fn test_checksum() {
	assert checksum('ab'.bytes()) == u64(97 + 98)
}
