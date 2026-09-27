# Los Guajiros

Tienda mobile-first de productos caseros en Marianao. Incluye búsqueda, categorías, carrito persistente, recogida, mensajería por zona y confirmación del pedido por WhatsApp.

## Desarrollo

```bash
npm install
npm run dev
```

## Verificación

```bash
npm test
npm run build
```

La identidad del negocio, el número temporal y las tarifas están centralizados en `config/tenant.json`. Los productos y su disponibilidad están en `lib/catalog.js`. El panel administrativo queda especificado en `ADMIN-PHASE-2.md`.

Pendientes de sustitución: número definitivo de WhatsApp, enlace del grupo, dirección completa y fotografías reales de los productos futuros.
