import os
import requests 
import shutil
from bs4 import BeautifulSoup

def download_and_compress_pdfs():
    # Caminho do diretório onde os arquivos serão baixados e compactados
    download_dir = r"D:\Intuitive\a-teste"
    os.makedirs(download_dir, exist_ok=True)

    # URL da página onde os arquivos PDF estão localizados
    url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

    # Fazer uma requisição HTTP para obter o conteúdo da página
    print("Acessando o site...")
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Erro ao acessar a página.")
        return

    # Usar BeautifulSoup para fazer o parsing do HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrar todos os links para PDFs
    print("Procurando por links de PDF...")
    pdf_links = soup.find_all("a", href=True)
    pdf_links_to_download = []

    # Filtrar os links que contém 'Anexo I' ou 'Anexo II' no texto
    for link in pdf_links:
        if "Anexo I" in link.get_text() or "Anexo II" in link.get_text():
            pdf_links_to_download.append(link['href'])

    if not pdf_links_to_download:
        print("Nenhum link de PDF encontrado para Anexo I ou II.")
        return

    # Baixar os PDFs
    print(f"Encontrados {len(pdf_links_to_download)} PDF(s). Baixando...")
    downloaded_files = []
    for pdf_url in pdf_links_to_download:
        # Construir o caminho completo para o arquivo PDF
        if not pdf_url.startswith("http"):
            pdf_url = "https://www.gov.br" + pdf_url

        pdf_name = pdf_url.split("/")[-1]
        file_path = os.path.join(download_dir, pdf_name)

        print(f"Baixando: {pdf_name}")
        pdf_response = requests.get(pdf_url)

        if pdf_response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(pdf_response.content)
            downloaded_files.append(file_path)
            print(f"Baixado: {file_path}")
        else:
            print(f"Falha ao baixar o arquivo: {pdf_url}")

    # Compactar os PDFs em um único arquivo ZIP
    if downloaded_files:
        zip_path = os.path.join(download_dir, "anexos_ans.zip")
        print(f"Compactando arquivos em {zip_path}...")
        
        # Corrigido: Removido o 'with' e chamando a função diretamente
        arquivo_zip = shutil.make_archive(zip_path.replace('.zip', ''), 'zip', download_dir)
        print(f"Compressão concluída. Arquivo salvo em: {arquivo_zip}")

        # Opcional: Remover os arquivos PDF baixados
        for file in downloaded_files:
            os.remove(file)
        print("Arquivos PDF removidos.")

if __name__ == "__main__":
    download_and_compress_pdfs()