import os

from app.views import app


port = int(os.environ.get("PORT", 5000))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
