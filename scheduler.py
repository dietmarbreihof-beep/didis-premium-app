# scheduler.py - Tägliche Modul-Freischaltung für Didis Trading Academy
"""
Scheduled Job für die automatische Modul-Freischaltung:
- Läuft täglich um 00:05 UTC
- Schaltet Module basierend auf Registrierungsdatum und Subscription-Level frei
- Sendet Email-Benachrichtigungen für neue Freischaltungen
"""

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import logging

# Logger konfigurieren
logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.INFO)
logger = logging.getLogger(__name__)

# Scheduler-Instanz (wird in init_scheduler() konfiguriert)
scheduler = None


def get_modules_for_subscription_level(subscription_level, db, LearningModule):
    """
    Gibt alle Module zurück, die für ein bestimmtes Subscription-Level verfügbar sind.
    Sortiert nach sort_order (global).
    
    Args:
        subscription_level: z.B. "free", "premium", "elite"
        db: SQLAlchemy DB-Instanz
        LearningModule: LearningModule Model-Klasse
    
    Returns:
        Liste von LearningModule-Objekten, sortiert nach sort_order
    """
    try:
        # Alle veröffentlichten Module laden
        all_modules = LearningModule.query.filter_by(is_published=True).order_by(LearningModule.sort_order).all()
        
        # Nach Subscription-Level filtern
        matching_modules = []
        for module in all_modules:
            # Lead-Magnete sind für alle verfügbar
            if module.is_lead_magnet:
                matching_modules.append(module)
            # Prüfe ob das Subscription-Level passt
            elif subscription_level in (module.required_subscription_levels or []):
                matching_modules.append(module)
        
        return matching_modules
    except Exception as e:
        logger.error(f"Fehler beim Laden der Module für {subscription_level}: {e}")
        return []


def unlock_modules_for_user(user, db, LearningModule, UserModuleUnlock, send_unlock_email=None):
    """
    Schaltet Module für einen User basierend auf Subscription-Level und Tagen seit Start frei.
    
    Args:
        user: User-Objekt
        db: SQLAlchemy DB-Instanz
        LearningModule: LearningModule Model-Klasse
        UserModuleUnlock: UserModuleUnlock Model-Klasse
        send_unlock_email: Optional - Funktion zum Senden der Freischaltungs-Email
    
    Returns:
        Liste der neu freigeschalteten Module
    """
    subscription_level = user.subscription_type.value
    
    # Tage seit Subscription-Start berechnen
    days_since_start = user.get_days_since_subscription_start(subscription_level)
    
    if days_since_start <= 0:
        return []
    
    # Alle Module für dieses Subscription-Level holen
    available_modules = get_modules_for_subscription_level(subscription_level, db, LearningModule)
    
    # Bereits freigeschaltete Module für diesen User laden
    existing_unlocks = UserModuleUnlock.query.filter_by(
        user_id=user.id,
        subscription_level=subscription_level
    ).all()
    
    existing_module_ids = {unlock.module_id for unlock in existing_unlocks}
    
    # Module freischalten bis zum aktuellen Tag
    newly_unlocked = []
    
    for idx, module in enumerate(available_modules):
        unlock_day = idx + 1  # Tag 1, 2, 3, ...
        
        # Nur freischalten wenn:
        # 1. Der Tag erreicht ist
        # 2. Das Modul noch nicht freigeschaltet wurde
        if unlock_day <= days_since_start and module.id not in existing_module_ids:
            try:
                # Neue Freischaltung erstellen
                unlock = UserModuleUnlock(
                    user_id=user.id,
                    module_id=module.id,
                    unlock_day=unlock_day,
                    subscription_level=subscription_level,
                    unlocked_at=datetime.utcnow(),
                    notification_sent=False
                )
                db.session.add(unlock)
                newly_unlocked.append((module, unlock))
                
                logger.info(f"✅ Modul '{module.title}' für User {user.username} freigeschaltet (Tag {unlock_day})")
            except Exception as e:
                logger.error(f"Fehler beim Freischalten von {module.title} für {user.username}: {e}")
    
    # Änderungen speichern
    if newly_unlocked:
        try:
            db.session.commit()
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Freischaltungen: {e}")
            db.session.rollback()
            return []
    
    return newly_unlocked


