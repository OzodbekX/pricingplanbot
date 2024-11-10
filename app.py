from flask import Flask, request

from bot import handle_update

app = Flask(__name__)


@app.route(f"/7128849436:AAE6uhEK6_kViChviOAkfr-NNlAcCEx5wiU", methods=["POST"])
def telegram_webhook():
    if request.method == "POST":
        update = request.get_json()
        handle_update()
    return "ok"


# if __name__ == '__main__':
#     app.run(port=5000, debug=True)
if __name__ == '__main__':
    handle_update()
