from flask import Blueprint, render_template, request
from Backend.Memcache.s3Helper import put_image_to_s3

image_routes = Blueprint("image_routes", __name__)


@image_routes.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        key = request.form.get('key')
        response = put_image_to_s3(request, key)
        # TODO: call memcache
        return render_template("add_key.html", save_status=response)
    return render_template("add_key.html")


@image_routes.route('/show_image', methods=['GET', 'POST'])
def show_image():
    if request.method == 'POST':
        key = request.form.get('key')
        # TODO: call memcache
        # result = 
        # if result != -1:
        #     image = get_image_from_s3(key)
        #     return render_template('show_image.html', exists=True, filename=image, source="Source from cache")
        # else:
        #     print("Image not found.")
        #     return render_template('show_image.html', exists=False, filename="Does not Exist")
    return render_template('show_image.html')
