module main

import greet

fn test_greet_default() {
	assert greet.message('world') == 'Hello, world!'
}
