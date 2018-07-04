import sys
import os

root = "${directory.replace("\\", "\\\\")}"

sys.path = ["${python_path.replace("\\", "\\\\")}", os.path.join(root, 'crdppf_core')] + sys.path

from pyramid.paster import get_app

configfile = os.path.join(root, "${'development' if development == 'TRUE' else 'production'}.ini")

application = get_app(configfile, 'main')
