// login.js

document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById("video");
  const canvas = document.getElementById("canvas");
  const faceLoginButton = document.getElementById("faceLoginButton");

  // Configura a câmera
  function startFaceRecognition() {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then((stream) => {
        video.srcObject = stream;
        video.play();
        faceLoginButton.disabled = true; // Desativa o botão após iniciar o reconhecimento
      })
      .catch((error) => {
        console.error("Erro ao acessar a câmera:", error);
      });
  }

  // Função adicional para capturar a imagem do vídeo e enviar para o servidor pode ser adicionada aqui

  // Define o botão de iniciar reconhecimento facial
  faceLoginButton.addEventListener("click", startFaceRecognition);
});
