async function cargarParadas() {
    let res = await fetch("/paradas");
    let data = await res.json();
    let lista = document.getElementById("lista-paradas");
    lista.innerHTML = "";
    data.forEach(p => {
        let li = document.createElement("li");
        li.textContent = p;
        lista.appendChild(li);
    });
}

async function cargarConexiones() {
    let res = await fetch("/conexiones");
    let data = await res.json();
    let lista = document.getElementById("lista-conexiones");
    lista.innerHTML = "";
    data.forEach(c => {
        let li = document.createElement("li");
        li.textContent = `${c[0]} -> ${c[1]} : ${c[2]} min`;
        lista.appendChild(li);
    });
}

async function calcularRuta() {
    let ori = document.getElementById("ori").value;
    let des = document.getElementById("des").value;
    let res = await fetch(`/ruta?ori=${ori}&des=${des}`);
    let data = await res.json();
    if (data.tiempo === null) {
        document.getElementById("resultado-ruta").textContent = "No hay ruta disponible.";
    } else {
        document.getElementById("resultado-ruta").textContent = 
            `Tiempo: ${data.tiempo} min | Camino: ${data.camino.join(" -> ")}`;
    }
}
