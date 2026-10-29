import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
    handlers=[logging.FileHandler("app.log", encoding="utf-8"), logging.StreamHandler()],
)
log = logging.getLogger("backup")

log.debug("not shown at INFO level")
log.info("backup started")
log.warning("disk %d%% full", 85)
try:
    1 / 0
except ZeroDivisionError:
    log.exception("calculation failed")   # includes the traceback
