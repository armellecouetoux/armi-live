// Comentarios de clientes para la agenda ARMI.
// Pega este código en Extensiones → Apps Script de una Google Sheet nueva y
// despliégalo como aplicación web (Ejecutar como: yo · Acceso: cualquier persona).

const HOJA = 'Comentarios';
const VISTAS = ['cbqupfrchc', 'lm7l8rjbdi']; // una por cliente

function hoja_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(HOJA);
  if (!sh) {
    sh = ss.insertSheet(HOJA);
    sh.appendRow(['Fecha', 'Vista', 'Tarea', 'Nombre', 'Comentario']);
  }
  return sh;
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  const vista = String((e && e.parameter && e.parameter.v) || '');
  if (VISTAS.indexOf(vista) < 0) return json_([]);
  const filas = hoja_().getDataRange().getValues().slice(1);
  return json_(filas
    .filter(function (r) { return r[1] === vista; })
    .map(function (r) { return { ts: new Date(r[0]).toISOString(), task: r[2], name: r[3], text: r[4] }; }));
}

function doPost(e) {
  let d = {};
  try { d = JSON.parse(e.postData.contents); } catch (err) { return json_({ ok: false }); }
  if (d.website) return json_({ ok: true });          // campo trampa contra spam
  const vista = String(d.v || '');
  const nombre = String(d.name || '').trim().slice(0, 60);
  const texto = String(d.text || '').trim().slice(0, 1500);
  const tarea = String(d.task || '').slice(0, 60);
  if (VISTAS.indexOf(vista) < 0 || !nombre || !texto) return json_({ ok: false });
  const lock = LockService.getScriptLock(); lock.waitLock(5000);
  try { hoja_().appendRow([new Date(), vista, tarea, nombre, texto]); } finally { lock.releaseLock(); }
  return json_({ ok: true });
}
