import os
import dir_ops as do
from repository_generator.BaseRepository import BaseRepository
import py_starter.py_starter as ps

class Repository( BaseRepository ):

    template_Dir = do.Dir( do.Path( os.path.abspath(__file__) ).ascend().join( 'Template' ) )
    DEFAULT_KWARGS = {
    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( Repository.DEFAULT_KWARGS, kwargs )
        BaseRepository.__init__( self, *args, **joined_kwargs )

        self.url_pages = 'https://jameskabbes.github.io/' + self.repo_name

 
