#!/bin/bash
mongodump --host localhost --port 27017  --username vohungvi --password viscomsolution --out /var/orchid/backup_db --db orchid
cd /var/orchid/backup_db
tar -czvf /var/orchid/download/orchid_database.tar.gz orchid