from flask import request, jsonify
from flask_restful import Resource
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin

class WebContent(Resource):

    def get(self):
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "URL parameter is missing."}), 400
        clean_text = WebContent.get_clean_text_with_urls(url)
        if not clean_text:
            # revisar estado de error 
            return jsonify({"error": "Failed to fetch and clean the content."}), 500
        return clean_text

    def get_clean_text_with_urls(url):
        try:
            # Make the GET request to the URL
            response = requests.get(url)
            response.raise_for_status()

            # Create a BeautifulSoup object to parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find JSON objects in the HTML
            json_values = []
            for script in soup.find_all("script", {"type": "application/json"}):
                try:
                    json_data = json.loads(script.string)
                    # Extract all values from the JSON object
                    json_values.extend(WebContent.extract_values(json_data))
                except json.JSONDecodeError:
                    pass

            # Extract URLs from the links in the HTML and make them absolute
            base_url = response.url
            links = {link.text: urljoin(base_url, link['href']) for link in soup.find_all('a', href=True)}

            # Combine the plain text, JSON values, and URLs with associated text
            combined_text = ""
            for text in soup.stripped_strings:
                combined_text += text + " "
                if text in links:
                    combined_text += f"[{links[text]}] "
            combined_text += " ".join(json_values)

            return combined_text

        except requests.exceptions.RequestException as e:
            print("Error making the request:", e)
            return None

    def extract_values(obj):
        """Recursively extract all values from a JSON object."""
        if isinstance(obj, dict):
            for value in obj.values():
                yield from WebContent.extract_values(value)
        elif isinstance(obj, list):
            for item in obj:
                yield from WebContent.extract_values(item)
        else:
            yield str(obj)

    

