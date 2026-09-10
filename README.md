Previsão Marítima - São Sebastião (Back-end)

Repositório responsável pela coleta e processamento de dados meteorológicos e marítimos da cidade de São Sebastião - SP, desenvolvido para o Projeto Integrador (PI).

O sistema consulta a API da Open-Meteo, processa as informações no fuso horário do Brasil (UTC-3) e gera um arquivo JSON limpo e atualizado automaticamente para o consumo da equipe de Front-end.

Como Funciona a Arquitetura

Coleta de Dados: O script previsao.py extrai dados brutos de ventos, ondas, chuvas, temperatura e visibilidade.

O GitHub Actions executa o script automaticamente a cada 3 horas, sincronizado exatamente com o tempo de atualização dos supercomputadores meteorológicos globais.

O resultado é salvo e sobrescrito no arquivo previsao_sao_sebastiao.json, servindo como uma API estática para o site.

Para a Equipe de Front-end (Integração)

O arquivo JSON fornece a matriz de dados puros. Para injetar essas informações no site, utilize o link Raw do arquivo no GitHub dentro de uma requisição nativa.

Exemplo prático em JavaScript:

JavaScript
// Substitua pela URL "Raw" do arquivo previsao_sao_sebastiao.json do seu repositório
const urlPrevisao = 'COLE_O_LINK_RAW_AQUI';

fetch(urlPrevisao)
    .then(resposta => resposta.json())
    .then(dados => {
        // dados[0] representa a hora atual; dados[1] a próxima hora, e assim por diante.
        const agora = dados[0]; 
        
        console.log(`Horário: ${agora.data_hora}`);
        console.log(`Altura da Onda: ${agora.onda_altura_m}m`);
        console.log(`Vento: ${agora.vento_kmh} km/h`);
        
        // Exemplo de manipulação do DOM:
        // document.getElementById('velocidade-vento').innerText = `${agora.vento_kmh} km/h`;
    })
    .catch(erro => console.error("Erro ao carregar a previsão:", erro));
Para Rodar Localmente (Desenvolvimento Back-end)

Se for necessário testar ou evoluir o código Python na sua máquina:

Faça o clone do repositório:
git clone [https://github.com/SEU_USUARIO/PrevisaoMarinaFlow.git](https://github.com/SEU_USUARIO/PrevisaoMarinaFlow.git)

Instale as bibliotecas necessárias:
pip install -r requirements.txt

Execute o script:
python previsao.py
