from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring
import json
import requests

class SOAPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Recebe os dados da requisição POST
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        # Extrai o número da requisição SOAP
        number = self.parse_soap_request(post_data)
        if number is not None:
            # Calcula a tabuada do número recebido
            result = self.tabuada_function(number)
            # Cria a resposta SOAP com o resultado da tabuada
            response = self.create_soap_response(result)
            # Envia a resposta para o cliente
            self.send_response(200)
            self.send_header('Content-Type', 'text/xml')
            self.end_headers()
            self.wfile.write(response)
        else:
            # Envia uma resposta de erro se não conseguir extrair o número
            self.send_response(400)
            self.end_headers()

    def parse_soap_request(self, data):
        # Analisa a requisição SOAP e extrai o número
        root = fromstring(data)
        namespace = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'}
        body = root.find('.//soapenv:Body', namespace)
        if body is not None:
            number_element = body.find('.//number')
            if number_element is not None:
                try:
                    number = int(number_element.text)
                    return number
                except ValueError:
                    pass
        return None

    def tabuada_function(self, x):
        # Calcula a tabuada do número fornecido
        result = ""
        for i in range(1, 11):
            result += str(x) + " x " + str(i) + " = " + str(i * x) + "\n"
        return result

    def create_soap_response(self, result):
        # Cria a resposta SOAP com o resultado da tabuada
        envelope = Element('soapenv:Envelope', {'xmlns:soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'})
        body = SubElement(envelope, 'soapenv:Body')
        response = SubElement(body, 'Response')
        response.text = str(result)
        return tostring(envelope, encoding='utf-8')

def send_service_info(url):
    # Envia informações sobre o serviço para o servidor Publisher
    service_info = {
        "name": "Tabuada",
        "description": "Este serviço fornece a tabuada de um número enviado como entrada.",
        "endpoint": f"{url}",
        "methods": ["tabuada"],
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post("http://localhost:8001/register", data=json.dumps(service_info), headers=headers)
    if response.status_code == 200:
        print("Informações do serviço enviadas com sucesso para o servidor Publisher.")
    else:
        print("Erro ao enviar informações do serviço para o servidor Publisher.")

def run(server_class=HTTPServer, handler_class=SOAPRequestHandler, port=8000):
    # Inicia o servidor
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting SOAP server on port {port}...')
    # Envia informações sobre o serviço para o servidor Publisher
    send_service_info(f'http://localhost:{port}')
    # Aguarda e responde às requisições dos clientes
    httpd.serve_forever()

if __name__ == "__main__":
    run()