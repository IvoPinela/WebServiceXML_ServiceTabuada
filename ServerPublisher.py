from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Dicionário para armazenar informações sobre os serviços registrados
services = {}

class ServiceRegistryHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Recebe os dados da requisição POST contendo informações sobre o serviço
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        # Envia uma resposta de sucesso para o cliente
        self.send_response(200)
        self.end_headers()
        # Converte os dados recebidos em formato JSON para um dicionário Python
        service_info = json.loads(post_data)
        # Extrai o nome do serviço do dicionário
        service_name = service_info.get("name")
        # Registra o serviço no dicionário de serviços
        if service_name:
            services[service_name] = service_info
            print(f"Serviço '{service_name}' registrado com sucesso.")
        else:
            print("Erro ao registrar serviço.")

    def do_GET(self):
        # Retorna a lista de serviços registrados em formato JSON em resposta a uma requisição GET
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(services).encode())

def run(server_class=HTTPServer, handler_class=ServiceRegistryHandler, port=8001):
    # Inicia o servidor de registro de serviços
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting Service Registry Server on port {port}...')
    # Aguarda e responde às requisições dos clientes
    httpd.serve_forever()

if __name__ == "__main__":
    run()