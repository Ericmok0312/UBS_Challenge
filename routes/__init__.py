from flask import Flask

app = Flask(__name__)
import routes.square
import routes.klotski
import routes.colony
import routes.kazuma
import routes.wordle
import routes.bugfixer