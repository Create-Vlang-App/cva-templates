module checksum

fn test_of_bytes() {
	assert of_bytes('ab'.bytes()) == u64(97 + 98)
}
