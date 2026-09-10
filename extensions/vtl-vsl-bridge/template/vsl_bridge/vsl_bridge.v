module vsl_bridge

import vsl.plot
import vtl

// tensor_to_scatter builds a plot from a VTL 1D tensor (no GUI).
pub fn tensor_to_scatter(values []f64) &plot.Plot {
	x := vtl.seq[f64](values.len)
	mut plt := plot.Plot.new()
	plt.scatter(
		x:    x.to_array()
		y:    values
		mode: 'lines+markers'
	)
	plt.layout(title: 'VTL → VSL plot bridge')
	return plt
}

pub fn bridge_demo_plot() &plot.Plot {
	y := [0.0, 1.0, 0.5, 2.0, 1.5]
	return tensor_to_scatter(y)
}
