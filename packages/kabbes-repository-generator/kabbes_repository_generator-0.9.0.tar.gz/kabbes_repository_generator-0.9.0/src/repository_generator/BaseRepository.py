import git
import dir_ops as do
import py_starter as ps
from parent_class import ParentClass

class BaseRepository( ParentClass, git.Repo ):

    """Pulled from the GitPython class Repo, must be initialized at the root directory of a Git repository"""

    TRIGGER_BEG = '{-{'
    TRIGGER_END = '}-}'

    DEFAULT_KWARGS = {
    }

    def __init__( self, Dir, **kwargs ):

        git.Repo.__init__( self, Dir.p )
        ParentClass.__init__( self )

        joined_kwargs = ps.merge_dicts( BaseRepository.DEFAULT_KWARGS, kwargs )
        self.set_atts( joined_kwargs )

        self.Dir = Dir
        self.url_clone = self.remotes.origin.url
        self.url_nav = self.url_clone[ : -1*len('.git') ]
        self.repo_name = self.url_nav.split( '/' )[-1]
        self.readme_Path = self.Dir.join_Path( path = 'README.md' )

    def print_imp_atts(self, **kwargs):

        return self._print_imp_atts_helper( atts = ['repo_name','Dir'], **kwargs )

    def print_one_line_atts(self, **kwargs):
         
        return self._print_one_line_atts_helper( atts = ['repo_name','Dir'], **kwargs )

    def generate( self, *args, overwrite: bool = False, **kwargs ):

        print ('Generating from Repository template')
        self.copy_template_files( overwrite=overwrite )

    def get_attr( self, att_string ):

        if not self.has_attr( att_string ):
            att_value = input('Enter a value for ' + att_string + ': ')
            self.set_attr( att_string, att_value )

        return getattr( self, att_string )

    def copy_template_files( self, *args, overwrite: bool = False, **kwargs ) -> None:

        bad_folders = ['__pycache__','.git']
        template_Paths = self.template_Dir.walk_contents_Paths( block_dirs = False, block_paths = False, folders_to_skip = bad_folders )
        rel_Paths = template_Paths.get_rels( self.template_Dir )
        paste_Paths = rel_Paths.join_Dir( self.Dir )
        
        for i in range(len(paste_Paths)):

            unformatted_Path = list(paste_Paths)[i]

            if unformatted_Path.type_path:
                copy_Path = list(template_Paths)[i]
                paste_Path = do.Path( self.format_string_by_atts( unformatted_Path.path, trigger_beg = self.TRIGGER_BEG, trigger_end = self.TRIGGER_END ) )
                print (paste_Path)

                if not paste_Path.exists() or overwrite:
                    print ('Copying Template Path: ' + str(paste_Path) )            

                    if paste_Path.exists():
                        paste_Path.remove( override = True )

                    copy_Path.copy( Destination = paste_Path, print_off=False, override = True ) 

                    try:
                        string = paste_Path.read()
                    except:
                        print ('Skipping formatting, cannot read')
                        continue
                    
                    # if we are able to read, then we shouldn't be copying it over
                    formatted_string = self.format_string_by_atts( paste_Path.read(), trigger_beg = self.TRIGGER_BEG, trigger_end = self.TRIGGER_END )
                    paste_Path.write( string = formatted_string, override = True )

                else:
                    print ('Skipping existing Path: ' + str(paste_Path) )

            if unformatted_Path.type_dir:
                copy_Dir = list(template_Paths)[i]
                paste_Dir = do.Dir( self.format_string_by_atts( unformatted_Path.path, trigger_beg = self.TRIGGER_BEG, trigger_end = self.TRIGGER_END ) )
                print (paste_Dir)

                if not paste_Dir.exists():
                    print ('Copying Template Dir: ' + str(paste_Dir))
                    paste_Dir.create( override = True )

                else:
                    print ('Skipping Template Dir: ' + str(paste_Dir))


