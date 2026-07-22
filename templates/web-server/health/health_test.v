module health

fn test_index_body() {
	assert index_body().contains('CVA')
}

fn test_ok_body() {
	assert ok_body() == 'OK'
}
