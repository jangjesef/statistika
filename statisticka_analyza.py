import numpy as np
import matplotlib.pyplot as plt
from weasyprint import HTML
import tempfile

# Data
velikosti = [35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
cetnosti = [5, 3, 5, 8, 12, 10, 9, 7, 3, 2]

# Základní výpočty
prumer = np.average(velikosti, weights=cetnosti)
modus = velikosti[cetnosti.index(max(cetnosti))]
median = 39

# Rozšířená data pro výpočty
rozsirena_data = []
for vel, cet in zip(velikosti, cetnosti):
    rozsirena_data.extend([vel] * cet)
rozsirena_data = np.array(rozsirena_data)

rozptyl = np.var(rozsirena_data)
smerodatna_odchylka = np.std(rozsirena_data)
variacni_koeficient = (smerodatna_odchylka / prumer) * 100

# Vytvoření grafů
plt.figure(figsize=(15, 10))

# 1. Sloupcový diagram
plt.subplot(221)
plt.bar(velikosti, cetnosti, color='skyblue')
plt.title('Četnosti velikostí bot')
plt.xlabel('Velikost boty')
plt.ylabel('Četnost')
plt.grid(True, alpha=0.3)

# 2. Koláčový diagram
plt.subplot(222)
plt.pie(cetnosti, labels=velikosti, autopct='%1.1f%%')
plt.title('Rozložení velikostí bot')

# 3. Krabicový diagram
plt.subplot(223)
plt.boxplot(rozsirena_data)
plt.title('Krabicový diagram velikostí')
plt.grid(True, alpha=0.3)

# 4. Histogram
plt.subplot(224)
plt.hist(rozsirena_data, bins=10, color='skyblue', density=True)
plt.title('Histogram velikostí')
plt.xlabel('Velikost boty')
plt.ylabel('Četnost')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('statisticke_grafy.png', dpi=300, bbox_inches='tight')

# Vytvoření HTML reportu
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Statistická analýza velikostí bot</title>
    <meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{ 
            font-family: Arial, sans-serif;
            margin: 0;
            background-color: white;
        }}
        .container {{
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            page-break-inside: avoid;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border: 1px solid #ddd;
        }}
        th {{
            background-color: #f8f9fa;
        }}
        img {{
            max-width: 100%;
            height: auto;
            margin: 20px 0;
            page-break-inside: avoid;
        }}
        .section {{
            margin: 30px 0;
            page-break-inside: avoid;
        }}
        h1, h2 {{
            color: #2c3e50;
            page-break-after: avoid;
        }}
        ul {{
            page-break-inside: avoid;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Statistická analýza velikostí bot</h1>

        <div class="section">
            <h2>1. Základní charakteristiky</h2>
            <table>
                <tr><th>Charakteristika</th><th>Hodnota</th></tr>
                <tr><td>Aritmetický průměr</td><td>{prumer:.3f}</td></tr>
                <tr><td>Modus</td><td>{modus}</td></tr>
                <tr><td>Medián</td><td>{median}</td></tr>
                <tr><td>Rozptyl</td><td>{rozptyl:.3f}</td></tr>
                <tr><td>Směrodatná odchylka</td><td>{smerodatna_odchylka:.3f}</td></tr>
                <tr><td>Variační koeficient</td><td>{variacni_koeficient:.2f}%</td></tr>
            </table>
        </div>

        <div class="section">
            <h2>2. Grafy</h2>
            <img src="statisticke_grafy.png" alt="Statistické grafy">
        </div>

        <div class="section">
            <h2>3. Tabulka četností</h2>
            <table>
                <tr>
                    <th>Velikost boty</th>
                    <th>Absolutní četnost</th>
                    <th>Relativní četnost</th>
                    <th>Relativní četnost (%)</th>
                </tr>
"""

# Přidání řádků tabulky
for vel, cet in zip(velikosti, cetnosti):
    rel_cet = cet / sum(cetnosti)
    html_content += f"""
                <tr>
                    <td>{vel}</td>
                    <td>{cet}</td>
                    <td>{rel_cet:.3f}</td>
                    <td>{rel_cet * 100:.1f}%</td>
                </tr>"""

html_content += """
            </table>
        </div>

        <div class="section">
            <h2>4. Závěry</h2>
            <ul>
                <li>Nejčastější velikost bot je {modus}</li>
                <li>Průměrná velikost bot je {prumer:.3f}</li>
                <li>50% hodnot leží pod velikostí {median}</li>
                <li>Rozptyl velikostí je {rozptyl:.3f}, což indikuje variabilitu dat</li>
                <li>Směrodatná odchylka {smerodatna_odchylka:.3f} ukazuje průměrnou odchylku od průměru</li>
                <li>Variační koeficient {variacni_koeficient:.2f}% značí relativní variabilitu souboru</li>
            </ul>
        </div>
    </div>
</body>
</html>
""".format(
    modus=modus,
    prumer=prumer,
    median=median,
    rozptyl=rozptyl,
    smerodatna_odchylka=smerodatna_odchylka,
    variacni_koeficient=variacni_koeficient
)

# Uložení HTML reportu
with open('statisticka_analyza.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# Konverze HTML do PDF
HTML(string=html_content).write_pdf('statisticka_analyza.pdf') 