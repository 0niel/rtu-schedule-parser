import os
import sys
from typing import Any, Dict

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# sys.path.insert(0, os.path.abspath('..'))

# Insert rtu_schedule_parser's path into the system.
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("_themes"))

import rtu_schedule_parser

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "rtu-schedule-parser"
copyright = "2022, Oniel"
author = "Oniel"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
]


napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

templates_path = ["_templates"]
exclude_patterns = ["_build"]

language = "ru"

# The short X.Y version.
version = rtu_schedule_parser.__version__
# The full version, including alpha/beta/rc tags.
release = rtu_schedule_parser.__version__


# If true, '()' will be appended to :func: etc. cross-reference text.
add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#
# show_authors = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_theme_options: Dict[str, Any] = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/pradyunsg/furo",
            "html": """
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 927.67 914.19">
                  <defs>
                    <style>
                      .cls-1 {
                        fill: #fff;
                      }
                    </style>
                  </defs>
                  <g id="&#x421;&#x43B;&#x43E;&#x439;_2" data-name="&#x421;&#x43B;&#x43E;&#x439; 2">
                    <g id="&#x421;&#x43B;&#x43E;&#x439;_1-2" data-name="&#x421;&#x43B;&#x43E;&#x439; 1">
                      <g>
                        <path class="cls-1" d="M205.15,218.36c-8.14,6.21-16,12.71-23.39,19.49-13.25-10.42-27.67-21.43-34.59-26.78C134.81,201.51,122,192.25,108.92,183c2.82,5.39,5.79,11.22,9.21,17.77,3.26,6.56,6.68,13,10,19.38s6.68,12.67,9.65,18.5c3.12,6,5.65,11.07,7.88,15.15L132,270.14c-4.55-1.43-10-3.14-16.28-5s-13-4-20.09-6.14-13.78-4.13-20.82-6.27c-6.89-2.14-13.34-4-19.06-5.84q17,16.75,34.49,32.64c6.33,5.65,19.59,17.54,31.82,28.71a298.93,298.93,0,0,0-14.86,26.44c-11.93-11.16-24.17-22.62-28.88-27-8.85-8.42-17.83-16.83-26.53-25.25s-17.25-16.68-25.21-24.66-15-15.54-21.1-22.36L24,213.21c4.84,1,10.7,2.4,17.44,4.11S55.68,221,63.6,223.14c7.77,2.28,15.83,4.55,23.9,7.12,7.91,2.43,15.54,4.71,22.58,7-3.42-6.55-7.13-13.69-11-21.12S91.51,201.27,87.94,194s-6.84-14.13-9.82-20.69c-3-6.41-5.36-11.81-7.15-16.47l17.68-21.21c7.79,4.91,16.32,10.4,25.73,16.77s19,13,28.83,20.25c9.85,7.09,19.71,14.32,29.57,21.56C177.93,198.1,192.06,208.52,205.15,218.36Z"/>
                        <g>
                          <path class="cls-1" d="M254.2,38.93l-28,11.78,52,123.92c9.18-4.32,18.51-8.19,28-11.78Z"/>
                          <path class="cls-1" d="M499.13,121.1c-2.82-5.1-5.93-10-8.89-14.71q-4.67-7.2-9.33-13.53a138.52,138.52,0,0,0-9-11.48c8.16-3.72,14.27-8.6,18.31-14.77,4.2-6,6.18-14,5.81-23.6-.56-15.36-6.2-26.43-17.23-33.36-11-7.08-26.56-10.18-46.88-9.58q-8.34.29-18.86,1.47A180.58,180.58,0,0,0,392.6,4.92L397,139.75q14.89-2.31,30.25-3.31l-1.55-47.67,14.92-.42a108.57,108.57,0,0,1,8.13,10.33c2.81,3.78,5.47,7.7,8.29,12.07,2.81,4.22,5.62,8.59,8.29,13.1,2.23,3.79,4.6,7.72,6.82,11.36,12.14.19,24,1,35.86,2.2C505.51,132.6,501.8,125.76,499.13,121.1ZM457.83,59c-4.81,3-13,4.79-24.39,5.17l-8.48.21L423.64,27.2l5-.48c1.75-.16,3.8-.32,6-.34,9.65-.37,17.12.74,22.12,3.48s7.81,7.4,8,14C464.93,50.86,462.63,55.85,457.83,59Z"/>
                          <path class="cls-1" d="M712,85.18l9.76-23.92L637.49,26.67,585.83,152.59a411.83,411.83,0,0,1,87.91,36.75.15.15,0,0,0,.15.15l11.49-27.68-60.32-24.68L636,110.36l49.9,20.52,9.61-23.48L645.57,87l10.19-24.8Z"/>
                          <path class="cls-1" d="M872.24,182.89c-10.22,2.27-20.58,4.84-31,7.56s-21.31,6-32.69,9.47-23.49,7.21-36,11.41c-11.67,3.75-30.34,10.18-44.79,15.12a302,302,0,0,1,24.9,22.48c27.86-10.17,101.82-35.47,103.72-36.07-1,1.76-57.51,89.68-58.67,91.3v.14a291.81,291.81,0,0,1,17,30c8.24-12.79,17.48-27.49,24.42-38.52,6.93-11.31,13.43-22,19.49-32.33s11.54-20.13,16.59-29.68,10.09-19,14.84-28.35Z"/>
                          <g>
                            <path class="cls-1" d="M186.72,688.9,130,742.26c1.45-8.22,3-17,4.45-26.27s2.57-18.2,3.71-27c1-8.94,1.84-17.44,2.41-25.65s.72-15.37.6-21.52l-.31-.72a228.2,228.2,0,0,1-15.19-20.91L28,712.4l22,23.27,62.32-58.74a479,479,0,0,1-6.39,53.38c-3.15,17.91-6.9,35.39-11.54,52.46l18.83,19.81,98.93-93.7A310.86,310.86,0,0,1,186.72,688.9Z"/>
                            <path class="cls-1" d="M283.46,749.44,238.08,872.65l30.36,11.25,45.25-122.77C303.38,757.67,293.35,753.78,283.46,749.44Z"/>
                            <path class="cls-1" d="M490.87,783.92l.64,76.07c-5.11-6.78-10.51-13.84-16.22-21-5.7-7.35-11.55-14.4-17.25-21.31S446.51,804.41,441,798.38c-5.23-5.46-10-10.34-14.33-14.2-9.23-.69-18.32-1.54-27.41-2.82l.89,132.83,32-.2-.54-85.73a478.41,478.41,0,0,1,34.76,41.15c10.83,14.56,21.07,29.28,30.44,44.16l27.2-.25-.89-132.82C512.49,782,501.69,783.27,490.87,783.92Z"/>
                            <path class="cls-1" d="M720.33,823.59c-1.35-5.74-3.87-11-6.48-16.91l-35.4-80.34c-9.25,5.45-18.66,10.61-28.51,15.34l33.71,76.73c17.05,37.88-35.54,32.22-40.08,31.87L643,877.44C652.86,881.41,733.88,881.17,720.33,823.59Z"/>
                            <path class="cls-1" d="M887.07,649.71c-12.5-3.12-24.41-6.1-35.58-8.66-11.32-2.55-22.19-4.82-32.47-6.81-10-2-22-4.1-31.86-5.65A242.78,242.78,0,0,1,769,651.33c4.14,9.28,10.08,21,14.79,30q7.3,13.9,15.95,29.09c5.61,10,11.82,20.54,18.47,31.52,6.66,11.14,14.07,23,22.08,35.84l20.23-27c-.3-.58-56.94-89.71-58.15-91.44,2.06.39,98.43,27.44,104.46,29.22l20.81-27.77Q905.82,654.6,887.07,649.71Z"/>
                          </g>
                        </g>
                        <path class="cls-1" d="M741.39,439.9H708.65A49.79,49.79,0,0,0,659.07,394H526.75a82.28,82.28,0,0,1-66.08-33.37A82.24,82.24,0,0,1,394.6,394H262.28a49.8,49.8,0,0,0-49.59,45.91H180a82.52,82.52,0,0,1,82.33-78.58H394.6a49.79,49.79,0,0,0,49.73-49.74H477a49.79,49.79,0,0,0,49.74,49.74H659.07A82.51,82.51,0,0,1,741.39,439.9Z"/>
                        <path class="cls-1" d="M741.39,480.23a82.51,82.51,0,0,1-82.33,78.59H526.74A49.79,49.79,0,0,0,477,608.55H444.33a49.79,49.79,0,0,0-49.74-49.73H262.27A82.51,82.51,0,0,1,180,480.23h32.74a49.79,49.79,0,0,0,49.58,45.91H394.59a82.28,82.28,0,0,1,66.08,33.37,82.24,82.24,0,0,1,66.07-33.37H659.06a49.8,49.8,0,0,0,49.59-45.91Z"/>
                        <path class="cls-1" d="M460.64,171.05c-190.89,0-346.06,129.74-346.06,289.06S269.75,749,460.64,749s346.22-129.6,346.22-288.91S651.54,171.05,460.64,171.05Zm0,545.39c-172.89,0-313.49-115-313.49-256.33s140.6-256.34,313.49-256.34,313.49,115,313.49,256.34S633.54,716.44,460.64,716.44Z"/>
                        <rect class="cls-1" x="542.35" y="443.92" width="98.02" height="32.29"/>
                        <rect class="cls-1" x="280.98" y="443.92" width="98.02" height="32.29"/>
                        <path class="cls-1" d="M52.07,548H15.94a250,250,0,0,1,0-175.67h36a217.66,217.66,0,0,0-18.58,87.91A213.54,213.54,0,0,0,52.07,548Z"/>
                        <path class="cls-1" d="M921.51,460.12A250.22,250.22,0,0,1,905.57,548h-36a217.82,217.82,0,0,0,18.57-87.91,213.38,213.38,0,0,0-18.72-87.76h36.13A248.78,248.78,0,0,1,921.51,460.12Z"/>
                      </g>
                    </g>
                  </g>
                </svg>
            """,
            "class": "",
        },
    ],
    "source_repository": "https://github.com/mirea-ninja/rtu-schedule-parser",
    "source_branch": "main",
    "source_directory": "docs/",
}
