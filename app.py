"""Hybrid: Network Security Auditor.
WARNING: Educational/authorized testing only. No offensive usage.
"""
from datetime import datetime
import json
import os
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length

from config import Config
from scanner.scanner import scan_target, discover_hosts, dns_lookup, reverse_dns, whois_lookup, uptime_check
from scanner.risk_analyzer import analyze_risk
from scanner.geoip import geo_lookup
from reports.pdf_generator import build_pdf_report
from telegram.telegram_bot import send_telegram_notification

app = Flask(__name__)
app.config.from_object(Config)
os.makedirs("instance", exist_ok=True)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(16), default="Analyst")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(120), nullable=False)
    open_ports = db.Column(db.Text, nullable=False)
    risk_level = db.Column(db.String(32), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey("scan.id"), nullable=False)
    report_path = db.Column(db.String(255), nullable=False)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255), nullable=False)
    user = db.Column(db.String(64), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField("Role", choices=[("Analyst", "Analyst"), ("Admin", "Admin")])
    submit = SubmitField("Register")

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def t(key):
    lang = session.get("lang", "ru")
    with open(f"translations/{lang}.json", encoding="utf-8") as f:
        return json.load(f).get(key, key)

@app.context_processor
def inject_globals():
    return {"tr": t, "lang": session.get("lang", "ru")}

def add_log(action):
    u = current_user.username if current_user.is_authenticated else "system"
    db.session.add(Log(action=action, user=u)); db.session.commit()

@app.route('/set-lang/<lang>')
def set_lang(lang):
    if lang in ["ru", "kz"]: session["lang"] = lang
    return redirect(request.referrer or url_for("login"))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("User exists", "danger")
        else:
            user = User(username=form.username.data, password_hash=generate_password_hash(form.password.data), role=form.role.data)
            db.session.add(user); db.session.commit(); add_log("Registered new user")
            flash("Registered", "success"); return redirect(url_for('login'))
    return render_template('login.html', form=form, register=True)

@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user); add_log("Login")
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "danger")
    return render_template('login.html', form=form, register=False)

@app.route('/logout')
@login_required
def logout():
    add_log("Logout"); logout_user(); return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    scans = Scan.query.order_by(Scan.created_at.desc()).limit(10).all()
    stats = {"scans": Scan.query.count(), "users": User.query.count()}
    return render_template('dashboard.html', scans=scans, stats=stats)

@app.route('/scan', methods=['GET','POST'])
@login_required
def scan():
    if request.method == 'POST':
        target = request.form.get('target','').strip()
        result = scan_target(target, app.config["SCAN_TIMEOUT"])
        risk = analyze_risk(result["open_ports"])
        rec = Scan(target=target, open_ports=json.dumps(result["open_ports"], ensure_ascii=False), risk_level=risk["level"])
        db.session.add(rec); db.session.commit()
        send_telegram_notification(app.config["TELEGRAM_BOT_TOKEN"], app.config["TELEGRAM_CHAT_ID"], target, len(result["open_ports"]), risk["level"], result["duration"])
        add_log(f"Scan {target}")
        return render_template('results.html', result=result, risk=risk, scan_id=rec.id)
    return render_template('scan.html')

@app.route('/history')
@login_required
def history():
    q = request.args.get('q','')
    query = Scan.query
    if q: query = query.filter(Scan.target.contains(q))
    return render_template('reports.html', scans=query.order_by(Scan.created_at.desc()).all())

@app.route('/report/<int:scan_id>')
@login_required
def report(scan_id):
    scan = db.session.get(Scan, scan_id)
    open_ports = json.loads(scan.open_ports)
    risk = analyze_risk(open_ports)
    path = build_pdf_report(scan, open_ports, risk)
    db.session.add(Report(scan_id=scan.id, report_path=path)); db.session.commit(); add_log(f"Report for {scan.target}")
    return send_file(path, as_attachment=True)

@app.route('/api/analytics')
@login_required
def analytics():
    scans = Scan.query.order_by(Scan.created_at.asc()).all()
    labels = [s.created_at.strftime('%d.%m') for s in scans]
    values = [len(json.loads(s.open_ports)) for s in scans]
    return jsonify({"labels": labels, "values": values})

@app.route('/tools')
@login_required
def tools():
    target = request.args.get("target", "8.8.8.8")
    return jsonify({"geo": geo_lookup(target), "dns": dns_lookup(target), "reverse": reverse_dns(target), "whois": whois_lookup(target), "uptime": uptime_check(target), "hosts": discover_hosts('192.168.1.0/30')})

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)
