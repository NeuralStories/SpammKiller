# Política de Retención y Borrado - SCAMEATER

## Períodos de retención

| Categoría | Retention | Notas |
|-----------|-----------|-------|
| Audios de llamada | 30 días | Borrado automático por job nocturno |
| Transcripciones completas | 90 días | Redacción previa si requerido |
| Transcripciones redactadas | 2 años | Disponibles para análisis |
| Datos de llamada (metadatos) | 2 años | Estadísticas agregadas |
| Registros de auditoría | 5 años | Cumplimiento legal |
| Datos de API (costes) | 5 años | Ningún dato personal |
| Datos de kampana/organización | 5 años | Anonimizable tras 2 años sin actividad |

## Procedimiento de borrado

### Script: services/worker/jobs/retention_cleanup.py
- Job nocturno (00:00 UTC)
- Identifica registros más antiguos que el período de retención
- Para audios: elimina archivo de MinIO, luego registro de BD
- Para transcripciones: mantiene versión redactada, elimina completa
- Genera informe en `audit_log`

### Antes del borrado
- Verificación de que no existe retención legal activa
- Registro en `audit_log` con acción `retention_cleanup` y qué se eliminó

## Derechos de los interesados
- Los spammers NO son sujetos RGPD (comunicación no solicitada no constituye relación)
- Los usuarios del sistema tienen derechos de acceso, rectificación y supresión
-操 作 requires approval from legal role

## Revisión
Esta política se revisa anualmente o cuando cambia la legislación aplicable.