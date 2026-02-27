import speech_recognition as sr
from gtts import gTTS
import os
import hashlib
import datetime
import folium
import os
import joblib
from PIL import Image
import numpy as np
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

pest_model = joblib.load("models/pest_model.pkl")
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER,exist_ok=True)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '2109'
app.config['MYSQL_DB'] = 'agri_db'

mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM farmers")
    farmers = cursor.fetchall()
    return render_template('dashboard.html', farmers=farmers)

@app.route('/add_farmer', methods=['POST'])
def add_farmer():
    name = request.form['name']
    location = request.form['location']
    land_size = request.form['land_size']

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO farmers (name, location, land_size) VALUES (%s, %s, %s)",
        (name, location, land_size)
    )
    mysql.connection.commit()

    return jsonify({"message": "Farmer Added Successfully!"})

@app.route('/predict_yield', methods=['POST'])
def predict_yield():
    soil = float(request.json['soil'])
    rainfall = float(request.json['rainfall'])

    # Simple formula (Demo AI logic)
    prediction = (soil * 0.5) + (rainfall * 0.3)

    return jsonify({"yield_prediction": round(prediction, 2)})
    
@app.route('/recommend_crop', methods=['POST'])
def recommend_crop():
    soil = request.json['soil_type']
    rainfall = float(request.json['rainfall'])
    temperature = float(request.json['temperature'])

    # Simple Decision Logic (Demo AI)
    if soil == "Black" and rainfall > 100:
        crop = "Cotton"
    elif soil == "Loamy" and temperature > 25:
        crop = "Wheat"
    elif soil == "Sandy" and rainfall < 80:
        crop = "Millets"
    else:
        crop = "Rice"

    return jsonify({"recommended_crop": crop})
    
@app.route('/fertilizer_advice', methods=['POST'])
def fertilizer_advice():
    nitrogen = float(request.json['nitrogen'])

    if nitrogen < 40:
        advice = "Apply Urea (High Nitrogen Fertilizer)"
    else:
        advice = "Nitrogen level sufficient"

    return jsonify({"fertilizer_advice": advice})    
    
@app.route('/irrigation_advice', methods=['POST'])
def irrigation_advice():
    moisture = float(request.json['moisture'])

    if moisture < 30:
        msg = "Irrigation Needed Immediately"
    elif moisture < 60:
        msg = "Moderate Irrigation Suggested"
    else:
        msg = "Soil Moisture is Sufficient"

    return jsonify({"irrigation": msg})
@app.route('/pest_detection', methods=['GET', 'POST'])
def pest_detection():
    if request.method == 'POST':
        file = request.files['image']
        
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            img = Image.open(filepath)
            img = img.resize((50, 50))
            img_array = np.array(img)

            # Simulated feature extraction
            features = [
                img_array.mean(),
                img_array.std(),
                img_array.max()
            ]

            prediction = pest_model.predict([features])[0]

            pesticide_map = {
                "Aphids": "Use Neem Oil Spray",
                "Leaf Miner": "Use Spinosad",
                "Whitefly": "Use Imidacloprid"
            }

            pesticide = pesticide_map.get(prediction, "Consult Expert")

            return render_template(
                "pest.html",
                pest=prediction,
                pesticide=pesticide
            )

    return render_template("pest.html")
    
