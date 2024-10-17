import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_and_find_broken_links(url):
    # Richiede la pagina principale
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return f"Errore: impossibile accedere al sito {url}"
    except requests.RequestException as e:
        return f"Errore durante il collegamento a {url}: {e}"

    # Analizza il contenuto HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    
    broken_links = []
    
    for link in links:
        href = link['href']
        # Unisce gli URL relativi al dominio base
        full_url = urljoin(url, href)
        
        try:
            link_response = requests.get(full_url)
            if link_response.status_code != 200:
                broken_links.append((full_url, link_response.status_code))
        except requests.RequestException:
            broken_links.append((full_url, 'No Response'))
    
    if broken_links:
        report = "Bug report: Link non funzionanti trovati:\n"
        for broken_link, status in broken_links:
            report += f"{broken_link} - Status: {status}\n"
        return report
    else:
        return "Tutti i link funzionano correttamente!"

# Esempio di utilizzo
url = 'https://it.wikipedia.org/wiki/Pagina_principale'
report = crawl_and_find_broken_links(url)
print(report)
