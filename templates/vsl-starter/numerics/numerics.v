module numerics

import vsl.la

// matrix_trace returns the trace of a small demo matrix.
pub fn matrix_trace() f64 {
	mut a := la.Matrix.new[f64](2, 2)
	a.set(0, 0, 1.0)
	a.set(1, 1, 2.0)
	return a.get(0, 0) + a.get(1, 1)
}
