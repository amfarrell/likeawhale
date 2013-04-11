echo "assuming you are in your virtualenv..."
pip install -r requirements.txt
cd learning/django-allauth
python setup.py install
cd ../..
echo "the password is sekkrit"
echo "DELETE FROM south_migrationhistory WHERE app_name='accounts';" | ./manage.py dbshell
echo "DROP SEQUENCE accounts_userwordknowledge_id_seq CASCADE" | ./manage.py dbshell
echo "DROP SEQUENCE accounts_userlanguageknowledge_id_seq CASCADE" | ./manage.py dbshell
echo "DROP TABLE accounts_userlanguageknowledge" | ./manage.py dbshell
echo "DROP TABLE accounts_userwordknowledge" | ./manage.py dbshell
./manage.py schemamigration 'allauth' --init
./manage.py schemamigration 'allauth.account' --init
./manage.py migrate 'allauth.account'
./manage.py migrate 'learning'
./manage.py migrate 'articles'
