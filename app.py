from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL
from send_mail import send_mail

app = Flask(__name__)

url = URL.create(
    drivername="postgresql",
    username="postgres",
    host="localhost",
    password="mysecretpassword",
    database="lexus"
)

engine = create_engine(url, echo=True)
connection = engine.connect()
Base = declarative_base()


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer = Column(String(200), unique=True)
    dealer = Column(String(200))
    rating = Column(Integer, primary_key=True)
    comments = Column(String(200))

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def index():  # put application's code here
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or customer is None or dealer == '' or dealer is None:
            return render_template('index.html', message='SVP veuillez compléter tous les champs du questionnaire')
        if session.query(Feedback).filter_by(customer = customer).count() == 0:
            print(customer, dealer, rating, comments)
            data = Feedback(customer, dealer, rating, comments)
            session.add(data)
            session.commit()
            send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='Vous avez déjà soumis le questionnaire')


if __name__ == '__main__':
    app.run(debug=True)
