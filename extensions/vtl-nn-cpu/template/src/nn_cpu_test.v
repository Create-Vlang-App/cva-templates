module main

fn test_one_step_moves_toward_target() {
	w1 := one_step_mse_update(1.0, 2.0, 0.0, 0.1)
	assert w1 > 0.0
}

fn test_nn_cpu_demo_loss_finite() {
	loss := nn_cpu_demo_loss()
	assert loss >= 0.0
}

fn test_tensor_batch_size_smoke() {
	assert tensor_batch_size_smoke() == 4
}
