async function api(path, opts={}) {
  const res = await fetch(path, { headers:{'Content-Type':'application/json'}, ...opts });
  let data;
  try { data = await res.json(); } catch { data = null; }
  if (!res.ok) throw new Error((data && data.error) || `HTTP ${res.status}`);
  return data;
}

async function refrescar() {
  const [ps, cs] = await Promise.all([api('/paradas'), api('/conexiones')]);
  // paradas
  const contP = document.getElementById('paradas');
  contP.innerHTML = '';
  ps.forEach(p => {
    const s = document.createElement('span');
    s.className = 'pill';
    s.textContent = p;
    const x = document.createElement('button');
    x.textContent = ' ×';
    x.style.marginLeft = '6px';
    x.onclick = async () => { await api('/eliminar_parada',{method:'POST',body:JSON.stringify({nombre:p})}); await refrescar(); }
    s.appendChild(x);
    contP.appendChild(s);
  });

  const ori = document.getElementById('ori'), des = document.getElementById('des');
  ori.innerHTML = ''; des.innerHTML = '';
  ps.forEach(p => {
    const o = document.createElement('option'); o.value = p; o.textContent = p; ori.appendChild(o);
    const d = document.createElement('option'); d.value = p; d.textContent = p; des.appendChild(d);
  });

  const contC = document.getElementById('conexiones');
  contC.innerHTML = '';
  const ul = document.createElement('ul');
  cs.forEach(([a,b,t]) => {
    const li = document.createElement('li');
    li.textContent = `${a} → ${b} (${t}m) `;
    const btn1 = document.createElement('button');
    btn1.textContent = 'Eliminar →';
    btn1.onclick = async () => { await api('/eliminar_conexion',{method:'POST',body:JSON.stringify({a,b,bidir:false})}); await refrescar(); };
    const btn2 = document.createElement('button');
    btn2.textContent = 'Eliminar ↔';
    btn2.style.marginLeft='6px';
    btn2.onclick = async () => { await api('/eliminar_conexion',{method:'POST',body:JSON.stringify({a,b,bidir:true})}); await refrescar(); };
    li.appendChild(btn1); li.appendChild(btn2); ul.appendChild(li);
  });
  contC.appendChild(ul);
}

async function agregarParada(){
  const nombre = document.getElementById('nueva-parada').value.trim();
  if (!nombre) return;
  await api('/agregar_parada',{method:'POST',body:JSON.stringify({nombre})});
  document.getElementById('nueva-parada').value='';
  await refrescar();
}

async function agregarConexion(){
  const a = document.getElementById('cx-a').value.trim();
  const b = document.getElementById('cx-b').value.trim();
  const t = Number(document.getElementById('cx-t').value.trim());
  const bidir = document.getElementById('cx-bidir').checked;
  if (!a || !b || Number.isNaN(t)) return;
  try {
    await api('/agregar_conexion',{method:'POST',body:JSON.stringify({a,b,t,bidir})});
  } catch(e){ alert(e.message); }
  ['cx-a','cx-b','cx-t'].forEach(id=>document.getElementById(id).value='');
  await refrescar();
}

async function calcularRuta(){
  const ori = document.getElementById('ori').value;
  const des = document.getElementById('des').value;
  const out = document.getElementById('resultado');
  out.textContent = 'Calculando...';
  try{
    const r = await api(`/ruta?ori=${encodeURIComponent(ori)}&des=${encodeURIComponent(des)}`);
    out.innerHTML = `<div class="ok">Tiempo: ${r.tiempo} min</div><div>Camino: ${r.camino.join(' → ')}</div>`;
  }catch(e){
    out.innerHTML = `<div class="err">${e.message}</div>`;
  }
}

async function guardar(){
  const msg = document.getElementById('persist-msg');
  try { await api('/guardar',{method:'POST',body:JSON.stringify({ruta:'grafo.json'})}); msg.textContent='Guardado en grafo.json'; }
  catch(e){ msg.textContent='Error al guardar: '+e.message; }
}

async function cargar(){
  const msg = document.getElementById('persist-msg');
  try { await api('/cargar',{method:'POST',body:JSON.stringify({ruta:'grafo.json'})}); msg.textContent='Cargado desde grafo.json'; await refrescar(); }
  catch(e){ msg.textContent='Error al cargar: '+e.message; }
}

window.addEventListener('DOMContentLoaded', refrescar);
