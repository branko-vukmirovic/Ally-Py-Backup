'''
Created on Jul 8, 2011

@package: ally core
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the decoding handler.
'''

from ally.container.ioc import injected
from ally.core.spec.codes import UNKNOWN_DECODING
from ally.core.spec.server import IProcessor, ProcessorsChain, Request, Response, \
    Processors, ContentRequest
from ally.api.config import INSERT, UPDATE
from ally.core.spec.context import Transform, ContentSpec

# --------------------------------------------------------------------

@injected
class DecodingHandler(IProcessor):
    '''
    Implementation for a processor that provides the decoding of the request input content based on the requested 
    format to actual arguments that can be used in calling the invoke. The decoding handler relays on a processors
    chain that contains the decoding processors.
    
    Provides on request: [content.charSet], [content.contentLanguage], [content.contentConverter]
    Provides on response: NA
    
    Requires on request: method, [content.contentType], accContentTypes
    Requires on response: [code]
    '''

    decodings = Processors
    # The decodings processors, if a processor is successful in the decoding process it has to stop the chain
    # execution.
    charSetDefault = str
    # The default character set to be used if none provided for the content.

    def __init__(self):
        assert isinstance(self.decodings, Processors), 'Invalid decodings processors %s' % self.decodings
        assert isinstance(self.charSetDefault, str), 'Invalid default character set %s' % self.charSetDefault

    def process(self, req, rsp, chain):
        '''
        @see: IProcessor.process
        '''
        assert isinstance(req, Request), 'Invalid request %s' % req
        assert isinstance(rsp, Response), 'Invalid response %s' % rsp
        assert isinstance(chain, ProcessorsChain), 'Invalid processors chain %s' % chain
        assert isinstance(rsp, Transform), 'Invalid transform response %s' % rsp
        assert isinstance(rsp, ContentSpec), 'Invalid content response %s' % rsp
        content = req.content
        assert isinstance(content, ContentRequest), 'Invalid content on request %s' % content

        if req.method in (INSERT, UPDATE):
            if not content.charSet: content.charSet = rsp.charSet de verificat cine ar pune aici valori
            si de asemenea toate decodingurile
            if not content.language: content.language = rsp.language

            decodingChain = self.decodings.newChain()
            assert isinstance(decodingChain, ProcessorsChain)
            decodingChain.process(req, rsp)

            if rsp.code and not rsp.code.isSuccess:
                # A failure occurred in decoding, stopping chain execution
                return

            if decodingChain.isConsumed():
                rsp.setCode(UNKNOWN_DECODING, 'Content type \'%s\' not supported for decoding' % content.contentType)
                return

        chain.proceed()
