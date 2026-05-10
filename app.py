from flask import Flask, request, render_template_string

app = Flask(__name__)

# -------------------- Unit Conversion Data --------------------
length_units = {
    "m": 1,
    "cm": 0.01,
    "mm": 0.001,
    "km": 1000,
    "inch": 0.0254,
    "ft": 0.3048
}

mass_units = {
    "kg": 1,
    "g": 0.001,
    "mg": 0.000001,
    "lb": 0.453592
}

# -------------------- HTML Template --------------------
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Mechanical Unit Converter & Density Checker</title>
    <style>
        body { font-family: Arial; background:#f4f4f4; padding:20px; }
        .container { background:white; padding:20px; border-radius:10px; max-width:800px; margin:auto; }
        h2 { color:#333; }
        .header { text-align:center; background:#222; color:white; padding:10px; border-radius:10px; }
        input, select { padding:8px; margin:5px; width:200px; }
        button { padding:10px 15px; background:#007bff; color:white; border:none; cursor:pointer; }
        .result { margin-top:10px; font-weight:bold; }
    </style>
</head>
<body>

<div class="container">

<div class="header">
    <h2>Imran Ali</h2>
    <p>Roll No: 25-ME-191</p>
</div>

<h2>🔧 Mechanical Unit Converter</h2>

<form method="POST">
    <input type="number" step="any" name="value" placeholder="Enter value" required>

    <select name="category">
        <option value="length">Length</option>
        <option value="mass">Mass</option>
    </select>

    <select name="from_unit">
        <option>m</option><option>cm</option><option>mm</option>
        <option>km</option><option>inch</option><option>ft</option>
        <option>kg</option><option>g</option><option>mg</option><option>lb</option>
    </select>

    <select name="to_unit">
        <option>m</option><option>cm</option><option>mm</option>
        <option>km</option><option>inch</option><option>ft</option>
        <option>kg</option><option>g</option><option>mg</option><option>lb</option>
    </select>

    <button type="submit" name="convert">Convert</button>
</form>

{% if conversion_result %}
<p class="result">Result: {{conversion_result}}</p>
{% endif %}

<hr>

<h2>📦 Material Density Checker</h2>

<form method="POST">
    <input type="number" step="any" name="mass" placeholder="Mass (kg)" required>
    <input type="number" step="any" name="volume" placeholder="Volume (m³)" required>
    <button type="submit" name="density">Calculate Density</button>
</form>

{% if density_result %}
<p class="result">Density: {{density_result}} kg/m³</p>
{% endif %}

</div>

</body>
</html>
"""

# -------------------- Routes --------------------
@app.route("/", methods=["GET", "POST"])
def index():
    conversion_result = None
    density_result = None

    if request.method == "POST":

        # ---------------- Unit Conversion ----------------
        if "convert" in request.form:
            value = float(request.form["value"])
            from_unit = request.form["from_unit"]
            to_unit = request.form["to_unit"]

            # convert length or mass
            if from_unit in length_units and to_unit in length_units:
                base = value * length_units[from_unit]
                result = base / length_units[to_unit]
                conversion_result = f"{result:.4f} {to_unit}"

            elif from_unit in mass_units and to_unit in mass_units:
                base = value * mass_units[from_unit]
                result = base / mass_units[to_unit]
                conversion_result = f"{result:.4f} {to_unit}"

            else:
                conversion_result = "Invalid conversion"

        # ---------------- Density Calculation ----------------
        if "density" in request.form:
            mass = float(request.form["mass"])
            volume = float(request.form["volume"])

            if volume != 0:
                density = mass / volume
                density_result = f"{density:.4f}"
            else:
                density_result = "Volume cannot be zero"

    return render_template_string(
        HTML,
        conversion_result=conversion_result,
        density_result=density_result
    )

if __name__ == "__main__":
    app.run(debug=True)
