
from flask import Flask,request,render_template,session,g
from datetime import datetime
from exist import db,mail
from sqlalchemy import text
import config
from flask_migrate import Migrate
from blueprints.qa import bp as qa_bp
from blueprints.user import bp as user_bp
from models import Usermodel
app=Flask(__name__)

app.config.from_object(config)

db.init_app(app)
mail.init_app(app)
migrate=Migrate(app,db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)

@app.before_request
def my_before_request():
    user_id=session.get("user_id")
    if user_id:
        user=Usermodel.query.get(user_id)
        setattr(g,"user",user)
    else:
        setattr(g,"user",None)

@app.context_processor
def my_context_processor():
    return {"user":g.user}

if __name__=='_main_':
    app.run()
