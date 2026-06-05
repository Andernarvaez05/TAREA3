from flask import Flask, render_template_string, request, jsonify
import json

app = Flask(__name__)

STUDENTS = [
    {"id": 1, "name": "Ana García",   "grade": 9.5, "career": "Ingeniería"},
    {"id": 2, "name": "Luis Pérez",   "grade": 7.8, "career": "Medicina"},
    {"id": 3, "name": "Sofía Torres", "grade": 8.3, "career": "Arquitectura"},
]
_next_id = 4

HTML = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>EduTrack</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f0f4ff; }
    h1 { color: #4f46e5; }
    .form { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    input { padding: 8px; margin: 5px; border: 1px solid #ddd; border-radius: 4px; }
    button { padding: 8px 16px; background: #4f46e5; color: white; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #3730a3; }
    table { width: 100%; border-collapse: collapse; background: white; border-radius: 8px; overflow: hidden; }
    th { background: #4f46e5; color: white; padding: 12px; text-align: left; }
    td { padding: 12px; border-bottom: 1px solid #eee; }
    tr:hover { background: #f0f4ff; }
    .badge { padding: 4px 10px; border-radius: 20px; font-size: 0.85em; }
    .high { background: #d1fae5; color: #065f46; }
    .mid  { background: #dbeafe; color: #1e40af; }
    .low  { background: #fee2e2; color: #991b1b; }
    .del  { background: #dc2626; padding: 4px 10px; }
    .del:hover { background: #b91c1c; }
  </style>
</head>
<body>
  <h1>🎓 EduTrack — Gestión de Estudiantes</h1>

  <div class="form">
    <h3>Agregar estudiante</h3>
    <input id="name"   placeholder="Nombre" />
    <input id="career" placeholder="Carrera" />
    <input id="grade"  placeholder="Nota (0-10)" type="number" min="0" max="10" step="0.1" />
    <button onclick="agregar()">Agregar</button>
  </div>

  <table>
    <thead>
      <tr><th>#</th><th>Nombre</th><th>Carrera</th><th>Nota</th><th></th></tr>
    </thead>
    <tbody id="tbody"></tbody>
  </table>

  <script>
    let students = {{ students_json }};

    function render() {
      document.getElementById('tbody').innerHTML = students.map((s, i) => `
        <tr>
          <td>${i + 1}</td>
          <td>${s.name}</td>
          <td>${s.career}</td>
          <td><span class="badge ${s.grade >= 8.5 ? 'high' : s.grade >= 7 ? 'mid' : 'low'}">${s.grade.toFixed(1)}</span></td>
          <td><button class="del" onclick="eliminar(${s.id})">Eliminar</button></td>
        </tr>`).join('');
    }

    async function agregar() {
      const name   = document.getElementById('name').value.trim();
      const career = document.getElementById('career').value.trim();
      const grade  = parseFloat(document.getElementById('grade').value);
      if (!name || !career || isNaN(grade)) return alert('Completa todos los campos');
      const r = await fetch('/api/students', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, career, grade })
      });
      students.push(await r.json());
      render();
      ['name', 'career', 'grade'].forEach(id => document.getElementById(id).value = '');
    }

    async function eliminar(id) {
      await fetch('/api/students/' + id, { method: 'DELETE' });
      students = students.filter(s => s.id !== id);
      render();
    }

    render();
  </script>
</body>
</html>"""


@app.route("/")
def index():
    return render_template_string(HTML, students_json=json.dumps(STUDENTS))

@app.route("/api/students", methods=["GET"])
def get_students():
    return jsonify(STUDENTS)

@app.route("/api/students", methods=["POST"])
def add_student():
    global _next_id
    data   = request.get_json() or {}
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
    app.run(host="0.0.0.0", port=5000, debug=False)