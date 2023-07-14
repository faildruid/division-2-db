#!/bin/ash
# Runs on every start of the Division 2 Docker container

# Stop when an error occures
set -e

# Give time for the database server to initialize
echo "⏳ Waiting 5 seconds for the database server to initialize"
sleep 5

#If there is database backup file to restore, restore the database.
BACKUP_FILE="/source/backup/div2db.bkp"

if [ -e $BACKUP_FILE ]; then
    echo "💡 We have a database backup file $BACKUP_FILE to restore"
    psql -t -U $DIVISION_DB_USER -h $DIVISION_DB_HOST -d $DIVISION_DB_NAME -f backup/test_db.sql | sed -e 's/^[[:space:]]*//' | sed 's/\r$//' > /source/backup/tables.out
    read -r has_data < /source/backup/tables.out
    if [ "$has_data" = "0" ] ; then
        echo "⏳ The Division 2 database needs to be restored, restoring."
        pg_restore -U $DIVISION_DB_USER -h $DIVISION_DB_HOST -d $DIVISION_DB_NAME $BACKUP_FILE
    else
        echo "💡 The Division 2 database has already been restored, continuing."
    fi
fi

cd "$DIVISION_ROOT"
cp /source/development/division_config.py /source/division_config.py
# Prepare the web static content

echo "⏳ Running initial systems check..."
division-server migrate
division-server collectstatic --noinput

# # Nõw for some jiggery pokery in the background to setup a superuser for development.
# cat <<EOP | division-server shell
# from django.contrib.auth.models import User
# from users.models import Token
# u = User.objects.filter(username='${DIVISION_SUPERUSER_NAME}')
# if not u:
#     u = User.objects.create_superuser('${DIVISION_SUPERUSER_NAME}', '${DIVISION_SUPERUSER_EMAIL}', '${DIVISION_SUPERUSER_PASSWORD}')
#     Token.objects.create(user=u, key='${DIVISION_SUPERUSER_API_TOKEN}')
# else:
#     u = u[0]
#     if u.email != '${DIVISION_SUPERUSER_EMAIL}':
#         u.email = '${DIVISION_SUPERUSER_EMAIL}'
#     if not u.check_password('${DIVISION_SUPERUSER_PASSWORD}'):
#         u.set_password('${DIVISION_SUPERUSER_PASSWORD}')
#     u.save()
#     t = Token.objects.filter(user=u)
#     if t:
#         t = t[0]
#         if t.key != '${DIVISION_SUPERUSER_API_TOKEN}':
#             t.key = '${DIVISION_SUPERUSER_API_TOKEN}'
#             t.save()

# exit()
# EOP

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "💡 Superuser Username: ${DIVISION_SUPERUSER_NAME}, E-Mail: ${DIVISION_SUPERUSER_EMAIL}, Password ${DIVISION_SUPERUSER_PASSWORD}"

# Launch the division server
exec division-server runserver 0.0.0.0:8080 --insecure
