import requests
from bs4 import BeautifulSoup

# Función que realiza el scraping de un producto en Amazon
def scrape_product(url, search_query):

    response = requests.get(url)
    content = response.text

    soup = BeautifulSoup(content, 'html.parser')

    product_elements = soup.find_all('h2', class_='poly-box poly-component__title')
    price_elements = soup.find_all('span', class_='andes-money-amount')

    if not product_elements:
        print("No se encontraron productos en la búsqueda.")
    else:
        print(f"Se encontraron {len(product_elements)} productos.")

    products = []

    for product_element in product_elements:
        title_element = product_element.find('a')  # Si el título está dentro de un <a> en este contenedor
        price_element = product_element.find_next('span', class_='andes-money-amount')  # Encuentra el siguiente elemento de precio

        # Verificar si encontramos ambos elementos
        if title_element and price_element:
            title = title_element.get_text(strip=True)
            price = price_element.get_text(strip=True)
            products.append({'title': title, 'price': price})

    # Imprimir los productos encontrados
    for product in products:
       print(f"Título: {product['title']}, Precio: {product['price']}")

    # Filtrar productos que contienen la búsqueda especificada en el título
    # matching_products = [product for product in products if search_query.lower() in product['title'].lower()]
    matching_products = [
    product for product in products 
    if any(word.lower() in product['title'].lower() for word in search_query.split())
    ]
    # print("-----------------------")
    total_price = 0.0 
    count = 0  

    for product in matching_products:
        # print(f"Título: {product['title']}, Precio: {product['price']}")
        try:
            clean_price = product['price'].replace("$", "").replace(".", "").replace(",", "")
            price = float(clean_price)
            total_price += price
            count += 1
        except ValueError:
            print(f"Error: El precio '{product['price']}' no es un número válido y será ignorado.")


    if count > 0:
        average_price = total_price / count
        # print(f"El promedio de los precios es: ${average_price:,.2f}")
    else:
        return {
        "Search": "No se encontraron productos que coincidan con la búsqueda especificada.",
        "Average price": 0.0
    }

    # Devolver los datos scrapeados
    return {
        "Search": search_query,
        "Average price": average_price
    }
