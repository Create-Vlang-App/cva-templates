module main

import cli { Command, Flag }
import os

fn main() {
	mut cmd := Command{
		name:        'app'
		description: 'CLI application starter for Create Vlang App'
		version:     '0.1.0'
	}
	cmd.add_flag(Flag{
		flag:        .string
		name:        'name'
		abbrev:      'n'
		description: 'Name to greet'
		default_value: ['world']
	})
	cmd.add_flag(Flag{
		flag:     .bool
		name:     'help'
		abbrev:   'h'
		description: 'Show help'
	})
	cmd.setup()
	cmd.parse(os.args)
	name := cmd.flags.get_string('name') or { 'world' }
	println('Hello, ${name}!')
}
