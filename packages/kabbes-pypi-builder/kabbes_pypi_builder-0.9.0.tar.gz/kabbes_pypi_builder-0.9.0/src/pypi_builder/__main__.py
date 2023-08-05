from pypi_builder import generate
import sys
import py_starter as ps 

args, kwargs = ps.find_kwargs_in_strings( sys.argv[1:] )
generate( *args, **kwargs )
