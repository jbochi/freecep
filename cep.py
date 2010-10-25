import cookielib
import urllib
import urllib2
from StringIO import StringIO
from PIL import Image

URL = 'http://www.buscacep.correios.com.br/servicos/dnec/'

class Correios():
    def __init__(self, proxy=None):
        cj = cookielib.LWPCookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cj)
        if proxy:
            proxy_handler = urllib2.ProxyHandler({
                'http': proxy,
                'https': proxy,
            })
            opener = urllib2.build_opener(proxy_handler, cookie_handler)
        else:
            opener = urllib2.build_opener(cookie_handler)
        urllib2.install_opener(opener)

    def _url_open(self, url, data=None, headers=None):
        if headers == None:
            headers = {}
            
        headers['User-agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        req = urllib2.Request(URL + url, urllib.urlencode(data) if data else None, headers)
        handle = urllib2.urlopen(req)

        return handle

    def _url_open_image(self, url, data=None, headers=None):
        image_handle = self._url_open(url, data, headers)
        image_string = image_handle.read()
        image_buffer = StringIO(image_string)
        im = Image.open(image_buffer)
        return im    

    def consulta(self, endereco, open_image=False):
        """Retorna imagem com resultados da pesquisa"""
        self._url_open('consultaLogradouroAction.do', {'relaxation': endereco,
                                                      'Metodo': 'listaLogradouro',
                                                      'TipoConsulta': 'relaxation',
                                                      'StartRow': '1',
                                                      'EndRow': '10'})

        if open_image:
            im = self._url_open_image('ListaLogradouroImage?paramx=nullnullnullnullrelaxationnullnull')

            return im

    def detalhe(self, posicao=1):
        """Retorna imagem detalhada do resultado detalhado"""
        return self._url_open_image('ListaDetalheCEPImage?TipoCep=2&Posicao=%d' % posicao)


if __name__ == '__main__':
    c = Correios()
    im = c.consulta('91370000')
    im = c.detalhe()
    im.show()   
