module pipeline

import ulises_jeremias.rxv

// hello_value is the demo observable payload.
pub fn hello_value() string {
	return 'Hello, rxv!'
}

// run_hello prints hello_value through an rxv observable.
pub fn run_hello() {
	mut obs := rxv.just[string](hello_value())
	done := obs.for_each(fn (v string) {
		println(v)
	}, fn (e IError) {
		eprintln('error: ${e}')
	}, fn () {})
	_ = <-done
}
