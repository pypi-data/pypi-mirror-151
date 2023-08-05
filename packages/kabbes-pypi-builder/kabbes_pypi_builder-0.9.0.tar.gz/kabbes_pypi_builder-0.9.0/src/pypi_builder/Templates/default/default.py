from pypi_builder import BasePackage
from repository_generator.Templates.default.default import Repository 
import dir_ops as do
import py_starter as ps
import os

class Package( BasePackage, Repository ):

    template_Dir = do.Dir( do.Path( os.path.abspath(__file__) ).ascend().join( 'Template' ) )
    DEFAULT_KWARGS = {
    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( Package.DEFAULT_KWARGS, kwargs )
        BasePackage.__init__( self, *args, **joined_kwargs )
        Repository.__init__( self, *args, **joined_kwargs )

        self.BasePackage_init()
