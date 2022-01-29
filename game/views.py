from flask import render_template, request, flash, redirect, url_for, Blueprint
from game.model import Round, Scores
from game import db
from flask_login import login_required, current_user
from random import randint

views = Blueprint('views', __name__)

@views.route("/")
def home_page():
    return render_template('home_page.html')


@views.route("/game", methods=['GET', 'POST'])
@login_required
def game_page():

    if request.method == 'POST':
        pussy = request.form.get('guess')
        guess = pussy.lower()
        matty = ['rock', 'paper', 'scissors']
        matt = randint(0, 2)
        mikk = matty[matt]
        round = Round()
        if mikk == 'scissors' and guess == 'paper':
            round = Round(computer=1)
            flash(f'you lost this round!!!', category='danger')
        elif mikk == 'scissors' and guess == 'rock':
            round = Round(user=1)
            flash(f'You win this round!!!', category='success')
        elif mikk == guess:
            round = Round()
            flash(f'Draw this round!!!', category='warning')
        elif mikk == 'paper' and guess == 'rock':
            round = Round(computer=1)
            flash(f'you lost this round!!!', category='danger')
        elif mikk == 'paper' and guess == 'scissors':
            round = Round(user=1)
            flash(f'You wins this round!!!', category='success')
        elif mikk == 'rock' and guess == 'paper':
            round = Round(user=1)
            flash(f'You wins! this round!!', category='success')
        elif mikk == 'rock' and guess == 'scissors':
            round = Round(computer=1)
            flash(f'you lost this round!!!', category='danger')
        db.session.add(round)
        db.session.commit()
        if len(Round.query.all()) >= 10:
            mark = 0
            for i in Round.query.all():
                mark = mark + i.user
            scores = Scores(score=mark, user_id=current_user.id)
            db.session.add(scores)
            db.session.commit()
            if mark > current_user.highscore:
                current_user.highscore = mark
                db.session.commit()
            return redirect(url_for('views.result_page'))
    rounds = Round.query.all()
    return render_template('game.html', rounds=rounds)



@views.route("/result_page")
@login_required
def result_page():
    rounds = Round.query.all()
    mark = 0
    mint = 0
    for i in rounds:
        mark = mark + i.user
        mint = mint + i.computer
    if mark == mint:
        result = 'This match ended in a draw'
        color = 'yellow'
    elif mark > mint:
        result = f'{current_user.username} is the winner with {mark} points while Computer had {mint}'
        color = 'green'
    else:
        result = f'{current_user.username} is a loser Computer: {mint} while {current_user.username}: {mark}'
        color = 'red'

    return render_template('result.html', rounds=rounds, result=result, color=color)


@views.route("/delete_all")
@login_required
def delete_all():
    mad = Round.query.all()
    for i in mad:
        db.session.delete(i)
    db.session.commit()
    return redirect(url_for('views.game_page'))
