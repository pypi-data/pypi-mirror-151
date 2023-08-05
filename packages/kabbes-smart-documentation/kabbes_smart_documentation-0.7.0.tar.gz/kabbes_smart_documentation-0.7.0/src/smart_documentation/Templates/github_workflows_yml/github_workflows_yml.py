from smart_documentation import BaseDocumentation
from pypi_builder.Templates.default.default import Package
import dir_ops as do
import py_starter as ps
import os

class Documentation( BaseDocumentation, Package ):

    template_Dir = do.Dir( do.Path( os.path.abspath(__file__) ).ascend().join( 'Template' ) )
    DEFAULT_KWARGS = {
    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( Documentation.DEFAULT_KWARGS, kwargs )
        BaseDocumentation.__init__( self, *args, **joined_kwargs )
        Package.__init__( self, *args, **joined_kwargs )
