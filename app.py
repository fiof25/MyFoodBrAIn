from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai
import os
import dotenv

dotenv.load_dotenv()
app = Flask(__name__)
app.debug = True
CORS(app)

# Set up your OpenAI API key
app.config.from_pyfile('settings.py')
openai.api_key = os.getenv("OPENAI_API_KEY")

print(openai.api_key)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/getrecipe', methods=['POST'])
def get_recipe():
    data = request.get_json()
    print(data)
    ingredients = data.get('ingredients', [])
    print(ingredients)
    
    # Use OpenAI API to process the ingredients and generate a response
    response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": f"Create a recipe using the following ingredients: {', '.join(ingredients)}"}],
            max_tokens=1500,
        )
    recipe = response.choices[0].message.content.strip()
    print(recipe)

    # Format the recipe for better readability
    formatted_recipe = recipe.replace("\n", "<br>")

    response_data = {
        'message': 'Recipe generated successfully!',
        'recipe': formatted_recipe
    }
    # try:
        
    #     }
    # except Exception as e:
    #     response_data = {
    #         'message': 'Error generating recipe',
    #         'error': str(e)
    #     }
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return jsonify(response_data)

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True)
