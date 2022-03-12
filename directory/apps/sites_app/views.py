from . import sites
from directory.utils.request import json_only
from directory import db
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from .models import Site


@sites.route('/', methods=['POST'])
@json_only
@jwt_required()
def create_site():
    args = request.get_json()
    try:
        new_site = Site()
        new_site.name = args.get('name')
        new_site.description = args.get('description')
        new_site.address = args.get('address')
        db.session.add(new_site)
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        return {'error': f'{e}'}, 400
    except IntegrityError:
        db.session.rollback()
        return {"Error": "Address is duplicated."}, 400

    return {"message": "Site added successfully.", "id": new_site.id}, 201

@sites.route('/', methods=['GET'])
def read_sites():
    sites = Site.query.all()
    sites = [
        {"id": site.id, 'name': site.name, 'address': site.address} for site in sites
    ]

    return jsonify(sites)

@sites.route('/<int:site_id>', methods=['GET'])
def read_site(site_id):
    site = Site.query.get(site_id)
    if not site:
        return {'error': 'Site with given ID not found!'}, 404

    return {"id": site.id,
            'name': site.name,
            'create_date': site.create_date,
            'description': site.description,
            'address': site.address}, 200
