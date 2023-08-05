import dir_ops as do
import py_starter as ps
import smart_documentation

def get_template( *args, template = None, **kwargs ):

    #list_contents_Paths()
    module_Dirs = smart_documentation.templates_Dir.list_contents_Paths( block_paths=True,block_dirs=False )
    
    if template == None:
        module_Dir = ps.get_selection_from_list( module_Dirs )
    else:
        module_Dir = smart_documentation.templates_Dir.join_Dir( path = template )

    module_Path = do.Path( module_Dir.join( module_Dir.dirs[-1] + '.py' ) )

    module = module_Path.import_module()
    return module.Documentation

def generate( *args, **kwargs ):

    Documentation_template = get_template( *args, **kwargs )
    R = Documentation_template( smart_documentation._cwd_Dir )
    R.generate( *args, **kwargs )
