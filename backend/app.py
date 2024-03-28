from flask import Flask, jsonify, request
from flask_cors import CORS
from grammar.grammar import Parser
from environment.ast import Ast
from environment.environment import Environment

app = Flask(__name__)
CORS(app)

@app.route("/run", methods=["POST"])
def run():
    code = request.get_json()['code']
    print(code)
    symbols = {}
    errors = []

    env = Environment(None, 'Global')
    ast = Ast()
    parser = Parser()
    instructions = parser.interpret(code)
    errors = parser.getErrors()

    for instruction in instructions:
        instruction.execute(ast, env)
    errors.extend(ast.getErrors())

    return jsonify({"console":ast.getConsole(), "errors":errors})

if __name__ == '__main__':
    app.run(debug=True)