-- Trading-Archetypen Modul Registration
-- Auszuführen in der Railway PostgreSQL Datenbank

-- 1. Prüfe, ob Kategorie "Trading-Strategien" existiert
-- Falls nicht, erstelle sie:

INSERT INTO module_category (name, slug, icon, description, sort_order, is_active, created_at, updated_at)
SELECT '1. Trading-Strategien', 'trading-strategien', '🎯',
       'Grundlegende und fortgeschrittene Trading-Methoden und -Strategien',
       1, TRUE, NOW(), NOW()
WHERE NOT EXISTS (
    SELECT 1 FROM module_category WHERE slug = 'trading-strategien'
);

-- 2. Prüfe, ob das Modul bereits existiert, falls nicht, füge es hinzu:

INSERT INTO learning_module (
    category_id,
    subcategory_id,
    title,
    slug,
    description,
    icon,
    template_file,
    content_type,
    is_published,
    is_lead_magnet,
    required_subscription_levels,
    estimated_duration,
    difficulty_level,
    sort_order,
    view_count,
    created_at,
    updated_at
)
SELECT
    mc.id,
    NULL,
    'Trading-Methoden Vertiefung',
    'trading-archetypen',
    'Verstehe die drei Säulen erfolgreichen Tradings: Buy & Hold, Position Trading und Swing Trading. Lerne den Keulen-Kombi-Prozess und finde deinen systematischen Edge.',
    '🎯',
    'trading_archetypen.html',
    'html',
    TRUE,
    FALSE,
    '["premium", "elite", "masterclass"]',
    25,
    'intermediate',
    100,
    0,
    NOW(),
    NOW()
FROM module_category mc
WHERE mc.slug = 'trading-strategien'
AND NOT EXISTS (
    SELECT 1 FROM learning_module WHERE slug = 'trading-archetypen'
);

-- 3. Verifizierung: Zeige das neu erstellte Modul an
SELECT
    lm.id,
    lm.title,
    lm.slug,
    lm.template_file,
    mc.name as category_name,
    lm.is_published,
    lm.difficulty_level
FROM learning_module lm
JOIN module_category mc ON lm.category_id = mc.id
WHERE lm.slug = 'trading-archetypen';
