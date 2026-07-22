module main

import ulises_jeremias.rxv

fn hello_value() string {
	return 'Hello, rxv!'
}

fn main() {
	mut obs := rxv.just[string](hello_value())
	done := obs.for_each(fn (v string) {
		println(v)
	}, fn (e IError) {
		eprintln('error: ${e}')
	}, fn () {})
	_ = <-done
}