@app.route('/irrigation', methods=['GET', 'POST'])
def irrigation():
    if request.method == 'POST':
        soil_moisture = float(request.form['soil_moisture'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        crop_type = request.form['crop']
        soil_type = request.form['soil_type']

        # 🌱 Advanced Smart Logic
        if soil_type == "Sandy":
            threshold = 45
        elif soil_type == "Clay":
            threshold = 35
        else:
            threshold = 40

        if soil_moisture < threshold and temperature > 28:
            result = f"Irrigate Now for {crop_type} 🌱"
        elif soil_moisture < threshold:
            result = "Moderate Irrigation Required 💧"
        else:
            result = "No Irrigation Required ✅"

        return render_template('irrigation.html', result=result)

    return render_template('irrigation.html')
    
@app.route('/soil_health', methods=['GET', 'POST'])
def soil_health():
    if request.method == 'POST':
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        ph = float(request.form['ph'])
        soil_type = request.form['soil_type']

        # 🌱 Soil Health Logic
        score = 0

        # NPK Check
        if nitrogen >= 50:
            score += 1
        if phosphorus >= 40:
            score += 1
        if potassium >= 40:
            score += 1

        # pH Check
        if 6.0 <= ph <= 7.5:
            score += 1

        # Health Status
        if score == 4:
            health = "Soil is Healthy ✅"
            recommendation = "No major fertilizer needed."
        elif score >= 2:
            health = "Soil is Moderately Healthy ⚠️"
            recommendation = "Apply balanced NPK fertilizer."
        else:
            health = "Soil is Poor ❌"
            recommendation = "Apply organic compost + NPK fertilizer."

        return render_template('soil_health.html',
                               health=health,
                               recommendation=recommendation)

    return render_template('soil_health.html')
    
    
@app.route('/climate_score', methods=['GET', 'POST'])
def climate_score():
    if request.method == 'POST':
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        rainfall = float(request.form['rainfall'])
        wind_speed = float(request.form['wind_speed'])

        score = 0

        # 🌡 Temperature Ideal Range (20-35)
        if 20 <= temperature <= 35:
            score += 25

        # 💧 Humidity Ideal Range (40-80)
        if 40 <= humidity <= 80:
            score += 25

        # 🌧 Rainfall Ideal Range (50-200 mm)
        if 50 <= rainfall <= 200:
            score += 25

        # 🌬 Wind Speed Ideal (< 25 km/h)
        if wind_speed < 25:
            score += 25

        # 🌱 Climate Status
        if score >= 80:
            status = "Excellent Climate for Crops 🌿"
        elif score >= 50:
            status = "Moderate Climate Conditions 🌤"
        else:
            status = "Risky Climate Conditions ⚠️"

        return render_template('climate_score.html',
                               score=score,
                               status=status)

    return render_template('climate_score.html')
    
@app.route('/satellite_map', methods=['GET', 'POST'])
def satellite_map():
    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])
        ndvi = float(request.form['ndvi'])

        # 🌿 NDVI Health Logic
        if ndvi >= 0.7:
            health_status = "Healthy Crops 🌿"
            color = "green"
        elif ndvi >= 0.4:
            health_status = "Moderate Crop Health 🌾"
            color = "orange"
        else:
            health_status = "Poor Crop Health ⚠️"
            color = "red"

        # Create Map
        m = folium.Map(location=[latitude, longitude], zoom_start=12)

        folium.CircleMarker(
            location=[latitude, longitude],
            radius=15,
            popup=health_status,
            color=color,
            fill=True,
            fill_color=color
        ).add_to(m)

        map_path = "templates/satellite_output.html"
        map_path="static/satellite_output.html"
        m.save(map_path)

        return render_template('satellite_map.html',
                               health_status=health_status,
                               map_generated=True)

    return render_template('satellite_map.html', map_generated=False)
    
    
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, datetime.datetime.now(), "Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        previous_block = self.get_latest_block()
        new_block = Block(
            len(self.chain),
            datetime.datetime.now(),
            data,
            previous_block.hash
        )
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True
blockchain=Blockchain()
@app.route('/blockchain', methods=['GET', 'POST'])
def blockchain_status():
    if request.method == 'POST':
        farmer_data = request.form['data']
        blockchain.add_block(farmer_data)

    is_valid = blockchain.is_chain_valid()

    return render_template('blockchain.html',
                           chain=blockchain.chain,
                           is_valid=is_valid)
                           
@app.route('/financial', methods=['GET', 'POST'])
def financial_eligibility():
    if request.method == 'POST':
        income = float(request.form['income'])
        land = float(request.form['land'])
        credit_score = int(request.form['credit_score'])
        crop = request.form['crop']

        eligibility = ""
        loan_amount = 0
        subsidy = ""

        # 💰 Eligibility Logic
        if credit_score >= 700 and income <= 500000:
            eligibility = "Eligible for Agricultural Loan ✅"
            loan_amount = land * 50000
            subsidy = "Eligible for Government Subsidy 🌾"
        elif credit_score >= 600:
            eligibility = "Eligible for Small Loan ⚠️"
            loan_amount = land * 30000
            subsidy = "Limited Subsidy Available"
        else:
            eligibility = "Not Eligible ❌"
            loan_amount = 0
            subsidy = "Improve Credit Score"

        return render_template('financial.html',
                               eligibility=eligibility,
                               loan_amount=loan_amount,
                               subsidy=subsidy)

    return render_template('financial.html')
@app.route('/voice_assistant', methods=['GET', 'POST'])
def voice_assistant():
    response_text = ""

    if request.method == 'POST':
        command = request.form['command'].lower()

        # 🌾 Smart Krishi Voice Logic
        if "soil" in command:
            response_text = "Soil health is good and suitable for cultivation."
        elif "irrigation" in command:
            response_text = "Irrigation is recommended tomorrow morning."
        elif "loan" in command:
            response_text = "You are eligible for agricultural loan."
        else:
            response_text = "Sorry, I did not understand your request."

        # Convert to Telugu voice
        tts = gTTS(response_text, lang='te')
        audio_path = "static/voice_response.mp3"
        tts.save(audio_path)

        return render_template("voice.html",
                               response=response_text,
                               audio_file="voice_response.mp3")

    return render_template("voice.html")

if __name__ == "__main__":
    app.run(debug=True)



