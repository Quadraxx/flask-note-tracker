from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash # Şifre güvenliği için
from datetime import datetime

# --- UYGULAMA VE VERİTABANI KONFİGÜRASYONU ---
app = Flask(__name__)

# KRİTİK DÜZELTME: SECRET_KEY'i byte (b') olarak tanımlayarak
# dosya yollarındaki Türkçe karakterlerden kaynaklanan UnicodeEncodeError hatasını çözdük.
# Lütfen 'sizin_guvenli_gizli_anahtarınız' kısmını daha karmaşık bir şeyle değiştirin.
app.config['SECRET_KEY'] = b'sizin_guvenli_gizli_anahtariniz'

# SQLite veritabanı dosyasının yolu
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tracker.db'
# Değişiklikler için uyarı vermeyi kapatır
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Giriş yapılmamışsa buraya yönlendir

# --- VERİTABANI MODELLERİ (TABLOLAR) ---

@login_manager.user_loader
def load_user(user_id):
    # Flask-Login'in oturum sırasında kullanıcı nesnesini yüklemesini sağlar
    return User.query.get(int(user_id))

# Kullanıcı tablosu (Authentication için gerekli)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Notlarla ilişki: Bir kullanıcı birden çok nota sahip olabilir
    notes = db.relationship('Note', backref='author', lazy=True)

    def set_password(self, password):
        # Şifreyi güvenli bir şekilde hashler
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        # Girilen şifrenin hashlenmiş şifreyle eşleşip eşleşmediğini kontrol eder
        return check_password_hash(self.password_hash, password)

# Not/Fatura tablosu (Kullanıcıya bağlı)
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Foreign Key: Bu notun hangi kullanıcıya ait olduğunu gösterir
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# --- ROTALAR (ROUTING) BAŞLANGIÇ ---

# --- KULLANICI YÖNETİMİ (AUTH) ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            flash('Bu kullanıcı adı zaten kullanılıyor.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()
        
        flash('Kaydınız başarılı! Lütfen giriş yapın.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- NOT YÖNETİMİ (CRUD) ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        # Sadece giriş yapmış kullanıcının notlarını çekiyoruz
        user_notes = Note.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', notes=user_notes)
    
    # Giriş yapılmamışsa, hoş geldin ekranını göster
    return render_template('index.html', notes=None)

@app.route('/add_note', methods=['POST'])
@login_required 
def add_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        if title and content:
            new_note = Note(
                title=title, 
                content=content, 
                user_id=current_user.id 
            )
            db.session.add(new_note)
            db.session.commit()
            flash('Yeni not başarıyla eklendi!', 'success')
        else:
            flash('Başlık ve içerik alanları boş bırakılamaz.', 'danger')
            
    return redirect(url_for('index'))

@app.route('/delete_note/<int:note_id>')
@login_required 
def delete_note(note_id):
    # Notu ID'sine göre bul ve kullanıcının yetkisi var mı kontrol et
    note_to_delete = Note.query.filter_by(id=note_id, user_id=current_user.id).first_or_404()
    
    db.session.delete(note_to_delete)
    db.session.commit()
    flash('Not başarıyla silindi.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    # Uygulama başladığında veritabanı tablolarını oluştur (Yoksa)
    with app.app_context():
        db.create_all()
    app.run(debug=True)