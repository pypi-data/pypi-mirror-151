from repository_generator import BaseRepository
import py_starter as ps
import datetime
import configparser

class BasePackage( BaseRepository ):

    PYPI_BASE_URL = 'https://pypi.org/project/'
    CONFIG_ATTS_NEEDED = ['author','version','name']

    DEFAULT_KWARGS = {
        'version': '0.1.0',
        'year': str(datetime.datetime.now().year)
    }
    def __init__( self, *args, **kwargs ):

        joined_kwargs = ps.merge_dicts( BasePackage.DEFAULT_KWARGS, kwargs )
        BaseRepository.__init__( self, *args, **joined_kwargs )

        self.config_Path = self.Dir.join_Path( path = 'setup.cfg' )
        self.parse_config( atts = self.CONFIG_ATTS_NEEDED )

    def BasePackage_init( self ):

        if not self.has_attr( 'url_home' ):
            self.set_attr( 'url_home', BasePackage.PYPI_BASE_URL + self.get_attr('name') )

    def parse_config( self, section = 'metadata', atts = [] ):

        if self.config_Path.exists():
            
            parser = configparser.ConfigParser()
            parser.read( self.config_Path.path ) 

            if parser.has_section( section ):
                for option in atts:
                    if parser.has_option( section, option ):
                        option_value = parser.get( section, option )
                        self.set_attr( option, option_value )
       