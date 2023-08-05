from pypi_builder import BasePackage
import py_starter as ps
import pypandoc

class BaseDocumentation( BasePackage ):

    CONFIG_ATTS_NEEDED = ['author','version','name']

    DEFAULT_KWARGS = {
        'readme_rst': '',
    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( BaseDocumentation.DEFAULT_KWARGS, kwargs )
        BasePackage.__init__( self, *args, **joined_kwargs )
        self.convert_readme()

    def convert_readme( self ):

        if self.readme_Path.exists():
            md_string = self.readme_Path.read()
            self.readme_rst = pypandoc.convert_text( md_string, 'rst', format = 'md' )
            
