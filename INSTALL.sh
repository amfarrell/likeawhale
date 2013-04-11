echo "assuming you are in your virtualenv..."
pip install -r requirements.txt
cd learning/django-allauth
python setup.py install
cd ../..
echo "the password is sekkrit"
echo "UPDATE south_migrationhistory SET app_name='learning' WHERE app_name='accounts';" | ./manage.py dbshell
./manage.py schemamigration 'allauth' --init
./manage.py schemamigration 'allauth.account' --init
./manage.py migrate 'allauth.account'
./manage.py migrate 'learning'
./manage.py migrate 'articles'
