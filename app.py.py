import os
import secrets
from functools import wraps
from flask import Flask, abort, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from db import execute, query

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("COOKIE_SECURE", "0") == "1"
FLAGS = {"wifi": "Wi-Fi", "outlets": "Outlets", "quiet": "Quiet", "groups": "Group-friendly", "food": "Food nearby", "reserve": "Reservable rooms", "offcampus": "Not owned by GSU"}


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    if query("SELECT user_id FROM suspended_users WHERE user_id = %s", (str(user_id),), one=True):
        session.clear()
        return None
    return {"id": str(user_id), "name": session.get("display_name", "Student"), "admin": session.get("role") == "admin"}


def login_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user():
            flash("Sign in to continue.")
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = current_user()
        if not user or not user["admin"]:
            abort(403)
        return fn(*args, **kwargs)
    return wrapper


def csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


@app.before_request
def verify_csrf():
    if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
        expected = session.get("csrf_token", "")
        provided = request.form.get("csrf_token", "")
        if not expected or not secrets.compare_digest(expected, provided):
            abort(400)


@app.context_processor
def context():
    return {"user": current_user(), "flags": FLAGS, "csrf_token": csrf_token}


@app.route("/")
def index():
    term = request.args.get("q", "").strip()
    filters = [key for key in FLAGS if request.args.get(key) == "1"]
    sort = request.args.get("sort", "name")
    sql = "SELECT s.*, COALESCE(AVG(r.rating), 0) AS average_rating, COUNT(r.id) AS review_count FROM study_spaces s LEFT JOIN reviews r ON r.space_id = s.id WHERE 1=1"
    params = []
    if term:
        sql += " AND (s.name LIKE %s OR s.location LIKE %s OR s.kind LIKE %s OR s.blurb LIKE %s OR s.noise LIKE %s)"
        params.extend(["%" + term + "%"] * 5)
    for key in filters:
        sql += " AND s.`" + key + "` = 1"
    sql += " GROUP BY s.id"
    sql += {"name": " ORDER BY s.name ASC", "rating": " ORDER BY average_rating DESC, s.name ASC", "reviews": " ORDER BY review_count DESC, s.name ASC"}.get(sort, " ORDER BY s.name ASC")
    spaces = query(sql, tuple(params))
    return render_template("index.html", spaces=spaces, term=term, selected=filters, sort=sort)


@app.route("/spaces/<int:space_id>")
def detail(space_id):
    space = query("SELECT * FROM study_spaces WHERE id = %s", (space_id,), one=True)
    if not space:
        abort(404)
    reviews = query("SELECT id, author, rating, text, created_at FROM reviews WHERE space_id = %s ORDER BY created_at DESC", (space_id,))
    return render_template("detail.html", space=space, reviews=reviews)


@app.route("/closing-times")
def closing_times():
    spaces = query("SELECT id, name, hours, eats, site, verified_at FROM study_spaces ORDER BY name")
    return render_template("hours.html", spaces=spaces)


@app.route("/reviews/<int:space_id>", methods=["POST"])
@login_required
def add_review(space_id):
    if not query("SELECT id FROM study_spaces WHERE id = %s", (space_id,), one=True):
        abort(404)
    user = current_user()
    rating = request.form.get("rating", "")
    message = request.form.get("text", "").strip()
    if rating not in {"1", "2", "3", "4", "5"} or not message or len(message) > 2000:
        flash("Enter a rating from 1 to 5 and a review under 2000 characters.")
    else:
        execute("INSERT INTO reviews (space_id, user_id, author, rating, text) VALUES (%s, %s, %s, %s, %s)", (space_id, user["id"], user["name"], int(rating), message))
        flash("Review saved.")
    return redirect(url_for("detail", space_id=space_id))


@app.route("/reports/<int:review_id>", methods=["POST"])
@login_required
def report_review(review_id):
    review = query("SELECT id, space_id FROM reviews WHERE id = %s", (review_id,), one=True)
    if not review:
        abort(404)
    reason = request.form.get("reason", "").strip()
    if not reason or len(reason) > 500:
        flash("Enter a reason under 500 characters.")
    else:
        execute("INSERT INTO reports (review_id, reporter_id, reason) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE reason = VALUES(reason), status = 'open'", (review_id, current_user()["id"], reason))
        flash("Report sent to an admin.")
    return redirect(url_for("detail", space_id=review["space_id"]))


@app.route("/admin")
@admin_required
def admin():
    reports = query("SELECT p.id, p.review_id, p.reason, p.reporter_id, r.author, r.user_id, r.text FROM reports p JOIN reviews r ON r.id = p.review_id WHERE p.status = 'open' ORDER BY p.created_at DESC")
    suspended = query("SELECT user_id, reason, suspended_at FROM suspended_users ORDER BY suspended_at DESC")
    return render_template("admin.html", reports=reports, suspended=suspended)


@app.route("/admin/reports/<int:report_id>/<action>", methods=["POST"])
@admin_required
def moderate(report_id, action):
    if action not in {"dismiss", "remove"}:
        abort(404)
    report = query("SELECT review_id FROM reports WHERE id = %s AND status = 'open'", (report_id,), one=True)
    if not report:
        abort(404)
    if action == "remove":
        execute("DELETE FROM reviews WHERE id = %s", (report["review_id"],))
    else:
        execute("UPDATE reports SET status = 'dismissed' WHERE id = %s", (report_id,))
    flash("Report handled.")
    return redirect(url_for("admin"))


@app.route("/admin/suspend", methods=["POST"])
@admin_required
def suspend():
    user_id = request.form.get("user_id", "").strip()
    reason = request.form.get("reason", "").strip()
    if not user_id or len(user_id) > 128 or not reason or len(reason) > 500 or user_id == current_user()["id"]:
        abort(400)
    execute("INSERT INTO suspended_users (user_id, reason) VALUES (%s, %s) ON DUPLICATE KEY UPDATE reason = VALUES(reason)", (user_id, reason))
    flash("User suspended.")
    return redirect(url_for("admin"))


@app.route("/admin/unsuspend", methods=["POST"])
@admin_required
def unsuspend():
    execute("DELETE FROM suspended_users WHERE user_id = %s", (request.form.get("user_id", ""),))
    flash("User restored.")
    return redirect(url_for("admin"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        admin_hash = os.getenv("ADMIN_PASSWORD_HASH", "")
        if os.getenv("ALLOW_DEMO_LOGIN", "0") == "1" and admin_hash and check_password_hash(admin_hash, request.form.get("password", "")):
            session.clear()
            session.update(user_id="demo-admin", display_name="Demo Admin", role="admin")
            return redirect(url_for("index"))
        flash("Sign in through the team login. Demo admin login must be enabled separately.")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    if not app.secret_key:
        raise RuntimeError("Set SECRET_KEY before running the app")
    app.run(debug=False)
