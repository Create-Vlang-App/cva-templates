module plotting

import vsl.plot

// build_demo_scatter creates a scatter plot (no GUI).
pub fn build_demo_scatter() &plot.Plot {
	mut plt := plot.Plot.new()
	plt.scatter(
		x:    [0.0, 1.0, 2.0, 3.0]
		y:    [0.0, 1.0, 0.5, 2.0]
		mode: 'markers'
	)
	plt.layout(title: 'CVA vsl-plotting demo')
	return plt
}
