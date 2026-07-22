module classical_ml

// fit_slope returns ordinary least-squares slope for y ~= a*x (through origin for simplicity).
pub fn fit_slope(x []f64, y []f64) f64 {
	mut num := 0.0
	mut den := 0.0
	for i in 0 .. x.len {
		num += x[i] * y[i]
		den += x[i] * x[i]
	}
	if den == 0 {
		return 0
	}
	return num / den
}

pub fn demo_linreg_slope() f64 {
	x := [1.0, 2.0, 3.0, 4.0]
	y := [2.0, 4.0, 6.0, 8.0]
	return fit_slope(x, y)
}
