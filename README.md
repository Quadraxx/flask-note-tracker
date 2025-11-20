# 📝 Flask Not ve Fatura Takip Uygulaması (Full-Stack CRUD)

## Proje Sahibi: Hüseyin Akın

Bu proje, Python **Flask** web çatısı ve **SQLAlchemy** (SQLite) kullanılarak geliştirilmiş, **tam teşekküllü (Full-Stack)** bir uygulamadır. Amacı, kullanıcıların güvenli bir şekilde hesap oluşturup, kendi özel notlarını ve fatura kayıtlarını takip etmelerini sağlamaktır.

Bu proje, bir geliştiricinin temel **güvenlik, veritabanı ilişkileri ve web uygulama mimarisi** becerilerini gösterir.

---

## ✨ Temel Özellikler

* **Güvenli Kimlik Doğrulama (Authentication):** Kullanıcıların kayıt (Register) ve giriş (Login) işlemlerini güvenle yönetir. Şifreler `Werkzeug` ile hashlenir.
* **Yetkilendirme ve İzolasyon:** Her kullanıcı sadece **kendi oluşturduğu** notları görür. (Veritabanı ilişkileri ile sağlanır.)
* **CRUD Fonksiyonları:**
    * **C**reate: Yeni not ekleme.
    * **R**ead: Notları listeleme.
    * **D**elete: Notları silme.
    * (Güncelleme, ileride eklenebilecek bir özelliktir.)
* **Teknoloji Yığını (Stack):** Python, Flask, Flask-SQLAlchemy, SQLite (Yerel veritabanı).

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Gereksinimler ve Sanal Ortam

Projeyi indirdikten sonra, sanal ortamınızı oluşturup kütüphaneleri yükleyin.

```bash
# 1. Sanal ortamı oluşturun
python -m venv venv

# 2. Sanal ortamı aktifleştirin (Windows)
.\venv\Scripts\activate

# 3. Gerekli kütüphaneleri kurun
pip install -r requirements.txt
