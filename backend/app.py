from flask import Flask, jsonify, request
from flask_cors import CORS
from grammar.grammar import Parser
from environment.ast import Ast
from environment.environment import Environment
from environment.generator import Generator
from environment.execute import rootExecuter

app = Flask(__name__)
CORS(app)

@app.route("/run", methods=["POST"])
def run():
    code = request.get_json()['code']
    print(code)
    symbols = {}
    errors = []

    ast = Ast()
    env = Environment(None, 'Global')
    gen = Generator()
    parser = Parser()
    instructions = parser.interpret(code)
    errors = parser.getErrors()

    rootExecuter(instructions, ast, env, gen)
    
    errors.extend(ast.getErrors())
    errors_json = [error.__dict__ for error in errors]

    return jsonify({"console":gen.get_final_code()+"\n# === Codigo ejecutado exitosamente. ===","errors": errors_json})

if __name__ == '__main__':
    app.run(debug=True)