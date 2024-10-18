from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import cv2
import numpy as np
import base64
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Pasta para armazenar as imagens dos usuários
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Dados fictícios para autenticação
user_data = {
    'user1': {
        'password': 'password123',
        'image_path': 'static/uploads/user1.jpg'
    },
    'user2': {
        'password': 'securepass',
        'image_path': 'static/uploads/user2.jpg'
    }
}


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verifica se o usuário está registrado e a senha está correta
        if username in user_data and user_data[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Credenciais inválidas.")
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        image_data = request.form['image'].split(',')[1]  # Remove o cabeçalho 'data:image/jpeg;base64,'

        # Salva a imagem do usuário
        image_path = os.path.join(UPLOAD_FOLDER, f'{username}.jpg')
        with open(image_path, 'wb') as fh:
            fh.write(base64.b64decode(image_data))

        # Armazena os dados do usuário
        user_data[username] = {'password': password, 'image_path': image_path}

        return redirect(url_for('login_page'))
    return render_template('register.html')


@app.route('/verify_face', methods=['POST'])
def verify_face():
    data = request.get_json()
    image_data = data['image'].split(',')[1]  # Remove o cabeçalho 'data:image/jpeg;base64,'

    # Decodifica a imagem base64
    image = np.frombuffer(base64.b64decode(image_data), np.uint8)
    img = cv2.imdecode(image, cv2.IMREAD_COLOR)

    # Converter para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Carrega o classificador Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detecta rostos na imagem
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        # Aqui você pode adicionar lógica para comparar a imagem com as imagens armazenadas para autenticação.
        # Esta lógica pode incluir o uso de algoritmos de reconhecimento facial.
        return jsonify({"success": "Rosto detectado!"})
    else:
        return jsonify({"error": "Nenhum rosto detectado."})


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login_page'))


if __name__ == '__main__':
    app.run(debug=True)
