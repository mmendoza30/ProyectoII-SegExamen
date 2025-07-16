/* ==============================================================
   La Liga Insights  –  Esquema general ANSI-SQL
   Tabla      :  partidos
   Objetivo   :  almacenar temporada 2024-2025 de la liga española
   Autor      :  Profesor
   Fecha      :  3-jul-2025
   ============================================================== */

/* ───────────────────────── 1. Creación de la tabla ───────────────────────── */
CREATE TABLE partidos (
    /* Clave primaria y contexto temporal */
    id_partido                INTEGER       PRIMARY KEY,   -- identificador único
    temporada                 SMALLINT      NOT NULL,      -- 2024, 2025
    fecha                     DATE          NOT NULL,      -- AAAA-MM-DD

    /* Identidad de los equipos */
    equipo_local              VARCHAR(100)  NOT NULL,
    equipo_visita             VARCHAR(100)  NOT NULL,

    /* Marcador final */
    goles_local               SMALLINT      NOT NULL,
    goles_visita              SMALLINT      NOT NULL,

    /* Métricas avanzadas (si se dispone) */
    xg_local                  DECIMAL(5,2),               -- expected goals
    xg_visita                 DECIMAL(5,2),

    /* Posesión (%) */
    posesion_local            DECIMAL(5,2),
    posesion_visita           DECIMAL(5,2),

    /* Disciplina */
    amarillas_local           SMALLINT,
    amarillas_visita          SMALLINT,
    rojas_local               SMALLINT,
    rojas_visita              SMALLINT,

    /* ─── Volumen ofensivo ─── */
    tiros_local               SMALLINT,
    tiros_visita              SMALLINT,
    tiros_a_puerta_local      SMALLINT,
    tiros_a_puerta_visita     SMALLINT,

    /* ─── Balón parado & presión ─── */
    corners_local             SMALLINT,
    corners_visita            SMALLINT,
    faltas_local              SMALLINT,
    faltas_visita             SMALLINT,

    /*  Reglas de integridad básicas  */
    CHECK (goles_local            >= 0 AND goles_visita            >= 0),
    CHECK (amarillas_local        >= 0 AND amarillas_visita        >= 0),
    CHECK (rojas_local            >= 0 AND rojas_visita            >= 0),
    CHECK (tiros_local            >= 0 AND tiros_visita            >= 0),
    CHECK (tiros_a_puerta_local   >= 0 AND tiros_a_puerta_visita   >= 0),
    CHECK (corners_local          >= 0 AND corners_visita          >= 0),
    CHECK (faltas_local           >= 0 AND faltas_visita           >= 0)
);



/* ───────────────────────── 2. Vistas de apoyo ───────────────────────── */
/* Ventaja local por temporada */
CREATE VIEW v_ventaja_local AS
SELECT
    temporada,
    COUNT(*)                                                        AS total_partidos,
    SUM(CASE WHEN goles_local > goles_visita THEN 1 ELSE 0 END)     AS victorias_local,
    CAST(100.0 *
         SUM(CASE WHEN goles_local > goles_visita THEN 1 ELSE 0 END) /
         COUNT(*) AS DECIMAL(5,2))                                  AS pct_victorias_local
FROM partidos
GROUP BY temporada
ORDER BY temporada;

/* Eficiencia ofensiva básica (goles / tiros) */
CREATE VIEW v_eficiencia_ofensiva AS
SELECT
    id_partido,
    equipo_local,
    equipo_visita,
    CASE WHEN tiros_local > 0
         THEN CAST(goles_local * 1.0 / tiros_local AS DECIMAL(6,3))
         ELSE NULL END AS gol_por_tiro_local,
    CASE WHEN tiros_visita > 0
         THEN CAST(goles_visita * 1.0 / tiros_visita AS DECIMAL(6,3))
         ELSE NULL END AS gol_por_tiro_visita
FROM partidos;

/* ───────────────────────── 3. Ejemplo de verificación ───────────────────────── */
/*
SELECT * FROM v_ventaja_local ORDER BY temporada DESC;
SELECT equipo_local, AVG(gol_por_tiro_local)
  FROM v_eficiencia_ofensiva
 GROUP BY equipo_local
 ORDER BY 2 DESC
 FETCH FIRST 10 ROWS ONLY;
*/
