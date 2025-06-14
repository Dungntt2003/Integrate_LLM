from flask import Flask, request, jsonify # type: ignore
from chroma_query import search_with_hybrid
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

        results = search_with_hybrid(query=destination)
        # print(f"Search results: {results}")
        related_chunks = results["documents"] if results and "documents" in results else []
        # print(f"Related chunks: {related_chunks}")
        if not related_chunks:
            return jsonify({"error": "No related context found from ChromaDB"}), 404

        ai_response = get_ai_response(user_input, related_chunks)

        return jsonify({"description": ai_response})

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
