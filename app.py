from flask import Flask, request, jsonify
from scraper import scrape_product
from urllib.parse import quote

app = Flask(__name__)

# Definir la ruta para el scraping
@app.route('/scrape', methods=['GET'])
def scrape():
    # Obtener el parámetro 'url' de la query string
    # url = request.args.get('url')
    search_query = request.args.get('search')  # La búsqueda especificada por el usuario
    encoded_query = quote(search_query)
    base_url = "https://listado.mercadolibre.com.co/"
    url = f"{base_url}{encoded_query}#D"
    # Verificar que el parámetro 'url' fue proporcionado
    if not url:
        return jsonify({"error": "Please provide a valid URL"}), 400

    # Llamar a la función scrape_amazon_product para obtener los datos
    data = scrape_product(url, search_query)

    # Devolver la respuesta en formato JSON
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
