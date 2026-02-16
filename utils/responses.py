from flask import jsonify
def error(msg,code): return jsonify({"error":msg}),code
