# ============================================================
#  Superstore BI — Backend API + DSS
#  Cara menjalankan: python app.py
#  Endpoint tersedia di: http://localhost:5000
# ============================================================
 
from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import joblib
import numpy as np
import os
from config import Config
 
# Inisialisasi Flask
app = Flask(__name__)
CORS(app)  # Izinkan akses dari domain lain (Laravel, browser, dll)
 
# ── Load model DSS ──────────────────────────────────────────
# Model dimuat satu kali saat app.py dijalankan
# Tidak perlu load ulang setiap ada request
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
try:
    model    = joblib.load(os.path.join(BASE_DIR, 'model_profit.pkl'))
    encoders = joblib.load(os.path.join(BASE_DIR, 'encoders.pkl'))
    print('✅ Model DSS berhasil dimuat.')
except FileNotFoundError as e:
    model, encoders = None, None
    print(f'⚠️  Model tidak ditemukan: {e}')
    print('   Pastikan model_profit.pkl & encoders.pkl ada di folder backend/')
 
 
# ── Helper fungsi koneksi & query database ───────────────────
def get_conn():
    """Buat koneksi baru ke MySQL."""
    return pymysql.connect(
        host     = Config.DB_HOST,
        user     = Config.DB_USER,
        password = Config.DB_PASSWORD,
        database = Config.DB_NAME,
        port     = Config.DB_PORT,
        cursorclass = pymysql.cursors.DictCursor  # Hasil berupa dict
    )
 
