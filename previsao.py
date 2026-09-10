import requests
import json
from datetime import datetime, timedelta, timezone

# Coordenadas de São Sebastião - SP
LAT = -23.8269
LON = -45.4243

def obter_dados():
    # Adicionado: wind_gusts_10m (rajadas) e visibility (visibilidade em metros)
    url_clima = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=temperature_2m,precipitation_probability,precipitation,wind_speed_10m,wind_direction_10m,wind_gusts_10m,visibility&timezone=America%2FSao_Paulo&forecast_days=2"

    # Adicionado: wave_period (período das ondas)
    url_mar = f"https://marine-api.open-meteo.com/v1/marine?latitude={LAT}&longitude={LON}&hourly=wave_height,wave_direction,wave_period&timezone=America%2FSao_Paulo&forecast_days=2"

    print("Buscando dados climáticos e marítimos completos...")
    resp_clima = requests.get(url_clima).json()
    resp_mar = requests.get(url_mar).json()

    # Extraindo dados de Clima
    horas = resp_clima['hourly']['time']
    temp = resp_clima['hourly']['temperature_2m']
    chuva_prob = resp_clima['hourly']['precipitation_probability']
    chuva_vol = resp_clima['hourly']['precipitation']
    vento_vel = resp_clima['hourly']['wind_speed_10m']
    vento_dir = resp_clima['hourly']['wind_direction_10m']
    vento_rajada = resp_clima['hourly']['wind_gusts_10m']
    visibilidade = resp_clima['hourly']['visibility']

    # Extraindo dados Marítimos
    onda_alt = resp_mar['hourly']['wave_height']
    onda_dir = resp_mar['hourly']['wave_direction']
    onda_per = resp_mar['hourly']['wave_period']

    # Força o fuso horário do Brasil (UTC-3) ignorando a hora do servidor do GitHub
    fuso_br = timezone(timedelta(hours=-3))
    agora_str = datetime.now(fuso_br).strftime("%Y-%m-%dT%H:00")

    relatorio = []
    horas_coletadas = 0

    for i in range(len(horas)):
        hora_atual = horas[i]

        if hora_atual >= agora_str:


            registro = {
                "data_hora": hora_atual,
                "temperatura_c": temp[i],
                "chance_chuva_pct": chuva_prob[i],
                "volume_chuva_mm": chuva_vol[i],
                "visibilidade_m": visibilidade[i],
                "vento_kmh": vento_vel[i],
                "vento_rajada_kmh": vento_rajada[i],
                "vento_direcao_graus": vento_dir[i],
                "onda_altura_m": onda_alt[i],
                "onda_periodo_s": onda_per[i],
                "onda_direcao_graus": onda_dir[i],

            }
            relatorio.append(registro)
            horas_coletadas += 1

            if horas_coletadas == 24:
                break

    return relatorio


def salvar_json(dados, nome_arquivo="previsao_sao_sebastiao.json"):
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)
    print(f"Relatório de 24h gerado com sucesso: {nome_arquivo}")


if __name__ == "__main__":
    dados_processados = obter_dados()
    salvar_json(dados_processados)