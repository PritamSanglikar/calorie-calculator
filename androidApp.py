from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image_data, prompt])
    return response.text

@app.route("/calculate_calories", methods=["POST"])
def calculate_calories():
    try:
        input_text = request.json.get("input")
        image_base64 = request.json.get("image")

        # Decode the base64 image
        image_data = BytesIO(base64.b64decode(image_base64))
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": image_data.getvalue()
            }
        ]

        prompt = """
        You are an expert in nutritionist where you need to see the food items from the image
        and calculate the total calories, also provide the details of every food items with calories intake.
        """

        # Generate response
        response_text = get_gemini_response(input_text, image_parts, prompt)
        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
