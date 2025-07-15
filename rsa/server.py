from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify({"items": ["item1", "item2", "item3"]})

if __name__ == '__main__':
    import ssl

    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='server.crt', keyfile='server.key')
    context.load_verify_locations(cafile='ca.crt')
    context.verify_mode = ssl.CERT_REQUIRED  # Require client certificate

    app.run(host='0.0.0.0', port=5000, ssl_context=context)
