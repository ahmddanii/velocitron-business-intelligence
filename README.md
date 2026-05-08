<div align="center">

# ⚡ Velocitron BI + DSS Platform

**Business Intelligence & Decision Support System**

Mengintegrasikan prediksi machine learning ke dalam alur kerja operasional bisnis secara nyata.

![Laravel](https://img.shields.io/badge/Laravel-13-FF2D20?style=flat-square&logo=laravel&logoColor=white)
![PHP](https://img.shields.io/badge/PHP-8.4-777BB4?style=flat-square&logo=php&logoColor=white)
![Python](https://img.shields.io/badge/Python-Flask-3776AB?style=flat-square&logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=flat-square&logo=mysql&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-Frontend-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)

</div>

---

## 📌 Overview

Velocitron adalah platform BI & DSS yang dirancang untuk mensimulasikan alur kerja operasional tingkat enterprise. Sistem ini mendemonstrasikan bagaimana prediksi machine learning dapat diintegrasikan ke dalam proses bisnis nyata.

**Sistem mengintegrasikan:**
- Role-based dashboards
- DSS prediction workflow
- Transaction approval lifecycle
- Business Intelligence analytics
- Executive insights & DSS monitoring
- Reporting & export features

---

## 🔄 Alur Utama Sistem

```
Create Request
      ↓
DSS Prediction
      ↓
Financial Review
      ↓
Approved / Rejected
      ↓
Stored in History
      ↓
Analytics Updated
```

---

## 🏗️ Arsitektur

```
Operational Requests
        ↓
DSS Prediction Engine
        ↓
Approval Workflow
        ↓
Historical Transactions
        ↓
Business Intelligence Analytics
        ↓
Executive Insights & Monitoring
```

---

## 👥 Roles & Tanggung Jawab

| Role | Tanggung Jawab |
|------|----------------|
| 💼 **Financial Controller** | Review DSS, approve/reject transaksi, ekspor laporan |
| 📦 **Procurement Director** | Analitik pengadaan, risiko supply, monitoring penolakan |
| 🚚 **Logistics Officer** | Risiko operasional pengiriman, monitoring ship mode |
| 🤝 **Key Account Manager** | Profitabilitas kontrak, insight segmen & regional |
| 📊 **Head Analytics** | DSS monitoring center, prediksi & confidence analytics |

---

## 🧠 DSS Prediction System

Model ML menganalisis input berikut:

| Input | |
|-------|-|
| Sales | Quantity |
| Discount | Shipping Days |
| Category | Segment |
| Region | Ship Mode |

**Output prediksi:**
- ✅ Profitable / ❌ Loss
- Confidence level
- Probability analysis

---

## 🛠️ Tech Stack

| Layer | Teknologi |
|-------|-----------|
| **Backend** | Laravel 13, PHP 8.4, MySQL |
| **Frontend** | Blade, TailwindCSS, Chart.js, Material Symbols |
| **DSS / ML** | Python Flask API, ML Prediction Model |

---

## 🚀 Instalasi

### Laravel

**1. Clone & masuk ke direktori**
```bash
git clone <repository-url>
cd velocitron
```

**2. Install dependensi**
```bash
composer install
npm install
```

**3. Konfigurasi environment**
```bash
cp .env.example .env
php artisan key:generate
```

**4. Konfigurasi database di `.env`**
```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=velocitron
DB_USERNAME=root
DB_PASSWORD=
```

**5. Migrate & seed database**
```bash
php artisan migrate
php artisan db:seed   # opsional
```

**6. Jalankan server**
```bash
php artisan serve
npm run dev
```

---

### Flask DSS API

**1. Masuk ke direktori Flask**
```bash
cd flask-api
```

**2. Install dependensi Python**
```bash
pip install -r requirements.txt
```

**3. Jalankan API**
```bash
python app.py
```

> Default: `http://127.0.0.1:5000`

---

## 📤 Export & Reporting

| Role | Dapat Mengekspor |
|------|-----------------|
| Financial Controller | Transaction history, DSS decisions, approval reports |
| Head Analytics | DSS monitoring report, confidence report, prediction metrics |

---

## ⚠️ Catatan Penting

> - **Flask API harus berjalan** sebelum menggunakan fitur DSS
> - **Vite harus aktif** untuk aset frontend
> - Chart.js analytics bergantung pada respons API
> - Fitur ekspor hanya tersedia untuk role tertentu

---

## 📄 Lisensi

**Educational Use Only** — Dikembangkan untuk simulasi Business Intelligence & DSS.
