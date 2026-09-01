module redis

// RedisConfig holds connection settings.
pub struct RedisConfig {
pub:
	url string = 'redis://localhost:6379/0'
}

// RedisClient is a stub interface – unit tests use the in-memory implementation.
pub interface RedisClient {
	get(key string) ?string
	set(key string, value string) bool
}

// MemoryClient is an in-memory stub for tests.
pub struct MemoryClient {
mut:
	store map[string]string
}

pub fn new_memory_client() MemoryClient {
	return MemoryClient{
		store: map[string]string{}
	}
}

pub fn (mut c MemoryClient) get(key string) ?string {
	return c.store[key] or { return none }
}

pub fn (mut c MemoryClient) set(key string, value string) bool {
	c.store[key] = value
	return true
}

pub fn new_config(url string) RedisConfig {
	return RedisConfig{
		url: url
	}
}
