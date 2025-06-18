var socket = io();
var miNombre = "";

function registrarse() {
    miNombre = document.getElementById("nombre").value;
    if (miNombre.trim() === "") {
        alert("Ingresa tu nombre.");
        return;
    }
    socket.emit("unirse", { nombre: miNombre });
    document.getElementById("registro").style.display = "none";
    document.getElementById("juego").style.display = "block";
}

function nuevaRonda() {
    socket.emit("nueva_ronda");
}

socket.on("letra", function(letra) {
    document.getElementById("letra").innerText = letra;
});

document.getElementById("formulario").addEventListener("submit", function(e) {
    e.preventDefault();

    var respuestas = {
        nombre: document.getElementById("nombre_categoria").value,
        apellido: document.getElementById("apellido").value,
        ciudad: document.getElementById("ciudad").value,
        color: document.getElementById("color").value,
        animal: document.getElementById("animal").value
    };

    socket.emit("enviar_respuestas", { nombre: miNombre, respuestas: respuestas });

    // Limpiar formulario
    document.getElementById("formulario").reset();
});

socket.on("jugadores_actualizados", function(jugadores) {
    var lista = document.getElementById("puntajes");
    lista.innerHTML = "";
    for (var jugador in jugadores) {
        lista.innerHTML += "<li>" + jugador + ": " + jugadores[jugador].puntos + " pts</li>";
    }
});
