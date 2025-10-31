from app import create_app
import os
app = create_app()

from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    app.run(debug=os.getenv("DEBUG", "True") == "True", port=int(os.getenv("PORT", 8080)), host="0.0.0.0")