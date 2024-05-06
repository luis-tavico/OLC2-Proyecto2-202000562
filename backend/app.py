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
    symbols = []
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

    for id, sym in env.tabla.items():
        symbols.append(sym)

    symbols_json = []

    for sym in symbols:
        symbols_json.append({"symbol_type":sym.symbol_type, "id":sym.id, "data_type":sym.data_type.name.lower(), "environment":"Global", "line":sym.line, "column":sym.column})

    return jsonify({"console":gen.get_final_code()+"\n# >>>Fin de codigo.","symbols":symbols_json,"errors":errors_json})

if __name__ == '__main__':
    app.run(debug=True)