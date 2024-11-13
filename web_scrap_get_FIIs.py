from playwright.async_api import async_playwright
import math
from dicAtivos import ativos  # Dicionário de ativos
from openpyxl import Workbook
import asyncio
import datetime
import subprocess


async def ipca():
    async with async_playwright() as p:
        # Lança o navegador
        browser = await p.chromium.launch()
        page = await browser.new_page()

        try:
            # Navega até a URL desejada
            await page.goto('https://investidor10.com.br/tesouro-direto')

            # Avalia o conteúdo da página para encontrar o número desejado
            ipca_text = await page.evaluate('''() => {
                // Localiza todos os elementos TD na página
                const tds = Array.from(document.querySelectorAll('td'));

                // Itera sobre os elementos TD para encontrar o que contém o texto "Tesouro IPCA+ 2045"
                for (let i = 0; i < tds.length; i++) {
                    if (tds[i].textContent.includes('Tesouro IPCA+ 2045')) {
                        // Verifica se há um próximo TD
                        if (i + 1 < tds.length) {
                            // Obtém o texto do próximo TD
                            const textoProximoTD = tds[i + 1].textContent.trim();

                            // Encontra o número antes do símbolo %
                            const resultado = textoProximoTD.match(/(\\d+,\\d+)%/);

                            if (resultado) {
                                return resultado[1].trim();
                            } else {
                                return 'Símbolo % ou formato de número não encontrado no texto.';
                            }
                        } else {
                            return 'Não há um próximo TD.';
                        }
                    }
                }
                return 'Elemento TD com o texto "Tesouro IPCA+ 2045" não encontrado.';
            }''')
        except:
            return ""
        await browser.close()
        return ipca_text

async def salvar_valor_xlsx(ativo, tipo,sheet):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(f'https://investidor10.com.br/{tipo}/{ativo}', timeout=120000)
        await page.wait_for_selector('body')

        # Extração de dados de acordo com o tipo (FIIs, Ações, BDRs)
        try:
            if tipo == 'FIIs':
                pvp_value = await page.locator('//*[@id="cards-ticker"]/div[3]/div[2]/span').first.inner_text()
                dy_value = await page.locator('//*[@id="cards-ticker"]/div[2]/div[2]/div/span').first.inner_text()
                ultimo_tipo_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[1]').first.inner_text()
                ultimo_datacom_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[2]').first.inner_text()
                ultimo_pagamento_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[3]').first.inner_text()
                ultimo_dividendo_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[4]').first.inner_text()
                cnpj_value = await page.locator('//*[@id="table-indicators"]/div[2]/div[2]/div/span').first.inner_text()
                tipo_value = await page.locator('//*[@id="table-indicators"]/div[6]/div[2]/div/span').first.inner_text()
                segmento_value = await page.locator('//*[@id="table-indicators"]/div[5]/div[2]/div/span').first.inner_text()
                razao_social_value = await page.locator('//*[@id="table-indicators"]/div[1]/div[2]/div/span').first.inner_text()
                dy_medio5anos_value = await page.locator('//*[@id="dividend-yield-section"]/div/div[2]/h3[2]/span').first.inner_text()

                pl_value = ""
                vpa_value = ""
                lpa_value = ""
                preco_justo = ""
                setor_value = ""

                # Colocar outras variáveis aqui se necessário...

            elif tipo == 'Acoes':
                pvp_value = await page.locator('//*[@id="cards-ticker"]/div[4]/div[2]/span').first.inner_text()
                pl_value = await page.locator('//*[@id="cards-ticker"]/div[3]/div[2]/span').first.inner_text()
                dy_value = await page.locator('//*[@id="cards-ticker"]/div[5]/div[2]/span').first.inner_text()
                ultimo_tipo_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[1]').first.inner_text()
                ultimo_datacom_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[2]').first.inner_text()
                ultimo_pagamento_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[3]').first.inner_text()
                ultimo_dividendo_value = await page.locator('//*[@id="table-dividends-history"]/tbody/tr[1]/td[4]').first.inner_text()
                cnpj_value = await page.locator('//*[@id="data_about"]/div[2]/div/div[1]/table/tbody/tr[2]/td[2]').first.inner_text()
                setor_value = await page.locator('//span[text()="Setor"]/following-sibling::span[1]').first.inner_text()
                segmento_value = await page.locator('//span[text()="Segmento"]/following-sibling::span[1]').first.inner_text()
                razao_social_value = await page.locator('//*[@id="data_about"]/div[2]/div/div[1]/table/tbody/tr[1]/td[2]').first.inner_text()
                dy_medio5anos_value = await page.locator('//*[@id="dividends-section"]/div[1]/div[1]/h3[2]/span').first.inner_text()
                vpa_value = await page.locator('//span[text()="VPA "]/following-sibling::div/span').first.inner_text()
                lpa_value = await page.locator('//span[text()="LPA "]/following-sibling::div/span').first.inner_text()

                try:
                    # Cálculo de Preço Justo
                    if vpa_value and lpa_value:
                        preco_justo = str(round(math.sqrt(22.5 * float(lpa_value.replace(',', '.')) * float(vpa_value.replace(',', '.'))), 2)).replace('.', ',')
                    else:
                        preco_justo = '-'
                except:
                    preco_justo = '-'
            # Adicionar tratamento para BDRs se necessário...
            try:   
                # Escrever no arquivo Excel
                print([ativo, tipo, pvp_value, pl_value, dy_value, ultimo_tipo_value, ultimo_datacom_value, ultimo_pagamento_value, ultimo_dividendo_value, cnpj_value, setor_value, segmento_value, razao_social_value, dy_medio5anos_value, vpa_value, lpa_value, preco_justo])
                sheet.append([ativo, tipo, pvp_value, pl_value, dy_value, ultimo_tipo_value, ultimo_datacom_value, ultimo_pagamento_value, ultimo_dividendo_value, cnpj_value, setor_value, segmento_value, razao_social_value, dy_medio5anos_value, vpa_value, lpa_value, preco_justo])
                print(f"Valores de {ativo} salvos no arquivo XLSX")
            except Exception as e:
                print(f"Erro ao escrever {ativo}: {e}")


        except Exception as e:
            print(f"Erro ao processar {ativo}: {e}")

        finally:
            await browser.close()

async def processar_ativos(ativos):
    wb = Workbook()
    sheet = wb.active

    # Obter data e hora atuais
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #ipca_text = ""

    ipca_text = await ipca()
    print(ipca_text)
    sheet.append([f'DataColeta:', data_hora, f'IPCA:', ipca_text])

    # Adicionar títulos das colunas
    sheet.append(["Ativo", "Tipo", "P/VP", "P/L", "DY", "DY_Tipo", "DY_DataCom", "DY_Pagamento",
                 "Último Dividendo", "CNPJ", "Setor", "Segmento", "Razão Social", "DY Médio 5 Anos", "VPA", "LPA", "Preço Justo"])

    """ # Processar cada ativo
    tasks = [salvar_valor_xlsx(ativo, tipo, sheet) for ativo, tipo in ativos.items()]
    await asyncio.gather(*tasks) """
    for ativo, tipo in ativos.items():
        await salvar_valor_xlsx(ativo, tipo, sheet)

    # Salvar o arquivo XLSX localmente
    # Caminho temporário
    local_file_path = '/tmp/ativos3.xlsx'
    
    wb = Workbook()
    wb.save(local_file_path)
    
    # Imprime caminho do arquivo salvo
    print(f"Arquivo salvo em: {local_file_path}")
    
if __name__ == "__main__":
    asyncio.run(processar_ativos(ativos))
