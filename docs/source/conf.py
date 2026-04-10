project = "MSMC2 Protocol"
author = "Manuel Hoyos"
release = "0.1"

extensions = ["myst_parser"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

html_theme = "sphinx_rtd_theme"

html_context = {
    "display_github": True,
    "github_user": "hoyosmanuel",
    "github_repo": "MSMC2-Protocol",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
