module static_files

import os

// static_path joins static dir with a relative path.
pub fn static_path(rel string) string {
	return os.join_path('static', rel)
}

// exists checks if a static file exists.
pub fn exists(rel string) bool {
	return os.exists(static_path(rel))
}
