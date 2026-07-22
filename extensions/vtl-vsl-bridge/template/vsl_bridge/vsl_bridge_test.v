module vsl_bridge

fn test_bridge_demo_plot() {
	plt := bridge_demo_plot()
	assert plt.traces.len >= 1
}
