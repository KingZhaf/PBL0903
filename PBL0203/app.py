from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)

def get_data():
    # Menggunakan path absolut agar tidak FileNotFoundError
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, 'Smartphone_Usage_And_Addiction_Analysis_7500_Rows.csv')
    
    if not os.path.exists(csv_path):
        return None
    
    df = pd.read_csv(csv_path)
    return df

@app.route('/')
def index():
    df = get_data()
    
    if df is None:
        return "File CSV tidak ditemukan! Pastikan file berada di folder yang sama dengan app.py"

    # Statistik untuk Dashboard
    stats = {
        'total_users': len(df),
        'avg_screen_time': round(df['daily_screen_time_hours'].mean(), 2),
        'high_stress_pct': round((df['stress_level'] == 'High').mean() * 100, 2),
        'addiction_rate': round((df['addicted_label'] == 1).mean() * 100, 2)
    }
    
    # Ambil 100 data untuk ditampilkan
    table_data = df.head(100).to_dict(orient='records')
    
    return render_template('index.html', stats=stats, data=table_data)

if __name__ == '__main__':
    app.run(debug=True)