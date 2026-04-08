project = 'MSMC2 Protocol'
copyright = '2026, Manuel Hoyos'
author = 'Manuel Hoyos'
release = '0.1'

extensions = ["myst_parser"]

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_context = {
    "display_github": True,
    "github_user": "hoyosmanuel",
    "github_repo": "MSMC2-Protocol",
    "github_version": "main",
}

html_theme_options = {
    "display_version": True,
}