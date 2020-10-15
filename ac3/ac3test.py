from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbimpacta:impacta#2020@dbimpacta.postgresql.dbaas.com.br/dbimpacta'
app.debug = True
db = SQLAlchemy(app)


class gh_team(db.Model):
    ra = db.Column(db.Integer, primary_key=True)
    nome_do_aluno = db.Column(db.String(50))
    email_do_aluno = db.Column(db.String(50))
    logradouro = db.Column(db.String(50))
    numero = db.Column(db.String(5))
    cep = db.Column(db.String(10))
    complemento = db.Column(db.String(20))

    def __init__(self, ra, nome_do_aluno, email_do_aluno, logradouro, numero, cep, complemento):
        self.ra = ra
        self.nome_do_aluno = nome_do_aluno
        self.email_do_aluno = email_do_aluno
        self.logradouro = logradouro
        self.numero = numero
        self.cep = cep
        self.complemento = complemento

    def __repr__(self):
        return '<Aluno %r>' % self.nome_do_aluno


@app.route('/')
def index():
    return render_template('add_student.html')


@app.route('/student')
def all_students():
    allStudents = gh_team.query.all()
    # .all() to return everything that matchs this filter
    return render_template('students.html', allStudents=allStudents)


@app.route('/student/<ra>')
def student(ra):
    student = gh_team.query.filter_by(ra=ra).first()
    return render_template('studentProfile.html', student=student)


@app.route('/post_student', methods=['POST'])
def post_student():
    student = gh_team(request.form['ra'], request.form['nome_do_aluno'], request.form['email_do_aluno'],
                      request.form['logradouro'], request.form['numero'], request.form['cep'], request.form['complemento'])
    db.session.add(student)
    db.session.commit()
    return redirect(url_for('all_students'))


@app.route('/del_student', methods=['POST'])
def del_student():
    gh_team.query.filter_by(ra=request.form['ra']).delete()
    db.session.commit()
    return redirect(url_for('all_students'))


@app.route('/edit_student', methods=['POST'])
def edit_student():
    student = gh_team.query.filter_by(ra=request.form['ra']).first()
    student.nome_do_aluno = request.form['nome_do_aluno']
    student.email_do_aluno = request.form['email_do_aluno']
    student.cep = request.form['cep']
    student.numero = request.form['numero']
    student.logradouro = request.form['logradouro']
    db.session.commit()
    return redirect(url_for('all_students'))


if __name__ == "__main__":
    app.run()
