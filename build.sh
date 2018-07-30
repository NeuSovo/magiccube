pip install -r requirements.txt
pip install uwsgi
yum install -y mysql-devel
pip install mysqlclient
python manage.py makemigrations event utils index shrine project paragraph
python manage.py migrate
python manage.py collectstatic
python manage.py runserver