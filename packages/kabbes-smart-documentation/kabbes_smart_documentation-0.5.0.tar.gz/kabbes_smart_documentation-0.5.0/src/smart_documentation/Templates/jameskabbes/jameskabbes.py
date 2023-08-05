from smart_documentation import BaseDocumentation
from pypi_builder.Templates.jameskabbes.jameskabbes import Package
import dir_ops as do
import py_starter as ps
import os

from smart_documentation.Templates.default.default import Documentation as default_Documentation

class Documentation( BaseDocumentation, Package ):

    template_Dir = default_Documentation.template_Dir
    DEFAULT_KWARGS = {
    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( Documentation.DEFAULT_KWARGS, kwargs )
        BaseDocumentation.__init__( self, *args, **joined_kwargs )
        Package.__init__( self, *args, **joined_kwargs )
        