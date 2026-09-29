# Master to-do · Agenda de clientes Q4

Panel de ARMI con la agenda y las tareas por cliente (Rocket Digital, Shopify) y una pestaña de Inicio que lo resume todo.

**Web:** https://armellecouetoux.github.io/master-to-do/

## Cómo se guardan los cambios

- Checks, estados (Pendiente, On going, Prioritario, Canceled, Done) y enlaces se guardan en `state.json`, en este repositorio.
- Cualquier dispositivo que abra la web lee `state.json`, así que todos ven lo mismo.
- Para **guardar** cambios, cada navegador necesita un token de GitHub (pulsa *Sincronizar dispositivos* al final de la página):
  1. GitHub → Settings → Developer settings → Fine-grained tokens → *Generate new token*.
  2. Repository access: *Only select repositories* → `master-to-do`.
  3. Permissions → Contents: *Read and write*.
- El token se queda solo en ese navegador; nunca se sube al repositorio.
- Sin token, los cambios se guardan solo en ese navegador.

## Compartir una pestaña (solo lectura)

- Rocket Digital: https://armellecouetoux.github.io/master-to-do/rocket/
- Shopify: https://armellecouetoux.github.io/master-to-do/shopify/

Muestran solo esa pestaña, sin editar y sin notas de reuniones, y se actualizan con cada cambio. Ojo: el repositorio es público, así que quien llegue al repo o a `state.json` puede ver todo.

## Archivos

- `index.html` — la página.
- `rocket/`, `shopify/` — vistas de solo lectura de cada pestaña.
- `state.json` — el estado de las tareas (lo escribe la página; no hace falta editarlo a mano).