def send_unlock_notifications(user, newly_unlocked, send_email_func, base_url):
    """
    Sendet Email-Benachrichtigungen für neu freigeschaltete Module.
    
    Args:
        user: User-Objekt
        newly_unlocked: Liste von (module, unlock) Tupeln
        send_email_func: send_email Funktion aus app.py
        base_url: Basis-URL der App (z.B. https://didis-premium-app-production.up.railway.app)
    """
    for module, unlock in newly_unlocked:
        if unlock.notification_sent:
            continue
        
        try:
            # Email senden
            success = send_email_func(
                to=user.email,
                subject=f'🔓 Neues Modul freigeschaltet: {module.title}',
                template='module_unlocked',
                username=user.username,
                first_name=user.first_name or user.username,
                module_title=module.title,
                module_description=module.description or '',
                module_icon=module.icon or '📚',
                module_url=f"{base_url}/module/{module.slug}",
                unlock_day=unlock.unlock_day
            )
            
            if success:
                unlock.notification_sent = True
                unlock.notification_sent_at = datetime.utcnow()
                logger.info(f"📧 Email gesendet: {module.title} → {user.email}")
            else:
                logger.warning(f"⚠️ Email konnte nicht gesendet werden: {module.title} → {user.email}")
                
        except Exception as e:
            logger.error(f"Fehler beim Email-Versand für {module.title} an {user.email}: {e}")


def run_daily_unlock_job(app):
    """
    Haupt-Job für die tägliche Modul-Freischaltung.
    Wird täglich um 00:05 UTC ausgeführt.
    
    Args:
        app: Flask App-Instanz
    """
    with app.app_context():
        from app import db, User, LearningModule, UserModuleUnlock, send_email
        import os
        
        logger.info("="*60)
        logger.info("🔄 Starte tägliche Modul-Freischaltung...")
        logger.info(f"   Zeitpunkt: {datetime.utcnow().isoformat()}")
        logger.info("="*60)
        
        # Basis-URL aus Environment oder Fallback
        base_url = os.environ.get('BASE_URL', 'https://didis-premium-app-production.up.railway.app')
        
        # Alle aktiven User laden
        try:
            active_users = User.query.filter_by(is_active=True).all()
            logger.info(f"📊 Verarbeite {len(active_users)} aktive User...")
        except Exception as e:
            logger.error(f"Fehler beim Laden der User: {e}")
            return
        
        total_unlocks = 0
        total_emails = 0
        
        for user in active_users:
            try:
                # Module für diesen User freischalten
                newly_unlocked = unlock_modules_for_user(
                    user=user,
                    db=db,
                    LearningModule=LearningModule,
                    UserModuleUnlock=UserModuleUnlock
                )
                
                if newly_unlocked:
                    total_unlocks += len(newly_unlocked)
                    
                    # Email-Benachrichtigungen senden
                    send_unlock_notifications(
                        user=user,
                        newly_unlocked=newly_unlocked,
                        send_email_func=send_email,
                        base_url=base_url
                    )
                    
                    # Änderungen speichern (notification_sent Flags)
                    db.session.commit()
                    total_emails += len([u for m, u in newly_unlocked if u.notification_sent])
                    
            except Exception as e:
                logger.error(f"Fehler bei User {user.username}: {e}")
                db.session.rollback()
                continue
        
        logger.info("="*60)
        logger.info(f"✅ Tägliche Modul-Freischaltung abgeschlossen!")
        logger.info(f"   Freigeschaltete Module: {total_unlocks}")
        logger.info(f"   Gesendete Emails: {total_emails}")
        logger.info("="*60)


def init_scheduler(app):
    """
    Initialisiert den APScheduler für die tägliche Modul-Freischaltung.
    
    Args:
        app: Flask App-Instanz
    """
    global scheduler
    
    # Scheduler nur starten wenn nicht bereits aktiv
    if scheduler is not None and scheduler.running:
        logger.info("⚠️ Scheduler läuft bereits")
        return scheduler
    
    scheduler = BackgroundScheduler()
    
    # Job hinzufügen: Täglich um 00:05 UTC
    scheduler.add_job(
        func=lambda: run_daily_unlock_job(app),
        trigger=CronTrigger(hour=0, minute=5, timezone='UTC'),
        id='daily_module_unlock',
        name='Tägliche Modul-Freischaltung',
        replace_existing=True
    )
    
    # Scheduler starten
    scheduler.start()
    logger.info("🚀 APScheduler gestartet - Tägliche Modul-Freischaltung um 00:05 UTC")
    
    # Scheduler beim App-Shutdown beenden
    atexit.register(lambda: shutdown_scheduler())
    
    return scheduler


def shutdown_scheduler():
    """Beendet den Scheduler sauber."""
    global scheduler
    if scheduler is not None and scheduler.running:
        scheduler.shutdown()
        logger.info("🛑 APScheduler beendet")


def trigger_manual_unlock(app):
    """
    Löst die Modul-Freischaltung manuell aus (z.B. für Tests).
    
    Args:
        app: Flask App-Instanz
    """
    logger.info("🔧 Manuelle Modul-Freischaltung ausgelöst...")
    run_daily_unlock_job(app)

