# Panel administrativo · Fase 2

La primera versión vende mediante catálogo, carrito y confirmación por WhatsApp. La siguiente fase incorporará acceso protegido para administrar productos, categorías, precios, disponibilidad del día, inventario opcional, pedidos, tarifas de mensajería, horarios, promociones y configuración centralizada de WhatsApp.

La disponibilidad actual vive en `lib/catalog.js` mediante `disabled` y `tag`. El número temporal está centralizado en `config/tenant.json`. No se debe mostrar un enlace público al panel hasta implementar autenticación.
