module static_files

fn test_static_path() {
	p := static_path('index.html')
	assert p == 'static/index.html'
}

fn test_exists_false_for_missing() {
	assert exists('__missing_12345__.html') == false
}
