from pypi_builder import BasePackage
from repository_generator.Templates.jameskabbes.jameskabbes import Repository 
import dir_ops as do
import py_starter as ps
import user_profile

from pypi_builder.Templates.default.default import Package as default_Package


class Package( BasePackage, Repository ):

    template_Dir = default_Package.template_Dir

    DEFAULT_KWARGS = {
        'author': user_profile.profile.name,
        'author_email': user_profile.profile.email
    }

    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( Package.DEFAULT_KWARGS, kwargs )
        BasePackage.__init__( self, *args, **kwargs )
        Repository.__init__( self, *args, **kwargs )

        self.gen_atts( joined_kwargs )
        self.BasePackage_init()

    def gen_atts( self, joined_kwargs ):

        keys = ['name','url_documentation']

        for key in keys:
            if key not in joined_kwargs:
                
                if key == 'name':
                    value = 'kabbes_' + self.name
                elif key == 'url_documentation':
                    value = self.url_pages

                self.set_attr( key, value )

