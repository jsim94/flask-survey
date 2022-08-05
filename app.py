from sqlite3 import Cursor
from flask import Flask, Response, redirect, request, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as survey_list


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "secretz"
debug = DebugToolbarExtension()

RESPONSES = 'responses'
CURRENT_QUESTION = 'current_question'
CURRENT_SURVEY = 'current_survey'
SURVEY_RESULTS = 'survey_results'


@app.route('/clear')
def clear_session():
    session.clear()
    print('SESSION CLEARED!')
    return redirect('/')


@app.route('/')
def home():

    if not SURVEY_RESULTS in session:
        session[SURVEY_RESULTS] = {}
    session[CURRENT_QUESTION] = 0
    session.pop(RESPONSES, None)
    session.pop(CURRENT_SURVEY, None)
    session.modified = True

    return render_template('survey-select.html', surveys=survey_list)


@ app.route('/questions/<qid>', methods=['GET', 'POST'])
def questions(qid):

    if request.method == 'POST':
        survey_id = request.form.get('survey_id')

        # DEPRECATED - App now disables button if completed
        # if survey_id in session.get(SURVEY_RESULTS):
        #    print("You've completed this one already!")
        #    return redirect('/')

        session[RESPONSES] = [None] * len(survey_list[survey_id].questions)
        session[CURRENT_SURVEY] = survey_id
        if session[CURRENT_QUESTION] is None:
            return redirect('/')

        return redirect('/questions/0')

    if not CURRENT_SURVEY in session or CURRENT_SURVEY in session[SURVEY_RESULTS]:
        return redirect('/')

    if int(qid) >= len(survey_list[session[CURRENT_SURVEY]].questions):
        flash("Tsk, tsk. Answer THIS one please.")
        return redirect(f'/questions/{session[CURRENT_QUESTION]}')

    return render_template('survey.html', survey=survey_list[session[CURRENT_SURVEY]], q=session[CURRENT_QUESTION])


@ app.route('/answer/<qid>', methods=['POST'])
def answer(qid):

    answer = request.form.get('options')
    comment = request.form.get('comment_box')
    record_answer(int(qid), answer, comment)

    try:
        session[CURRENT_QUESTION] = session[RESPONSES].index(None)
    except:
        return redirect('/complete')

    return redirect(f'/questions/{session[CURRENT_QUESTION]}')


@ app.route('/complete')
def complete():
    try:
        session[SURVEY_RESULTS][session[CURRENT_SURVEY]] = session[RESPONSES]
    except:
        redirect('/')

    session.pop(CURRENT_QUESTION, None)
    session.pop(CURRENT_SURVEY, None)
    return render_template('complete.html')


@app.route('/show-results')
def show_results():
    return render_template('view-results.html', survey_list=survey_list)


def record_answer(qid, answer, comment):
    session[RESPONSES][qid] = (answer, comment)
    session.modified = True
