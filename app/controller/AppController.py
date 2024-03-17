from flask import request, jsonify
import os
import io
import uuid
import base64
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class AppController:

    def __init__(self):
        pass

    @staticmethod
    def predict_label(image_path):

        dic = {0: 'Cerscospora', 1: 'Healthy', 2: 'Rust'}

        model = load_model('app/models/ResNet50V4.h5')

        # Membuka gambar dari path yang diberikan dan mengubah ukurannya menjadi 220x220 piksel
        image_array = image.load_img(image_path, target_size=(220, 220))
        # Mengubah gambar menjadi array numpy dan menormalisasi nilai pikselnya menjadi rentang 0-1
        image_array = image.img_to_array(image_array) / 255.0
        # Mengubah bentuk array gambar agar sesuai dengan input model (jumlah gambar, tinggi, lebar, saluran warna)
        image_array = image_array.reshape((1, 220, 220, 3))

        # Melakukan prediksi label gambar menggunakan model
        predictions = model.predict(image_array)

        # Mendapatkan indeks kelas dengan probabilitas tertinggi dari prediksi
        predicted_class = np.argmax(predictions[0])

        # Mendapatkan probabilitas tertinggi
        highest_probability = np.max(predictions[0]) * 100

        # Mendapatkan probabilitas untuk kelas lainnya
        other_probabilities = {label: round(probability * 100, 2)
                            for label, probability in zip(dic.values(), predictions[0])
                            if label != dic[predicted_class]}

        # Mengembalikan hasil prediksi dalam bentuk dictionary
        return {
            'label': dic[predicted_class], # Label kelas dengan probabilitas tertinggi
            'highest_probability': round(highest_probability, 2),  # Probabilitas tertinggi
            'other_probabilities': other_probabilities # Probabilitas kelas lainnya
        }
    def get_output(self):
        if request.method != 'POST':
            print('error')
            return jsonify({"error": "Bad request"}), 400

        try:
            image_data = request.form['image']
            image_data = image_data.split(",")[1]  # remove the "data:image/jpeg;base64," part
            image_file = io.BytesIO(base64.b64decode(image_data))
            filename = f"{uuid.uuid4()}.jpg"
            filepath = os.path.join("static/temp", filename)
            with open(filepath, "wb") as f:
                image_file.seek(0)
                f.write(image_file.read())

            result = AppController.predict_label(filepath)
        except Exception as e:
            return jsonify({"error": "Bad request", "message": str(e)}), 400

        return jsonify({
            'label': result['label'],
            'probabilities': {
                'main': result['highest_probability'],
                'others': result['other_probabilities']
            },
            'image_path': filepath
        })


