from apscheduler.schedulers.background import BackgroundScheduler

from devbot.devbot import app
from devbot.stats.stats_updator import update_stats_file

if __name__ == "__main__":
  scheduler = BackgroundScheduler()
  scheduler.add_job(update_stats_file, 'interval', seconds=app.config.get("STATS_UPDATE_FREQUENCY"))
  scheduler.start()

  # Run server
  app.run()
