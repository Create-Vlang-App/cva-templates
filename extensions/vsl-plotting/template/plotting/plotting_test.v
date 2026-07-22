module plotting

fn test_build_demo_scatter() {
	plt := build_demo_scatter()
	assert plt.traces.len >= 1
}
