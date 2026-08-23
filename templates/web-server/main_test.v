module main

import health

fn test_app_type_compiles() {
	mut app := &App{}
	assert app != unsafe { nil }
}

fn test_health_ok_body() {
	assert health.ok_body() == 'OK'
}

fn test_health_index_contains_cva() {
	assert health.index_body().contains('CVA')
}
