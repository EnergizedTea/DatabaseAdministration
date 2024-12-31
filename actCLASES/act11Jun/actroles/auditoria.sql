-- Crear tabla de auditoría
CREATE TABLE auditoria (
    id SERIAL PRIMARY KEY,
    accion VARCHAR(50),
    tabla VARCHAR(50),
    usuario VARCHAR(50),
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    datos JSONB
);

-- Crear trigger para INSERT
CREATE OR REPLACE FUNCTION log_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria (accion, tabla, usuario, datos)
    VALUES ('INSERT', TG_TABLE_NAME, SESSION_USER, row_to_json(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_insert
-- Cambiar por el nombre de la tabla
AFTER INSERT ON Estudiantes 
FOR EACH ROW EXECUTE FUNCTION log_insert();

-- Crear trigger para UPDATE
CREATE OR REPLACE FUNCTION log_update() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria (accion, tabla, usuario, datos)
    VALUES ('UPDATE', TG_TABLE_NAME, SESSION_USER, row_to_json(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_update
AFTER UPDATE ON Estudiantes
FOR EACH ROW EXECUTE FUNCTION log_update();

-- Crear trigger para DELETE
CREATE OR REPLACE FUNCTION log_delete() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO auditoria (accion, tabla, usuario, datos)
    VALUES ('DELETE', TG_TABLE_NAME, SESSION_USER, row_to_json(OLD));
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_log_delete
AFTER DELETE ON Estudiantes
FOR EACH ROW EXECUTE FUNCTION log_delete();