# url imports
import cookielib
import urllib
import urllib2
from StringIO import StringIO

# ocr imports
from PIL import Image
import tesseract  # http://github.com/jbochi/python-tesseract

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

    def _format(self, im, format):
        if format == 'image':
            return im
        elif format == 'text' or format == 'boxes':
            boxes = (format == 'boxes')
            return self.to_text(im, boxes)

    def improve_image(self, im):
        # Convert the image to grayscale
        im = im.convert('L')

        # Apply a 175 threshold
        im = im.point(lambda i: i if i < 175 else 255)

        # Scale it by 300%
        (width, height) = im.size
        im = im.resize((width*3, height*3), Image.BICUBIC)

        return im

    def to_text(self, im, boxes=False, improve=True, lang='por'):
        if improve:
            im = self.improve_image(im)
        if boxes:
            lang=None
        return tesseract.image_to_string(im, lang=lang, boxes=boxes).decode('utf-8')

    def consulta(self, endereco, format=None):
        """Consulta e retorna resultados em imagem/texto/boxes/nada"""
        self._url_open('consultaLogradouroAction.do', {'relaxation': endereco,
                                                      'Metodo': 'listaLogradouro',
                                                      'TipoConsulta': 'relaxation',
                                                      'StartRow': '1',
                                                      'EndRow': '10'})

        if format:
            im = self._url_open_image('ListaLogradouroImage')
            return self._format(im, format)

    def detalhe(self, posicao=1, format='text'):
        """Retorna imagem/texto/boxes do resultado detalhado"""
        improve = (format != 'image')
        im = self._url_open_image('ListaDetalheCEPImage?TipoCep=2&Posicao=%d' % posicao)
        return self._format(im, format)


if __name__ == '__main__':
    c = Correios()

    # exemplo com imagens
    c.consulta('91370000', format='image').show()
    c.detalhe(format='image').show()

    # exemplo com texto
    print c.consulta('91370000', format='text')
    print c.detalhe(format='text')
