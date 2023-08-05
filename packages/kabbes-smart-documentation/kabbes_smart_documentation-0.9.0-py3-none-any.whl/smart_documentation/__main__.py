import sys
from smart_documentation import generate

import py_starter as ps 
args, kwargs = ps.find_kwargs_in_strings( sys.argv[1:] )
generate( *args, **kwargs )
