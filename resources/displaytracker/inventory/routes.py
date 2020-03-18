from flask import (
    render_template, url_for, flash,
    redirect, request, abort, Blueprint
)
from flask_login import (
    current_user, login_required
)
from displaytracker import db
from displaytracker.models import (
    User, Post, PostDemo
)
# from displaytracker.forms import ()

inventory = Blueprint('inventory', __name__)


@inventory.route("/inv/home", methods=['GET', 'POST'])
@login_required
def display_squares():
    pass
    
    return render_template(
            'display_squares.html',
            title='DisplaySquares'
            )

