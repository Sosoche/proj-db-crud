from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app

from app.services import UserService
from app.forms import UserForm

user_bp = Blueprint("user", __name__)
service = UserService()


@user_bp.route("/")
def index():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "").strip()
    pagination = service.get_users_list(
        page, current_app.config["USERS_PER_PAGE"], search
    )
    return render_template(
        "index.html", pagination=pagination, search=search
    )


@user_bp.route("/user/add", methods=["GET", "POST"])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        success, message = service.create_user(
            form.username.data, form.email.data
        )
        if success:
            flash(message, "success")
            return redirect(url_for("user.index"))
        flash(message, "danger")
    return render_template("add_user.html", form=form)


@user_bp.route("/user/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        return render_template("errors/404.html"), 404

    form = UserForm(obj=user)
    if form.validate_on_submit():
        success, message = service.update_user(
            user_id, form.username.data, form.email.data
        )
        if success:
            flash(message, "success")
            return redirect(url_for("user.index"))
        flash(message, "danger")
    return render_template("edit_user.html", form=form, user=user)


@user_bp.route("/user/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id: int):
    success, message = service.delete_user(user_id)
    flash(message, "success" if success else "danger")
    return redirect(url_for("user.index"))
