module main

import veb
import health

pub struct Context {
	veb.Context
}

pub struct App {}

@[get]
pub fn (app &App) index(mut ctx Context) veb.Result {
	return ctx.text(health.index_body())
}

@[path: '/health']
@[get]
pub fn (app &App) health(mut ctx Context) veb.Result {
	return ctx.text(health.ok_body())
}

fn main() {
	mut app := &App{}
	veb.run[App, Context](mut app, 8080)
}
