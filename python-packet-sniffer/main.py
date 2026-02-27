from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    conteudo = """
    <h1>Hotel</h1>
    <form action="/login" method="post">
        Usuario: <input type="text" name="usuario">
        Senha: <input type="password" name="senha">
        <input type="submit" value="login">
    </form>
    """
    return conteudo

@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    return f"{usuario} logado com sucesso!"


if __name__ == '__main__':
    app.run()