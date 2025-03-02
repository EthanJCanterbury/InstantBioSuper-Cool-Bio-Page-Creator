from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import json
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

os.makedirs("static/uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)

BIO_DATA_FILE = "data/bios.json"

if not os.path.exists(BIO_DATA_FILE):
    with open(BIO_DATA_FILE, "w") as f:
        json.dump({}, f)


def get_bios():
    with open(BIO_DATA_FILE, "r") as f:
        return json.load(f)


def save_bios(bios):
    with open(BIO_DATA_FILE, "w") as f:
        json.dump(bios, f)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/api/docs')
def api_docs():
    """Display API documentation"""
    return render_template('api_docs.html')


@app.route('/docs')
def web_docs():
    """Display web documentation"""
    return render_template('documentation.html')


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        bios = get_bios()
        bio_name = request.form.get('bio_name')

        if not bio_name or not bio_name.isalnum():
            flash("Bio name must be alphanumeric!")
            return redirect(url_for('create'))

        if bio_name in bios:
            flash("This bio name already exists!")
            return redirect(url_for('create'))

        profile_image = None
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                file_path = os.path.join("static/uploads", filename)
                file.save(file_path)
                profile_image = f"/uploads/{filename}"

        bio_data = {
            "name": request.form.get('name', ''),
            "tagline": request.form.get('tagline', ''),
            "bio": request.form.get('bio', ''),
            "profile_image": profile_image,
            "theme": request.form.get('theme', 'default'),
            "social_links": {
                "twitter": request.form.get('twitter', ''),
                "instagram": request.form.get('instagram', ''),
                "linkedin": request.form.get('linkedin', ''),
                "github": request.form.get('github', '')
            },
            "custom_css": request.form.get('custom_css', '')
        }

        bios[bio_name] = bio_data
        save_bios(bios)

        flash("Bio created successfully!")
        return redirect(url_for('view_bio', bio_name=bio_name))

    return render_template('create.html')


@app.route('/<bio_name>')
def view_bio(bio_name):
    bios = get_bios()
    if bio_name not in bios:
        flash("Bio not found!")
        return redirect(url_for('home'))

    return render_template('bio.html', bio=bios[bio_name], bio_name=bio_name)


@app.route('/edit/<bio_name>', methods=['GET', 'POST'])
def edit_bio(bio_name):
    bios = get_bios()
    if bio_name not in bios:
        flash("Bio not found!")
        return redirect(url_for('home'))

    if request.method == 'POST':
        # Process profile image (ONLY WHEN UPLOADED!!!!!)
        profile_image = bios[bio_name].get('profile_image')
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename:
                filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
                file_path = os.path.join("static/uploads", filename)
                file.save(file_path)
                profile_image = f"/uploads/{filename}"

        bios[bio_name] = {
            "name": request.form.get('name', ''),
            "tagline": request.form.get('tagline', ''),
            "bio": request.form.get('bio', ''),
            "profile_image": profile_image,
            "theme": request.form.get('theme', 'default'),
            "social_links": {
                "twitter": request.form.get('twitter', ''),
                "instagram": request.form.get('instagram', ''),
                "linkedin": request.form.get('linkedin', ''),
                "github": request.form.get('github', '')
            },
            "custom_css": request.form.get('custom_css', '')
        }

        save_bios(bios)
        flash("Bio updated successfully!")
        return redirect(url_for('view_bio', bio_name=bio_name))

    return render_template('edit.html', bio=bios[bio_name], bio_name=bio_name)


# Endpoints
@app.route('/api/bios', methods=['GET'])
def api_get_bios():
    """Get a list of all bio names"""
    bios = get_bios()
    return jsonify({
        "success": True,
        "count": len(bios),
        "bios": list(bios.keys())
    })


@app.route('/api/bio/<bio_name>', methods=['GET'])
def api_get_bio(bio_name):
    """Get details for a specific bio by name"""
    bios = get_bios()
    if bio_name not in bios:
        return jsonify({"success": False, "error": "Bio not found"}), 404
    return jsonify({
        "success": True,
        "bio_name": bio_name,
        "bio": bios[bio_name]
    })


@app.route('/api/bio/<bio_name>', methods=['POST'])
def api_create_bio(bio_name):
    """Create a new bio with the specified name"""
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request must be JSON"
        }), 400

    bios = get_bios()
    if bio_name in bios:
        return jsonify({"success": False, "error": "Bio already exists"}), 409

    data = request.get_json()

    required_fields = ['name', 'bio']
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400

    bio_data = {
        "name":
        data.get('name'),
        "tagline":
        data.get('tagline', ''),
        "bio":
        data.get('bio'),
        "profile_image":
        data.get('profile_image'),
        "theme":
        data.get('theme', 'default'),
        "social_links":
        data.get('social_links', {
            "twitter": "",
            "instagram": "",
            "linkedin": "",
            "github": ""
        }),
        "custom_css":
        data.get('custom_css', '')
    }

    bios[bio_name] = bio_data
    save_bios(bios)

    return jsonify({
        "success": True,
        "message": "Bio created successfully",
        "bio_name": bio_name
    }), 201


@app.route('/api/bio/<bio_name>', methods=['PUT'])
def api_update_bio(bio_name):
    """Update an existing bio with the specified name"""
    if not request.is_json:
        return jsonify({
            "success": False,
            "error": "Request must be JSON"
        }), 400

    bios = get_bios()
    if bio_name not in bios:
        return jsonify({"success": False, "error": "Bio not found"}), 404

    data = request.get_json()
    current_bio = bios[bio_name]

    bio_data = {
        "name":
        data.get('name', current_bio.get('name')),
        "tagline":
        data.get('tagline', current_bio.get('tagline', '')),
        "bio":
        data.get('bio', current_bio.get('bio')),
        "profile_image":
        data.get('profile_image', current_bio.get('profile_image')),
        "theme":
        data.get('theme', current_bio.get('theme', 'default')),
        "social_links":
        data.get(
            'social_links',
            current_bio.get('social_links', {
                "twitter": "",
                "instagram": "",
                "linkedin": "",
                "github": ""
            })),
        "custom_css":
        data.get('custom_css', current_bio.get('custom_css', ''))
    }

    bios[bio_name] = bio_data
    save_bios(bios)

    return jsonify({
        "success": True,
        "message": "Bio updated successfully",
        "bio_name": bio_name
    })


@app.route('/api/bio/<bio_name>', methods=['DELETE'])
def api_delete_bio(bio_name):
    """Delete a bio with the specified name"""
    bios = get_bios()
    if bio_name not in bios:
        return jsonify({"success": False, "error": "Bio not found"}), 404

    del bios[bio_name]
    save_bios(bios)

    return jsonify({
        "success": True,
        "message": "Bio deleted successfully",
        "bio_name": bio_name
    })


@app.route('/api/themes', methods=['GET'])
def api_get_themes():
    """Get a list of available themes"""
    themes = ["default", "dark", "light", "colorful", "minimal"]
    return jsonify({"success": True, "count": len(themes), "themes": themes})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
