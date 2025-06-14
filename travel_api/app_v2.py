from flask import Flask, request, jsonify # type: ignore
from openai_chat import get_ai_response
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/api/generate-description", methods=["POST"])
def generate_description():
    try:
        data = request.get_json()
        user_input = data.get("itinerary", "").strip()
        destination = data.get("destination", "").strip()
        
        if not user_input:
            return jsonify({"error": "No itinerary provided"}), 400
                
        if not destination:
            return jsonify({"error": "No destination provided"}), 400
        ai_response = get_ai_response(user_input, "")

        return jsonify({"description": ai_response})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)