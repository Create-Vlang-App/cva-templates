module main

import veb

pub struct Context {
	veb.Context
}

pub struct App {}

@[get]
pub fn (app &App) index(mut ctx Context) veb.Result {
	return ctx.text('Hello from CVA web-server template')
}

@[path: '/health']
@[get]
pub fn (app &App) health(mut ctx Context) veb.Result {
	return ctx.text('OK')
}

fn main() {
	mut app := &App{}
	veb.run[App, Context](mut app, 8080)
}
