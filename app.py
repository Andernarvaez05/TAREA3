from flask import Flask, render_template_string, request, jsonify
import json

app = Flask(__name__)

STUDENTS = [
    {"id": 1, "name": "Ana García",   "grade": 9.5, "career": "Ingeniería de Software"},
    {"id": 2, "name": "Luis Pérez",   "grade": 7.8, "career": "Medicina"},
    {"id": 3, "name": "Sofía Torres", "grade": 8.3, "career": "Arquitectura"},
    {"id": 4, "name": "Carlos Mora",  "grade": 6.5, "career": "Derecho"},
    {"id": 5, "name": "Valeria Ruiz", "grade": 9.1, "career": "Ingeniería de Software"},
]
_next_id = 6

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>EduTrack</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --primary: #4f46e5;
      --bg:      #f0f4ff;
      --white:   #ffffff;
      --text:    #1e1b4b;
      --muted:   #6b7280;
      --border:  #e5e7eb;
      --green:   #059669;
      --blue:    #2563eb;
      --red:     #dc2626;
      --shadow:  0 2px 8px rgba(79,70,229,.10);
      --shadow-lg: 0 10px 30px rgba(79,70,229,.18);
      --ff: 'Inter', sans-serif;
    }

    body { font-family: var(--ff); background: var(--bg); color: var(--text); min-height: 100vh; }

    /* ── Header ── */
    header {
      background: linear-gradient(135deg, #1e1b4b 0%, #4f46e5 100%);
      padding: 1.2rem 2rem;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: 0 4px 20px rgba(79,70,229,.35);
    }
    .logo { color: #fff; font-size: 1.45rem; font-weight: 700; letter-spacing: -.02em; }
    .logo span { color: #a5b4fc; }
    .badge {
      background: rgba(255,255,255,.15); color: #fff;
      padding: .3rem .85rem; border-radius: 9999px;
      font-size: .78rem; font-weight: 500;
    }

    /* ── Main ── */
    main { max-width: 1080px; margin: 0 auto; padding: 2rem 1.5rem; }

    /* ── Stats ── */
    .stats { display: grid; grid-template-columns: repeat(3,1fr); gap: 1rem; margin-bottom: 2rem; }
    .stat {
      background: var(--white); border-radius: 16px;
      padding: 1.4rem 1.5rem; box-shadow: var(--shadow);
      display: flex; align-items: center; gap: 1rem;
    }
    .stat-icon {
      font-size: 1.7rem; width: 50px; height: 50px;
      border-radius: 13px; display: flex; align-items: center; justify-content: center;
    }
    .si-total { background: #eef2ff; }
    .si-avg   { background: #fef3c7; }
    .si-top   { background: #ecfdf5; }
    .stat-info p  { font-size: .75rem; color: var(--muted); margin-bottom: .2rem; }
    .stat-info strong { font-size: 1.7rem; font-weight: 700; line-height: 1; }

    /* ── Form ── */
    .form-card {
      background: var(--white); border-radius: 16px;
      padding: 1.4rem 1.5rem; box-shadow: var(--shadow); margin-bottom: 2rem;
    }
    .form-card h2 {
      font-size: .72rem; font-weight: 600; text-transform: uppercase;
      letter-spacing: .1em; color: var(--muted); margin-bottom: 1rem;
    }
    .form-row {
      display: grid; grid-template-columns: 1fr 1fr 110px auto;
      gap: .75rem; align-items: end;
    }
    .fg label { display: block; font-size: .72rem; font-weight: 500; color: var(--muted); margin-bottom: .3rem; }
    .fg input {
      width: 100%; border: 1.5px solid var(--border); border-radius: 10px;
      padding: .6rem .85rem; font-family: var(--ff); font-size: .88rem;
      color: var(--text); outline: none; transition: border-color .2s, box-shadow .2s;
    }
    .fg input:focus { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(79,70,229,.12); }
    .btn-add {
      background: linear-gradient(135deg,#4f46e5,#7c3aed);
      color: #fff; border: none; border-radius: 10px;
      padding: .68rem 1.3rem; font-family: var(--ff);
      font-size: .85rem; font-weight: 600; cursor: pointer;
      transition: opacity .2s, transform .15s; white-space: nowrap;
    }
    .btn-add:hover { opacity: .88; transform: translateY(-1px); }

    /* ── Search ── */
    .search-wrap {
      display: flex; align-items: center;
      background: var(--white); border: 1.5px solid var(--border);
      border-radius: 12px; padding: .55rem 1rem; gap: .5rem;
      max-width: 360px; margin-bottom: 1.5rem; transition: border-color .2s;
    }
    .search-wrap:focus-within { border-color: var(--primary); box-shadow: 0 0 0 3px rgba(79,70,229,.1); }
    .search-wrap span { color: var(--muted); }
    .search-wrap input {
      border: none; outline: none; font-family: var(--ff);
      font-size: .9rem; color: var(--text); width: 100%; background: transparent;
    }
    .search-wrap input::placeholder { color: #9ca3af; }

    /* ── Grid ── */
    .grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(295px,1fr)); gap: 1rem; }

    .card {
      background: var(--white); border-radius: 16px;
      padding: 1.4rem; box-shadow: var(--shadow);
      display: flex; align-items: center; gap: 1rem;
      position: relative; transition: box-shadow .2s, transform .2s;
    }
    .card:hover { box-shadow: var(--shadow-lg); transform: translateY(-2px); }

    /* Avatar */
    .avatar {
      width: 50px; height: 50px; border-radius: 13px; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center;
      color: #fff; font-size: 1.25rem; font-weight: 700;
    }
    .av0 { background: linear-gradient(135deg,#4f46e5,#7c3aed); }
    .av1 { background: linear-gradient(135deg,#059669,#10b981); }
    .av2 { background: linear-gradient(135deg,#d97706,#f59e0b); }
    .av3 { background: linear-gradient(135deg,#dc2626,#f87171); }
    .av4 { background: linear-gradient(135deg,#0284c7,#38bdf8); }

    .info { flex: 1; min-width: 0; }
    .info .name {
      font-size: .98rem; font-weight: 600;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }
    .info .career {
      font-size: .76rem; color: var(--muted); margin-top: .15rem;
      white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    }

    /* Grade */
    .grade { text-align: center; flex-shrink: 0; }
    .grade .num { font-size: 1.55rem; font-weight: 700; line-height: 1; }
    .grade .bar {
      width: 50px; height: 4px; background: var(--border);
      border-radius: 9999px; margin-top: .35rem; overflow: hidden;
    }
    .grade .fill { height: 100%; border-radius: 9999px; }

    .gh .num  { color: var(--green); } .gh .fill { background: var(--green); }
    .gm .num  { color: var(--blue);  } .gm .fill { background: var(--blue);  }
    .gl .num  { color: var(--red);   } .gl .fill { background: var(--red);   }

    /* Delete */
    .del {
      position: absolute; top: .7rem; right: .7rem;
      width: 24px; height: 24px; border-radius: 7px;
      border: none; background: transparent; cursor: pointer;
      font-size: .85rem; display: flex; align-items: center; justify-content: center;
      color: #d1d5db; transition: background .15s, color .15s;
    }
    .del:hover { background: #fee2e2; color: var(--red); }

    /* Empty */
    .empty { text-align: center; padding: 3rem; color: var(--muted); grid-column: 1/-1; }
    .empty .ei { font-size: 2.5rem; display: block; margin-bottom: .6rem; }

    /* Toast */
    .toast {
      position: fixed; bottom: 1.5rem; right: 1.5rem;
      background: #1e1b4b; color: #fff;
      padding: .75rem 1.3rem; border-radius: 12px; font-size: .85rem; font-weight: 500;
      opacity: 0; pointer-events: none; transform: translateY(8px) scale(.97);
      transition: all .28s cubic-bezier(.4,0,.2,1); z-index: 200;
      box-shadow: 0 8px 24px rgba(0,0,0,.18);
    }
    .toast.show { opacity: 1; transform: translateY(0) scale(1); }

    @media (max-width: 680px) {
      .stats    { grid-template-columns: 1fr; }
      .form-row { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

<header>
  <div class="logo">Edu<span>Track</span></div>
  <div class="badge" id="hdr-count">{{ students|length }} estudiantes</div>
</header>

<main>

  <!-- Stats -->
  <div class="stats">
    <div class="stat">
      <div class="stat-icon si-total">🎓</div>
      <div class="stat-info">
        <p>Total</p>
        <strong id="st-total">{{ students|length }}</strong>
      </div>
    </div>
    <div class="stat">
      <div class="stat-icon si-avg">📊</div>
      <div class="stat-info">
        <p>Promedio</p>
        <strong id="st-avg">{{ avg }}</strong>
      </div>
    </div>
    <div class="stat">
      <div class="stat-icon si-top">🏆</div>
      <div class="stat-info">
        <p>Mejor nota</p>
        <strong id="st-top">{{ top }}</strong>
      </div>
    </div>
  </div>

  <!-- Form -->
  <div class="form-card">
    <h2>➕ Nuevo estudiante</h2>
    <div class="form-row">
      <div class="fg"><label>Nombre</label><input id="i-name"   placeholder="Ej. María López" /></div>
      <div class="fg"><label>Carrera</label><input id="i-career" placeholder="Ej. Ingeniería" /></div>
      <div class="fg"><label>Nota (0-10)</label><input id="i-grade" type="number" min="0" max="10" step="0.1" placeholder="8.5" /></div>
      <button class="btn-add" onclick="addStudent()">Agregar</button>
    </div>
  </div>

  <!-- Search -->
  <div class="search-wrap">
    <span>🔍</span>
    <input id="search" placeholder="Buscar estudiante…" oninput="render()">
  </div>

  <!-- Grid -->
  <div class="grid" id="grid"></div>

</main>

<div class="toast" id="toast"></div>

<script>
  const COLORS = ['av0','av1','av2','av3','av4'];
  let students = {{ students_json }};

  function gradeClass(g)  { return g >= 8.5 ? 'gh' : g >= 7 ? 'gm' : 'gl'; }
  function initial(name)  { return name.trim()[0].toUpperCase(); }
  function colorOf(id)    { return COLORS[id % COLORS.length]; }

  function render() {
    const q    = document.getElementById('search').value.toLowerCase();
    const list = students.filter(s =>
      !q || s.name.toLowerCase().includes(q) || s.career.toLowerCase().includes(q)
    );
    const grid = document.getElementById('grid');

    if (!list.length) {
      grid.innerHTML = '<div class="empty"><span class="ei">🔍</span>Sin resultados.</div>';
    } else {
      grid.innerHTML = list.map(s => `
        <div class="card" id="c${s.id}">
          <div class="avatar ${colorOf(s.id)}">${initial(s.name)}</div>
          <div class="info">
            <div class="name">${esc(s.name)}</div>
            <div class="career">${esc(s.career)}</div>
          </div>
          <div class="grade ${gradeClass(s.grade)}">
            <div class="num">${s.grade.toFixed(1)}</div>
            <div class="bar"><div class="fill" style="width:${s.grade*10}%"></div></div>
          </div>
          <button class="del" onclick="del(${s.id})" title="Eliminar">✕</button>
        </div>`).join('');
    }
    updateStats();
  }

  function updateStats() {
    const n   = students.length;
    const avg = n ? (students.reduce((a,s)=>a+s.grade,0)/n).toFixed(1) : '—';
    const top = n ? Math.max(...students.map(s=>s.grade)).toFixed(1) : '—';
    document.getElementById('st-total').textContent = n;
    document.getElementById('st-avg').textContent   = avg;
    document.getElementById('st-top').textContent   = top;
    document.getElementById('hdr-count').textContent = n + ' estudiantes';
  }

  async function addStudent() {
    const name   = document.getElementById('i-name').value.trim();
    const career = document.getElementById('i-career').value.trim();
    const grade  = parseFloat(document.getElementById('i-grade').value);
    if (!name)                      return toast('Ingresa el nombre');
    if (!career)                    return toast('Ingresa la carrera');
    if (isNaN(grade)||grade<0||grade>10) return toast('Nota debe ser entre 0 y 10');

    const res  = await fetch('/api/students', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({name, grade, career})
    });
    const data = await res.json();
    students.push(data);
    render();
    toast(`"${name}" agregado ✓`);
    ['i-name','i-career','i-grade'].forEach(id => document.getElementById(id).value = '');
  }

  async function del(id) {
    await fetch(`/api/students/${id}`, {method:'DELETE'});
    students = students.filter(s => s.id !== id);
    render();
    toast('Estudiante eliminado');
  }

  function toast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg; t.classList.add('show');
    clearTimeout(t._t); t._t = setTimeout(()=>t.classList.remove('show'), 2400);
  }

  function esc(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

  render();
</script>
</body>
</html>"""


@app.route("/")
def index():
    avg = f"{sum(s['grade'] for s in STUDENTS)/len(STUDENTS):.1f}" if STUDENTS else "—"
    top = f"{max(s['grade'] for s in STUDENTS):.1f}" if STUDENTS else "—"
    return render_template_string(HTML, students=STUDENTS,
                                  students_json=json.dumps(STUDENTS), avg=avg, top=top)

@app.route("/api/students", methods=["GET"])
def get_students():
    q = request.args.get("q", "").lower()
    result = [s for s in STUDENTS if not q or q in s["name"].lower()]
    return jsonify(result)

@app.route("/api/students", methods=["POST"])
def add_student():
    global _next_id
    data = request.get_json() or {}
    name   = str(data.get("name", "")).strip()
    career = str(data.get("career", "")).strip()
    try:
        grade = float(data["grade"])
    except (KeyError, ValueError):
        return jsonify({"error": "grade inválido"}), 400
    if not name:               return jsonify({"error": "name requerido"}), 400
    if not (0 <= grade <= 10): return jsonify({"error": "grade fuera de rango"}), 400
    student = {"id": _next_id, "name": name, "grade": grade, "career": career}
    _next_id += 1
    STUDENTS.append(student)
    return jsonify(student), 201

@app.route("/api/students/<int:sid>", methods=["DELETE"])
def delete_student(sid):
    global STUDENTS
    before = len(STUDENTS)
    STUDENTS = [s for s in STUDENTS if s["id"] != sid]
    if len(STUDENTS) == before:
        return jsonify({"error": "no encontrado"}), 404
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)