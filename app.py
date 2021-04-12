# import modules
from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey

# flask setup
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = "passkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# GLOBAL VARIABLES
responses = []
surv = satisfaction_survey


# HOMEPAGE
@app.route('/')
def homepage():
    return render_template('homepage.html', survey_title=surv.title, survey_instructions=surv.instructions)

# NEXT QUESTION GET REQUEST
@app.route('/questions/<qnum>')
def questions_page(qnum):
    title = surv.title
    questions = surv.questions
    answered_q = len(responses)

    if ( (int(qnum) != 0) and (int(qnum) >= len(surv.questions) or int(qnum) != answered_q) ):
        qnum = len(responses)
        if qnum == len(surv.questions):
            flash("You've Answered All The Questions!")
            return redirect('/thank_you')
        else:
            flash("You're not supposed to be on that!")
            return redirect(f'/questions/{qnum}')
    else:
        return render_template("q_template.html", survey_title=title, survey_questions=questions, current_qnum=int(qnum))


# NEXT QUESTION POST REQUEST
@app.route('/questions/<qnum>', methods=["POST"])
def submit_questions(qnum):
    responses.append(request.form)

    if (int(qnum) < len(surv.questions)-1):
        return redirect(f'/questions/{int(qnum)+1}')
    else:
        return redirect('/thank_you')

# THANK YOU PAGE
@app.route('/thank_you')
def thank_you():
    return render_template("thank_you.html")