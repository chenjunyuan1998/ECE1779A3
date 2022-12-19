#################
#  ECE 1779 A3  #
#################

gunicorn --bind 0.0.0.0:5000 wsgi_frontend:webapp &
#gunicorn --bind 0.0.0.0:5001 wsgi_db:webapp &
gunicorn --bind 0.0.0.0:5002 wsgi_storage:webapp &
echo "Webapps started"