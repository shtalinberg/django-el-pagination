"""Django EL(Endless) Pagination documentation build configuration file."""



AUTHOR = 'Oleksandr Shtalinberg and Francesco Banconi'
APP = 'Django EL(Endless) Pagination'
TITLE = APP + ' Documentation'
VERSION = '4.0.0'


# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = APP
copyright = '2009-2023, ' + AUTHOR  # noqa: A001

# The short X.Y version.
version = release = VERSION

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'default'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Output file base name for HTML help builder.
htmlhelp_basename = 'DjangoELPaginationdoc'

# Grouping the document tree into LaTeX files. List of tuples (source start
# file, target name, title, author, documentclass [howto/manual]).
latex_documents = [(
    'index', 'DjangoELPagination.tex', TITLE, AUTHOR, 'manual')]

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', 'djangoelpagination', TITLE, [AUTHOR], 1)]

linkcheck_ignore = [r'http://localhost:8000']
