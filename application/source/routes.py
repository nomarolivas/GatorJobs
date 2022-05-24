from flask import request, render_template, make_response
from flask import current_app as app
from .models import db, User


@app.route('/', methods=['GET'])
def records():
    """Create a user via query string parameters."""
    username = request.args.get('user')
    email = request.args.get('email')
    if username and email:
        existing_user = User.query.filter(
            User.username == username or User.email == email
        ).first()
        if existing_user:
            return make_response(
                f'{username} ({email}) already created!'
            )
        new_user = User(
            username=username,
            email=email,
        )
       # Create an instance of the User class
        db.session.add(new_user)  # Adds new User record to database
        db.session.commit()  # Commits all changes
        redirect(url_for('user_records'))
    return render_template(
        'index.jinja2',
        users=User.query.all(),
        title="Show Users"
    )

@app.route('/', methods=['GET'])
def create_user():
    """Create a user."""

    return render_template(
        'users.jinja2',
        users=User.query.all(),
        title="Show Users"
    )
