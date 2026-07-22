module classical_ml

fn test_fit_slope_perfect_line() {
	assert fit_slope([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == 2.0
}

fn test_demo_linreg_slope() {
	assert demo_linreg_slope() == 2.0
}
