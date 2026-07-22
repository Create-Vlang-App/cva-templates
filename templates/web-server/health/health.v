module health

// Feature helpers for HTTP health/index responses.
// veb route methods stay on App in main.v (framework constraint).

pub fn index_body() string {
	return 'Hello from CVA web-server template'
}

pub fn ok_body() string {
	return 'OK'
}
