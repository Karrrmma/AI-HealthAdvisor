from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
from model import retrieve_chunks 
import faiss
import openai
from dotenv import load_dotenv
load_dotenv()

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API")

app = Flask(__name__)
CORS(app)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

@app.route("/api/disease-check", methods=["POST"])
def disease_check():
    data = request.get_json()
    query = data.get("query", "")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    try:
        # Use imported retrieve_chunks function
        retrieved_chunks = retrieve_chunks(query, top_k=3)
        print(f'Retreived CHunks: {retrieved_chunks}')
        
        # Create context for GPT prompt
        context = "\n".join(retrieved_chunks)
        prompt = f"Based on the following information, answer the user's question:\n{context}\n\nQuestion: {query}"
        print(f'Generated Prompt {prompt}')
        # OpenAI API Call
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a medical assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5
        )

        answer = response.choices[0].message.content.strip()
        print(f"OpenAI Response: {answer}")
        return jsonify({"results": answer})

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

    except openai.APIConnectionError as e:
        return jsonify({"error": "Failed to reach OpenAI servers", "details": str(e.__cause__)}), 503
    except openai.RateLimitError as e:
        return jsonify({"error": "Rate limit exceeded. Please slow down your requests."}), 429
    except openai.APIStatusError as e:
        return jsonify({"error": f"API returned status {e.status_code}", "details": e.response.text}), e.status_code
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
