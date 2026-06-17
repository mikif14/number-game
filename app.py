from flask import Flask, render_template, request, session, redirect
import random

app = Flask(__name__)
app.secret_key = "secret-key-123"

LOWEST = 1
HIGHEST = 100
MAX_ATTEMPTS = 7


def init_game():
    session["secret"] = random.randint(LOWEST, HIGHEST)
    session["attempts"] = 0
    session["game_over"] = False
    session["guesses"] = []


@app.route("/", methods=["GET", "POST"])
def index():

    if "secret" not in session:
        init_game()

    if "attempts" not in session:
        session["attempts"] = 0

    if "game_over" not in session:
        session["game_over"] = False

    if "guesses" not in session:
        session["guesses"] = []

    message = ""
    feedback = ""

    if request.method == "POST" and not session["game_over"]:

        guess = request.form.get("guess")

        if guess and guess.isdigit():

            guess = int(guess)

            session["attempts"] += 1

            guesses = session["guesses"]
            guesses.append(guess)
            session["guesses"] = guesses

            if guess == session["secret"]:
                session["game_over"] = True
                message = "WIN"

            elif guess > session["secret"]:
                feedback = " ⌛️ Too High"

            else:
                feedback = " ⏳ Too Low"

            if (
                session["attempts"] >= MAX_ATTEMPTS
                and not session["game_over"]
            ):
                session["game_over"] = True
                message = "LOSE"

    return render_template(
        "index.html",
        lowest=LOWEST,
        highest=HIGHEST,
        attempts=session["attempts"],
        max_attempts=MAX_ATTEMPTS,
        game_over=session["game_over"],
        secret=session["secret"],
        message=message,
        feedback=feedback,
        guesses=session["guesses"]
    )


@app.route("/restart")
def restart():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)