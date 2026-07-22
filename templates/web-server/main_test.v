module main

fn test_app_type_compiles() {
	mut app := &App{}
	assert app != unsafe { nil }
}
