pip install -r requirements.txt
source Voto/Scripts/activate
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_ENV=development
flask run