let video = document.getElementById("video");
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let streaming = false;

function startFaceRegistration() {
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
      .getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
        video.play();
        streaming = true;
        document.getElementById("camera").style.display = "block";
      })
      .catch(function (err) {
        console.error("Erro ao acessar a câmera: ", err);
      });
  }
}

function captureImage() {
  if (streaming) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    let dataURL = canvas.toDataURL("image/jpeg");
    document.getElementById("image").value = dataURL; // Adiciona a imagem ao campo oculto
    video.srcObject.getTracks().forEach((track) => track.stop()); // Para o vídeo
    document.getElementById("camera").style.display = "none";
    streaming = false;
  }
}

document
  .getElementById("registerForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    captureImage(); // Captura a imagem antes de enviar o formulário

    // Cria um FormData para enviar o formulário
    let formData = new FormData(this);

    fetch("/register", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.text())
      .then((text) => {
        if (text.includes("Registrar")) {
          window.location.href = "/login";
        } else {
          alert("Erro ao registrar: " + text);
        }
      })
      .catch((error) => console.error("Erro ao registrar:", error));
  });
