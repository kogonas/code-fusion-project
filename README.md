# Member 1 — Sprint 1 Starter

This is a **prepared starter implementation**, not evidence that it has been run, tested against MySQL, or committed to GitHub.

## Setup
1. Create a Python virtual environment and activate it.
2. Run `pip install -r requirements.txt`.
3. Run `schema.sql` in your local MySQL instance.
4. Copy `.env.example` to `.env` and set your actual credentials and a strong random `SECRET_KEY`.
5. Run `python app.py` and visit http://127.0.0.1:5000/register.

## Sprint 1 features
- Register a user with a hashed password.
- Log in with a password check and Flask session.
- View a protected dashboard.
- Log out.

## Manual verification checklist
- [ ] Register a new account.
- [ ] Confirm the password stored in MySQL is hashed.
- [ ] Confirm duplicate emails are rejected.
- [ ] Confirm incorrect login credentials are rejected.
- [ ] Confirm `/dashboard` redirects when logged out.
- [ ] Confirm logout clears the session.

## Before production or deployment
Add CSRF protection, stronger validation, rate limiting, secure cookie settings over HTTPS, and automated tests. Do not use the development fallback secret key in a deployed app.

## Git workflow
Create a branch such as `feature/member1-auth`, commit the starter files, push, and open a pull request. Follow the instructor's protected-main-branch and approval requirements. Use the **real** commit URL in your sprint report.
