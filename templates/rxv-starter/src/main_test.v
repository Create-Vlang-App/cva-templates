module main

import pipeline

fn test_hello_via_pipeline() {
	assert pipeline.hello_value() == 'Hello, rxv!'
}
