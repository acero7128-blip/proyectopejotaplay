"""
Módulo Principal de Rutas y Servidor (app.py)
--------------------------------------------------------------------------
Gestiona la plataforma con 3 juegos gratuitos y 3 juegos premium,
incluyendo el acceso directo de administrador con el usuario 'admin'.
"""

from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
import database as db

app = Flask(__name__)
app.secret_key = "clave_secreta_evaluacion_profe_angel_2026"

db.init_db()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session and not session.get('is_admin'):
            flash("Debes iniciar sesión para continuar.", "warning")
            return redirect(url_for('auth'))
        return f(*args, **kwargs)
    return decorated_function

def subscription_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth'))
        
        user = db.get_user_by_id(session['user_id'])
        if not user or user['sub_status'] != 'active':
            flash("Acceso denegado: Esta zona es exclusiva para usuarios con suscripción Premium activa.", "danger")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    user = db.get_user_by_id(session['user_id']) if 'user_id' in session else None
    return render_template('index.html', user=user)

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    """Gestiona el registro y el inicio de sesión unificado (Estudiantes y Administrador 'admin')."""
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email').strip()
        password = request.form.get('password')

        if action == 'register':
            username = request.form.get('username').strip()
            if db.create_user(username, email, password):
                flash("Registro exitoso. ¡Ya puedes jugar los 3 juegos gratuitos!", "success")
            else:
                flash("El correo o nombre de usuario ya se encuentran registrados.", "danger")
                
        elif action == 'login':
            # --- ACCESO DIRECTO COMO ADMINISTRADOR ---
            if email == "admin" and password == "admin123":
                session['is_admin'] = True
                flash("Bienvenido al Panel de Administrador.", "success")
                return redirect(url_for('admin_dashboard'))
            
            # --- ACCESO NORMAL DE ESTUDIANTE ---
            user = db.verify_user(email, password)
            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                flash(f"Bienvenido de nuevo, {user['username']}.", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Credenciales incorrectas. Verifica tus datos.", "danger")
                
    return render_template('auth.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión finalizada correctamente.", "info")
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = db.get_user_by_id(session['user_id'])
    payments = db.get_user_payments(session['user_id'])
    return render_template('dashboard.html', user=user, payments=payments)

@app.route('/submit_payment', methods=['POST'])
@login_required
def submit_payment():
    ref = request.form.get('reference').strip()
    if ref:
        db.register_payment_support(session['user_id'], ref)
        flash("Soporte reportado con éxito. Su estado cambió a 'Pendiente' mientras se verifica el pago en Bolívares.", "success")
    else:
        flash("Debe ingresar el código o número de referencia del comprobante.", "danger")
    return redirect(url_for('dashboard'))

@app.route('/cancel_subscription', methods=['POST'])
@login_required
def cancel_subscription():
    db.update_subscription_status(session['user_id'], 'cancelled')
    flash("Has cancelado tu suscripción exitosamente. Los juegos premium han sido bloqueados.", "warning")
    return redirect(url_for('dashboard'))

@app.route('/admin/approve/<int:user_id>')
@login_required
def admin_approve(user_id):
    db.approve_payment(user_id)
    flash(f"Suscripción Premium activada con éxito por 30 días para el usuario ID {user_id}.", "success")
    return redirect(url_for('dashboard'))

# --- 3 JUEGOS GRATUITOS ---
@app.route('/games/free/math')
@login_required
def game_free_math():
    user = db.get_user_by_id(session['user_id']) if 'user_id' in session else None
    return render_template('games/free_math.html', user=user)

@app.route('/games/free/spelling')
@login_required
def game_free_spelling():
    user = db.get_user_by_id(session['user_id']) if 'user_id' in session else None
    return render_template('games/free_spelling.html', user=user)

@app.route('/games/free/geography')
@login_required
def game_free_geography():
    user = db.get_user_by_id(session['user_id']) if 'user_id' in session else None
    return render_template('games/free_geography.html', user=user)

# --- 3 JUEGOS PREMIUM ---
@app.route('/games/premium/algebra')
@subscription_required
def game_premium_algebra():
    user = db.get_user_by_id(session['user_id'])
    return render_template('games/prem_algebra.html', user=user)

@app.route('/games/premium/history')
@subscription_required
def game_premium_history():
    user = db.get_user_by_id(session['user_id'])
    return render_template('games/prem_history.html', user=user)

@app.route('/games/premium/science')
@subscription_required
def game_premium_science():
    user = db.get_user_by_id(session['user_id'])
    return render_template('games/prem_science.html', user=user)

# --- PANEL DE ADMINISTRADOR ---
@app.route('/admin/dashboard')
def admin_dashboard():
    """Panel donde el administrador visualiza a los clientes y cambia su estatus de pendiente a activo."""
    if not session.get('is_admin'):
        flash("Debes iniciar sesión como administrador.", "warning")
        return redirect(url_for('auth'))
    
    users = db.get_all_users()
    return render_template('admin/dashboard.html', users=users)

@app.route('/admin/set_active/<int:user_id>')
def admin_set_active(user_id):
    """Cambia directamente el estatus del usuario de pendiente a activo por 30 días."""
    if not session.get('is_admin'):
        return redirect(url_for('auth'))
    
    db.approve_payment(user_id)
    flash(f"¡Estatus actualizado con éxito! El usuario ID {user_id} ahora está ACTIVO.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash("Sesión de administrador cerrada.", "info")
    return redirect(url_for('auth'))

if __name__ == '__main__':
    app.run(debug=True)
