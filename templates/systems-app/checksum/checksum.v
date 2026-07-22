module checksum

@[inline]
pub fn of_bytes(data []u8) u64 {
	mut sum := u64(0)
	for b in data {
		sum += u64(b)
	}
	return sum
}
