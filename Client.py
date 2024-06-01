import requests
from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

# Função para enviar uma requisição SOAP para um serviço específico
def send_soap_request(service_name, number, services):
    headers = {'Content-Type': 'text/xml'}

    if service_name in services:
        # Obtém a URL do serviço com base no nome do serviço
        service_url = services[service_name]['endpoint']
        # Cria um envelope SOAP com o corpo contendo a chamada de função e seus argumentos
        envelope = Element('soapenv:Envelope', {'xmlns:soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'})
        body = SubElement(envelope, 'soapenv:Body')
        function_call = SubElement(body, service_name)
        argument = SubElement(function_call, 'number')
        argument.text = str(number)
        body_text = tostring(envelope, encoding='utf-8')
        # Envia a requisição SOAP para o serviço e retorna a resposta
        response = requests.post(service_url, data=body_text, headers=headers)
        return response.text
    else:
        print("Serviço não disponível.")
        return None

# Função para selecionar um serviço da lista de serviços disponíveis
def select_service(services):
    print("\nServiços disponíveis:")
    for idx, service_name in enumerate(services, start=1):
        print(f"{idx}. {service_name}: {services[service_name]['description']}")
    choice = input("Escolha o serviço (digite o número correspondente): ")
    return choice

# Função para analisar a resposta SOAP e extrair o resultado
def parse_soap_response(response_text):
    root = fromstring(response_text)
    namespace = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/'}
    body = root.find('.//soapenv:Body', namespace)
    if body is not None:
        response_element = body.find('.//Response')
        if response_element is not None:
            return response_element.text
    return None

# Função para obter a lista de serviços
def get_services(url):
    response = requests.get(f"{url}/services")
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter serviços .")
        return None

# Função para selecionar um serviço da lista de serviços disponíveis
def select_service(services):
    print("\n--- Serviços Disponíveis ---")
    for idx, service_name in enumerate(services, start=1):
        print(f"{idx}. {service_name}: {services[service_name]['description']}")
    print("---------------------------")

    # Obtém a escolha do utilizador
    while True:
        choice = input("Escolha o serviço (digite o número correspondente): ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(services):
                # Obtém o nome do serviço com base na escolha do utilizador
                service_name = list(services.keys())[choice - 1]
                return service_name
            else:
                print("Escolha inválida. Por favor, escolha um número da lista.\n")
        except ValueError:
            print("Por favor, insira um número válido.\n")

# Função para obter a entrada do utilizador para o número
def get_number():
    while True:
        x_input = input("\nInsira um valor entre 1 e 9 (ou digite 0 para sair): ")
        if x_input == '0':
            print("Fechar o programa. Obrigado por usar os nossos serviços!\n")
            exit()

        try:
            x = int(x_input)
            if 1 <= x <= 9:
                return x
            else:
                print("O valor inserido está fora do intervalo permitido (1-9).\n")
        except ValueError:
            print("Por favor, insira um valor inteiro válido.\n")

# Função para repetir ou encerrar o programa com base na escolha do utilizador
def repeat_tabuada():
    while True:
        repeat_tabuada = input("\nDeseja repetir o programa? (S/N): ").strip().lower()
        if repeat_tabuada == 'n':
            print("Fechar o programa. Obrigado por usar os nossos serviços!\n")
            exit()
        elif repeat_tabuada == 's':
            return True
        else:
            print("Por favor, insira 'S' para sim ou 'N' para não.\n")

if __name__ == "__main__":
    url_publhisher = 'http://localhost:8001'

    # Obtém a lista de serviços
    services = get_services(url_publhisher)
    if services:
        while True:
            # Solicita ao utilizador que selecione um serviço
            service_name = select_service(services)
            # Obtém um número do utilizador
            x = get_number()
            # Envia uma requisição SOAP para o serviço selecionado
            response_text = send_soap_request(service_name, x, services)
            # Analisa a resposta SOAP e imprime o resultado
            result = parse_soap_response(response_text)
            print(f"\nResultado da Consulta para o Serviço '{service_name}':\n {result}")
            # Verifica se o utilizador  deseja repetir o programa
            if not repeat_tabuada():
                break
    else:
        print("Não foi possível obter os serviços.")