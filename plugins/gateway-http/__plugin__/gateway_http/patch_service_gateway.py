'''
Created on Jan 23, 2013

@package: gateway http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the gateway service setup patch.
'''

from __setup__.ally_core_http.processor import resources_root_uri
from ally.container import ioc
import logging

# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------

try: from __setup__ import ally_gateway
except ImportError: log.info('No gateway service available, thus no need to publish the gateway data')
else:
    ally_gateway = ally_gateway  # Just to avoid the import warning
    # ----------------------------------------------------------------
    
    from __setup__.ally_gateway.processor import gateway_uri
    
    @ioc.replace(gateway_uri)
    def gateway_uri_anonymous():
        '''
        The anonymous gateway URI.
        '''
        return resources_root_uri() % 'Gateway'

