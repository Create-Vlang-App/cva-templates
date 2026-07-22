module main

import vtl

// one_step_mse_update performs a single gradient step on scalar param w for target t ~= w*x.
fn one_step_mse_update(x f64, t f64, w0 f64, lr f64) f64 {
	pred := w0 * x
	grad := 2.0 * (pred - t) * x
	return w0 - lr * grad
}

fn nn_cpu_demo_loss() f64 {
	// Learn w for 2*x ~= t with x=1,t=2
	mut w := 0.0
	w = one_step_mse_update(1.0, 2.0, w, 0.1)
	pred := w * 1.0
	return (pred - 2.0) * (pred - 2.0)
}

fn tensor_batch_size_smoke() int {
	t := vtl.from_1d([0.0, 1.0, 0.0, 1.0]) or { panic(err) }
	return t.size
}
