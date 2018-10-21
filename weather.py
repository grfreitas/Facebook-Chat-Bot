from requests import get

def get_weather(location, climatempo_token):
    id_call = 'http://apiadvisor.climatempo.com.br/api/v1/locale/city?name={}&token={}'.format(location, climatempo_token)

    if len(get(id_call).json()) > 0:
        id = get(id_call).json()[0]['id']

        weather_call = 'http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{}/current?token={}'.format(id, climatempo_token)
        weather = get(weather_call).json()

        temperature = weather['data']['temperature']
        condition   = weather['data']['condition']
        humidity    = weather['data']['humidity']
        location    = weather['name'] + '/' + weather['state']

        return 'Em {} está fazendo {} graus Celsius, umidade relativa de {}% e com condição de {}'.format(location, temperature, humidity, condition.lower())
    else:
        return 'Cidade Inválida! Por favor, tente novamente :)'