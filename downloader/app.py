from flask import Flask

app = Flask(__name__)

@app.route("/collect")
def main():
  return "Hello Climate!"

if __name__ == '__main__':
  app.run(debug=True)