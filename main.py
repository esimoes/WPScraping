from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import csv

# Ruta del archivo chromedriver
PATH = "D:\Portable APPs\chromedriver-win64\chromedriver.exe"
# URL del blog
SITEMAP_URL = "https://chiptecno.com/post-sitemap.xml"

# Configurar el servicio del driver de Chrome
service = Service(PATH)
service.start()

# Configurar opciones del navegador (puedes agregar opciones adicionales si es necesario)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecución en modo headless (sin interfaz gráfica)
options.add_argument("--no-sandbox")  # Opción de seguridad para evitar el modo sandbox

# Iniciar el navegador
driver = webdriver.Chrome(service=service, options=options)

# Obtener el contenido de la página
driver.get(SITEMAP_URL)
page_content = driver.page_source

# Parsear el contenido HTML con BeautifulSoup
soup = BeautifulSoup(page_content, "html.parser")

# Encontrar la tabla con id="sitemap"
sitemap_table = soup.find("table", {"id": "sitemap"})

if sitemap_table:
    # Abrir el archivo CSV en modo de escritura
    with open("chiptecno_blog.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # Escribir la cabecera del archivo CSV
        writer.writerow(["Título", "Cuerpo"])

        # Encontrar todos los enlaces dentro de la tabla
        sitemap_links = sitemap_table.find_all("a", href=True)

        for link in sitemap_links:
            blog_url = link["href"]
            driver.get(blog_url)

            # Obtener el contenido de la nota de blog
            note_content = driver.page_source

            # Parsear el contenido HTML de la nota con BeautifulSoup
            note_soup = BeautifulSoup(note_content, "html.parser")

            # Extraer el título y el cuerpo de la nota
            note_title = note_soup.find("h1", {"class": "tdb-title-text"}).text.strip()
            note_body = note_soup.find("div", {"class": "tdb_single_content"}).text.strip()  # Supongamos que el cuerpo está dentro de un elemento <div> con class="entry-content"
            # Agregar comillas dobles a los valores de note_title y note_body
            note_title = '"' + note_title + '"'
            note_body = '"' + note_body + '"'
            # Escribir los datos en el archivo CSV
            writer.writerow([note_title, note_body])
else:
    print("No se encontró la tabla con id='sitemap' en la página.")

# Cerrar el navegador
driver.quit()
