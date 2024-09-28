from flask import Flask

app = Flask(__name__)
import routes.klotski
import routes.colony
import routes.kazuma
import routes.wordle
import routes.bugfixer
import routes.bugfixer2
import routes.bullet
import routes.programmer
import routes.mini_interpreter
# import routes.mailtime