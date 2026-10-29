import shutil, os
shutil.copy("config.json", "config.backup.json")
shutil.move("old.txt", "archive/old.txt")
shutil.make_archive("backup", "zip", "reports")   # zip a folder
os.remove("temp.txt")
print(shutil.disk_usage("/"))
