module redis

fn test_memory_client_set_get() {
	mut c := new_memory_client()
	assert c.set('k', 'v') == true
	val := c.get('k') or { '' }
	assert val == 'v'
}

fn test_memory_client_missing() {
	mut c := new_memory_client()
	assert c.get('missing') == none
}

fn test_new_config() {
	cfg := new_config('redis://localhost:6379/1')
	assert cfg.url == 'redis://localhost:6379/1'
}
