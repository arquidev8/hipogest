# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# driver = webdriver.Chrome()
#
# page = 1
# url = "http://realestate.hipoges.com/es/point/map/venta/pisos-y-casas/espana/5/40.416775/-3.70379?page=" + str(page)
# driver.get(url)
# time.sleep(45)
#
# while True:
#     # Obtener los enlaces
#     urls = driver.find_elements(By.XPATH, "//article[@class='flex rounded-hp border border-b-0 bg-white border-hp-gray flex-col w-full h-full']//a")
#     for url in urls:
#         links = url.get_attribute('href')
#         print(links)
#
#     # Actualizar la variable page y la URL para la siguiente página
#     page += 1
#     url = "http://realestate.hipoges.com/es/point/map/venta/pisos-y-casas/espana/5/40.416775/-3.70379?page=" + str(page)
#     try:
#         driver.get(url)
#     except Exception as e:
#         print("Error al obtener la página: " + str(e))
#         continue
#     time.sleep(45)  # tiempo de espera para cargar la página
#
# driver.quit()

import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

page = 1
url = "http://realestate.hipoges.com/es/point/map/venta/pisos-y-casas/espana/5/40.416775/-3.70379?page=" + str(page)
driver.get(url)
time.sleep(45)

# Creamos un DataFrame
df = pd.DataFrame(columns=['url'])

while True:
    # Obtener los enlaces
    urls = driver.find_elements(By.XPATH,
                                "//article[@class='flex rounded-hp border border-b-0 bg-white border-hp-gray flex-col w-full h-full']//a")

    for url in urls:
        links = url.get_attribute('href')

        # Añadimos la URL a nuestro DataFrame
        df = df._append({'url': links}, ignore_index=True)

    # Si se han obtenido menos de 20 URLS, significa que no hay más en la página y terminamos con el scraping
    if len(urls) < 20:
        break

    # Actualizar la variable page y la URL para la siguiente página
    page += 1
    url = "http://realestate.hipoges.com/es/point/map/venta/pisos-y-casas/espana/5/40.416775/-3.70379?page=" + str(page)
    try:
        driver.get(url)
    except Exception as e:
        print("Error al obtener la página: " + str(e))
        continue

    time.sleep(45)  # tiempo de espera para cargar la página

    # Si tenemos 20 URLs, guardamos en un archivo XLSX
    if len(df) == 20:
        # Buscamos si hay archivos previos y cargamos el contenido
        prev_files = [f for f in os.listdir('.') if f.startswith('Urls') and f.endswith('.xlsx') and os.path.isfile(f)]
        if prev_files:
            prev_df = pd.concat([pd.read_excel(f) for f in prev_files])
            prev_df = prev_df.drop_duplicates().reset_index(drop=True)
            df = pd.concat([prev_df, df], ignore_index=True)

        # Creamos un archivo XLSX para guardar las URLs
        writer = pd.ExcelWriter('Urls{}.xlsx'.format(page), engine='xlsxwriter')

        # Guardamos las URLs en una hoja de cálculo
        df.to_excel(writer, sheet_name='Urls{}'.format(page), index=False)

        # Cerramos el archivo XLSX
        writer._save()

        # Reseteamos el DataFrame para la siguiente página
        df = df.iloc[0:0]

# Guardamos las últimas URLs en un archivo XLSX si no tienen 20
if not df.empty:
    # Buscamos si hay archivos previos y cargamos el contenido
    prev_files = [f for f in os.listdir('.') if f.startswith('Urls') and f.endswith('.xlsx') and os.path.isfile(f)]
    if prev_files:
        prev_df = pd.concat([pd.read_excel(f) for f in prev_files])
        prev_df = prev_df.drop_duplicates().reset_index(drop=True)
        df = pd.concat([prev_df, df], ignore_index=True)

    writer = pd.ExcelWriter('Urls{}.xlsx'.format(page + 1), engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Urls{}'.format(page + 1), index=False)
    writer.save()

driver.quit()