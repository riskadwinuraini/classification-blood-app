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

        dic = {0: 'Ellyptocytes', 1: 'Normal', 2: 'Ovalocytes', 3: 'Random',4: 'Stomatocytes', 5: 'Teardop'}
        descriptions = {
            'Ellyptocytes': 'The system recognizes that the chosen item is categorized as ELLYPTOCYTES. To get a detailed explanation, you can click on the button provided below.',
            'Normal': 'The system recognizes that the chosen item is categorized as NORMAL. To get a detailed explanation, you can click on the button provided below.',
            'Ovalocytes': 'The system recognizes that the chosen item is categorized as OVALOCYTES. To get a detailed explanation, you can click on the button provided below.',
            'Stomatocytes': 'The system recognizes that the chosen item is categorized as STOMATOCYTES. To get a detailed explanation, you can click on the button provided below.',
            'Teardop': 'The system recognizes that the chosen item is categorized as TEARDOP. To get a detailed explanation, you can click on the button provided below.'
        }


        model = load_model('./app/models/ResNet50V4.h5')

        # Membuka gambar dari path yang diberikan dan mengubah ukurannya menjadi 220x220 piksel
        image_array = image.load_img(image_path, target_size=(256, 256))
        # Mengubah gambar menjadi array numpy dan menormalisasi nilai pikselnya menjadi rentang 0-1
        image_array = image.img_to_array(image_array) / 255.0
        # Mengubah bentuk array gambar agar sesuai dengan input model (jumlah gambar, tinggi, lebar, saluran warna)
        image_array = image_array.reshape((1, 256, 256, 3))

        # Melakukan prediksi label gambar menggunakan model
        predictions = model.predict(image_array)


        # Jika model tidak menghasilkan probabilitas
        if not np.any(predictions):
            
            return {
                'error': 'Model tidak menghasilkan probabilitas. Silakan cek input gambar.'
            }

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
            'label': dic[predicted_class].encode('utf-8').decode(), # Label kelas dengan probabilitas tertinggi
            'highest_probability': round(highest_probability, 2),  # Probabilitas tertinggi
            'other_probabilities': {k.encode('utf-8').decode(): v for k, v in other_probabilities.items()}, # Probabilitas kelas lainnya
            'description': descriptions[dic[predicted_class]].encode('utf-8').decode()
        }
    def get_result(self):
        if request.method != 'POST':
            print('error')
            return jsonify({"error": "Bad request"}), 400

        try:
            # Mendapatkan base64 data dari form request
            base64data = request.form['image']

            # Mengubah base64 data menjadi byte dan menyimpannya ke file temp
            filepath = base64.b64decode(base64data.encode('ascii'))
            img_filename = str(uuid.uuid4()) + ".jpg"
            img_path = "./app/static/temp/" + img_filename

            with open(img_path, "wb") as f:
                f.write(filepath) # Menyimpan file image base64 ke folder temp

            result = self.predict_label(img_path)

        except KeyError:
             return jsonify({"error": "Image data not found in the form"}), 400

        return jsonify({
            'label': result['label'],
            'probabilities': {
                'main': result['highest_probability'],
                'others': result['other_probabilities']
            },
            'image_path': img_path,
            'description': result['description']
        })
    
    def clearImage(self):

        temp_dir = os.path.join(os.getcwd(), 'app', 'static', 'temp')

        try:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            return jsonify(success=True, message='Semua gambar di temp berhasil dihapus.')

        except Exception as e:
            return jsonify(success=False, message=f'Terjadi kesalahan: {str(e)}')


