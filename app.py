from flask import Flask, redirect, request, render_template, flash
from flask_debugtoolbar import DebugToolbarExtension
import surveys


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "secretz"
debug = DebugToolbarExtension()

RESPONSES = []
CURRENT_QUESTION = 0


@app.route('/')
def home():
    # temp
    global CURRENT_QUESTION
    RESPONSES.clear()
    CURRENT_QUESTION = 0

    return render_template('survey-select.html', surveys=surveys.surveys)


@app.route('/questions/<survey>/<q>')
def questions(survey, q):
    global CURRENT_QUESTION

    if not check_valid_question(survey, int(q)):
        flash("Tsk, tsk. Answer THIS one please.")
        return redirect(f'/questions/{survey}/{CURRENT_QUESTION}')

    if CURRENT_QUESTION >= len(surveys.surveys[survey].questions):
        CURRENT_QUESTION = 0
        return redirect('/complete')

    return render_template('survey.html', id=survey, survey=surveys.surveys[survey], q=CURRENT_QUESTION)


@app.route('/answer/<survey>/<q>', methods=['POST'])
def answer(survey, q):
    global CURRENT_QUESTION

    if not check_valid_question(survey, int(q)):
        flash("Tsk, tsk. Answer THIS one please.")
        return redirect(f'/questions/{survey}/{CURRENT_QUESTION}')

    answer = request.form['yes_or_no']
    record_answer(survey, q, answer)

    print(RESPONSES)

    CURRENT_QUESTION += 1
    return redirect(f'/questions/{survey}/{CURRENT_QUESTION}')


@ app.route('/complete')
def complete():
    return render_template('complete.html')


def record_answer(survey, q, answer):
    RESPONSES.append(answer)
    return


def check_valid_question(survey, q):
    global CURRENT_QUESTION
    if q == CURRENT_QUESTION:
        return True