def query_db(sql, params=None):
    """Jalankan query SELECT dan kembalikan list of dict."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            return cur.fetchall()
    finally:
        conn.close()  # Selalu tutup koneksi

# ENDPOINT 1
# GET /api/summary
# Mengembalikan angka-angka utama untuk kartu KPI di dashboard
@app.route('/api/summary', methods=['GET'])
def summary():
    sql = '''
        SELECT
            ROUND(SUM(sales), 2)               AS total_sales,
            ROUND(SUM(profit), 2)              AS total_profit,
            COUNT(DISTINCT order_id)           AS total_orders,
            ROUND(AVG(profit_ratio) * 100, 2)  AS avg_profit_pct,
            SUM(quantity)                      AS total_units
        FROM fact_orders
    '''
    return jsonify(query_db(sql)[0])

# ENDPOINT 2
# GET /api/monthly-trend
# Data tren sales & profit per bulan untuk line chart
@app.route('/api/monthly-trend', methods=['GET'])
def monthly_trend():
    sql = '''
        SELECT
            CONCAT(d.year, '-', LPAD(d.month, 2, '0')) AS period,
            d.year,
            d.month,
            d.month_name,
            ROUND(SUM(f.sales),  2)        AS total_sales,
            ROUND(SUM(f.profit), 2)        AS total_profit,
            COUNT(DISTINCT f.order_id)     AS total_orders
        FROM fact_orders f
        JOIN dim_date d ON f.date_pk = d.date_pk
        GROUP BY d.year, d.month, d.month_name
        ORDER BY d.year ASC, d.month ASC
    '''
    return jsonify(query_db(sql))

# ENDPOINT 3
# GET /api/profit-by-category
# Sales & profit per kategori produk untuk bar chart
@app.route('/api/profit-by-category', methods=['GET'])
def profit_by_category():
    sql = '''
        SELECT
            p.category,
            ROUND(SUM(f.sales),  2)              AS total_sales,
            ROUND(SUM(f.profit), 2)              AS total_profit,
            ROUND(AVG(f.profit_ratio) * 100, 2)  AS avg_margin
        FROM fact_orders f
        JOIN dim_products p ON f.product_pk = p.product_pk
        GROUP BY p.category
        ORDER BY total_sales DESC
    '''
    return jsonify(query_db(sql))

# ENDPOINT 4
# GET /api/sales-by-region
# Distribusi sales per region untuk doughnut chart
@app.route('/api/sales-by-region', methods=['GET'])
def sales_by_region():
    sql = '''
        SELECT
            l.region,
            ROUND(SUM(f.sales),  2)     AS total_sales,
            ROUND(SUM(f.profit), 2)     AS total_profit,
            COUNT(DISTINCT f.order_id)  AS total_orders
        FROM fact_orders f
        JOIN dim_location l ON f.location_pk = l.location_pk
        GROUP BY l.region
        ORDER BY total_sales DESC
    '''
    return jsonify(query_db(sql))

# ENDPOINT 5
# GET /api/sales-by-segment
# Perbandingan sales per segmen untuk bar chart
@app.route('/api/sales-by-segment', methods=['GET'])
def sales_by_segment():
    sql = '''
        SELECT
            c.segment,
            ROUND(SUM(f.sales),  2)         AS total_sales,
            ROUND(SUM(f.profit), 2)         AS total_profit,
            COUNT(DISTINCT f.order_id)      AS total_orders,
            COUNT(DISTINCT c.customer_pk)   AS total_customers
        FROM fact_orders f
        JOIN dim_customers c ON f.customer_pk = c.customer_pk
        GROUP BY c.segment
        ORDER BY total_sales DESC
    '''
    return jsonify(query_db(sql))

# ENDPOINT 6
# GET /api/top-products
# 10 produk terlaris untuk tabel ranking
@app.route('/api/top-products', methods=['GET'])
def top_products():
    sql = '''
        SELECT
            p.product_name,
            p.category,
            p.sub_category,
            ROUND(SUM(f.sales),  2)  AS total_sales,
            ROUND(SUM(f.profit), 2)  AS total_profit,
            SUM(f.quantity)          AS total_qty
        FROM fact_orders f
        JOIN dim_products p ON f.product_pk = p.product_pk
        GROUP BY p.product_name, p.category, p.sub_category
        ORDER BY total_sales DESC
        LIMIT 10
    '''
    return jsonify(query_db(sql))

# ENDPOINT 7
# GET /api/yearly-trend
# Perbandingan sales antar tahun untuk bar chart
@app.route('/api/yearly-trend', methods=['GET'])
def yearly_trend():
    sql = '''
        SELECT
            d.year,
            ROUND(SUM(f.sales),  2)     AS total_sales,
            ROUND(SUM(f.profit), 2)     AS total_profit,
            COUNT(DISTINCT f.order_id)  AS total_orders
        FROM fact_orders f
        JOIN dim_date d ON f.date_pk = d.date_pk
        GROUP BY d.year
        ORDER BY d.year ASC
    '''
    return jsonify(query_db(sql))

# ENDPOINT DSS
# POST /api/predict-profit
# Menerima data transaksi, mengembalikan prediksi profitabilitas
@app.route('/api/predict-profit', methods=['POST'])
def predict_profit():
 
    # Cek apakah model tersedia
    if model is None:
        return jsonify({
            'error': 'Model belum tersedia.',
            'solution': 'Pastikan model_profit.pkl ada di folder backend/'
        }), 503
 
    # Ambil data dari request
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body kosong atau bukan format JSON'}), 400
 
    # Validasi semua field wajib ada
    required = ['sales','quantity','discount','shipping_days',
                'category','segment','region','ship_mode']
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({
            'error': f'Field tidak lengkap',
            'missing_fields': missing
        }), 400
 
    try:
        # Encode nilai kategoris menggunakan encoder dari Colab
        cat_vals = {}
        for col in ['category','segment','region','ship_mode']:
            le  = encoders[col]
            val = str(data[col])
            if val not in le.classes_:
                return jsonify({
                    'error': f'Nilai tidak valid untuk field {col}: "{val}"',
                    'valid_values': list(le.classes_)
                }), 400
            cat_vals[col] = int(le.transform([val])[0])
 
        # Susun array input sesuai urutan fitur saat training
        X = np.array([[
            float(data['sales']),
            int(data['quantity']),
            float(data['discount']),
            int(data['shipping_days']),
            cat_vals['category'],
            cat_vals['segment'],
            cat_vals['region'],
            cat_vals['ship_mode'],
        ]])
 
        # Prediksi
        prediction  = int(model.predict(X)[0])
        proba       = model.predict_proba(X)[0]
        prob_profit = round(float(proba[1]) * 100, 2)
        prob_loss   = round(float(proba[0]) * 100, 2)
 
        # Tentukan level keyakinan
        if prob_profit >= 80:   confidence = 'Sangat Tinggi'
        elif prob_profit >= 60: confidence = 'Tinggi'
        elif prob_profit >= 40: confidence = 'Sedang'
        else:                   confidence = 'Rendah'
 
        return jsonify({
            'prediction':       prediction,
            'label':            'Profitable' if prediction == 1 else 'Not Profitable',
            'label_id':         'Menguntungkan' if prediction == 1 else 'Tidak Menguntungkan',
            'prob_profitable':  prob_profit,
            'prob_loss':        prob_loss,
            'confidence':       confidence,
        })
 
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error Handler & Entry Point
# ── Error handler ───────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint tidak ditemukan',
                    'available': ['/api/summary','/api/monthly-trend',
                                  '/api/profit-by-category','/api/sales-by-region',
                                  '/api/sales-by-segment','/api/top-products',
                                  '/api/yearly-trend','/api/predict-profit']}), 404
 
@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
 
 
# ── Jalankan Flask ───────────────────────────────────────────
if __name__ == '__main__':
    print('\n' + '='*55)
    print('  Superstore BI — Backend API + DSS')
    print('  URL : http://localhost:5000')
    print('  Mode: Development (debug=True)')
    print('='*55 + '\n')
    app.run(debug=True, host='0.0.0.0', port=5000)
