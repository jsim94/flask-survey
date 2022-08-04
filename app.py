from flask import Flask, redirect, request, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as survey_list


app = Flask(__name__)
app.debug = True

app.config['SECRET_KEY'] = "secretz"
debug = DebugToolbarExtension()

RESPONSES = 'responses'
CURRENT_QUESTION = 'current_question'
CURRENT_SURVEY = 'current_survey'
COMPLETED_SURVEYS = 'completed_surveys'


@app.route('/')
def home():
    session.clear()
    session[CURRENT_QUESTION] = 0

    return render_template('survey-select.html', surveys=survey_list)


@app.route('/questions/<qid>', methods=['GET', 'POST'])
def questions(qid):

    if request.method == 'POST':
        story_id = request.form['storyid']
        session[RESPONSES] = [None] * len(survey_list[story_id].questions)
        session[CURRENT_SURVEY] = story_id
        session[CURRENT_QUESTION] = 0
        return redirect('/questions/0')

    # if survey in session[COMPLETED_SURVEYS]:
    #     print("You've completed this one already!")

    # if not check_valid_question(survey, int(qid)):
    #     flash("Tsk, tsk. Answer THIS one please.")
    #     return redirect(f'/questions/{survey}/{CURRENT_QUESTION}')

    # if session[CURRENT_QUESTION] >= len(survey_list[survey].questions):
    #     CURRENT_QUESTION = 0
    #     return redirect('/complete')

    return render_template('survey.html', survey=survey_list[session[CURRENT_SURVEY]], q=session[CURRENT_QUESTION])


@ app.route('/answer/<qid>', methods=['POST'])
def answer(qid):

    # if not check_valid_question(survey, int(qid)):
    #     flash("Tsk, tsk. Answer THIS one please.")
    #     return redirect(f'/questions/{survey}/{CURRENT_QUESTION}')

    answer = request.form.get('options')
    record_answer(qid, answer)

    CURRENT_QUESTION += 1
    return redirect(f'/questions/{survey}/{CURRENT_QUESTION}')


@ app.route('/complete')
def complete():
    return render_template('complete.html')


def record_answer(qid, answer):
    RESPONSES.append(answer)
    return


def check_valid_question(qid):
    global CURRENT_QUESTION
    if q == CURRENT_QUESTION:
        return True
