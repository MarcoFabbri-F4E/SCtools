# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = "SCtools"
copyright = "2024, Alvaro Cubi"
author = "Alvaro Cubi"
release = "2.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autosectionlabel"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ["_static"]
html_logo = "_static/logo.png"
html_theme_options = {
    "show_nav_level": 2,  # Adjust the number of levels shown in the sidebar
    "navigation_depth": 4,  # Adjust the depth of the navigation tree
    "collapse_navigation": False,  # Keep the navigation expanded
}

# Include custom CSS file
def setup(app):
    app.add_css_file('custom.css')
