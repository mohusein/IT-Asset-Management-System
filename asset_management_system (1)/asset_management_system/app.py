from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-this-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_tag = db.Column(db.String(50), unique=True, nullable=False)
    device_type = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.String(30), default='Available')
    assigned_to = db.Column(db.String(100), nullable=True)
    department = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class AssetLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    asset = db.relationship('Asset', backref=db.backref('logs', lazy=True, cascade='all, delete-orphan'))


@app.route('/')
def dashboard():
    assets = Asset.query.order_by(Asset.created_at.desc()).all()
    total_assets = Asset.query.count()
    available = Asset.query.filter_by(status='Available').count()
    assigned = Asset.query.filter_by(status='Assigned').count()
    maintenance = Asset.query.filter_by(status='Maintenance').count()
    retired = Asset.query.filter_by(status='Retired').count()
    return render_template(
        'dashboard.html',
        assets=assets,
        total_assets=total_assets,
        available=available,
        assigned=assigned,
        maintenance=maintenance,
        retired=retired,
    )


@app.route('/assets/new', methods=['GET', 'POST'])
def add_asset():
    if request.method == 'POST':
        asset = Asset(
            asset_tag=request.form['asset_tag'].strip(),
            device_type=request.form['device_type'].strip(),
            brand=request.form['brand'].strip(),
            model=request.form['model'].strip(),
            serial_number=request.form['serial_number'].strip(),
            status=request.form.get('status', 'Available'),
            assigned_to=request.form.get('assigned_to', '').strip() or None,
            department=request.form.get('department', '').strip() or None,
            location=request.form.get('location', '').strip() or None,
            notes=request.form.get('notes', '').strip() or None,
        )
        try:
            db.session.add(asset)
            db.session.commit()
            log = AssetLog(asset_id=asset.id, action='Created', notes='Asset added to inventory')
            db.session.add(log)
            db.session.commit()
            flash('Asset added successfully.', 'success')
            return redirect(url_for('dashboard'))
        except Exception:
            db.session.rollback()
            flash('Asset tag or serial number already exists.', 'danger')
    return render_template('asset_form.html', asset=None)


@app.route('/assets/<int:asset_id>')
def view_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    logs = AssetLog.query.filter_by(asset_id=asset.id).order_by(AssetLog.timestamp.desc()).all()
    return render_template('asset_detail.html', asset=asset, logs=logs)


@app.route('/assets/<int:asset_id>/edit', methods=['GET', 'POST'])
def edit_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    if request.method == 'POST':
        asset.asset_tag = request.form['asset_tag'].strip()
        asset.device_type = request.form['device_type'].strip()
        asset.brand = request.form['brand'].strip()
        asset.model = request.form['model'].strip()
        asset.serial_number = request.form['serial_number'].strip()
        asset.status = request.form.get('status', asset.status)
        asset.assigned_to = request.form.get('assigned_to', '').strip() or None
        asset.department = request.form.get('department', '').strip() or None
        asset.location = request.form.get('location', '').strip() or None
        asset.notes = request.form.get('notes', '').strip() or None
        try:
            db.session.commit()
            db.session.add(AssetLog(asset_id=asset.id, action='Updated', notes='Asset details updated'))
            db.session.commit()
            flash('Asset updated successfully.', 'success')
            return redirect(url_for('view_asset', asset_id=asset.id))
        except Exception:
            db.session.rollback()
            flash('Could not update asset. Check for duplicate asset tag or serial number.', 'danger')
    return render_template('asset_form.html', asset=asset)


@app.route('/assets/<int:asset_id>/checkout', methods=['POST'])
def checkout_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    user_name = request.form['assigned_to'].strip()
    department = request.form.get('department', '').strip()
    notes = request.form.get('notes', '').strip()
    asset.status = 'Assigned'
    asset.assigned_to = user_name
    asset.department = department or asset.department
    db.session.add(AssetLog(asset_id=asset.id, action='Checked Out', user_name=user_name, notes=notes))
    db.session.commit()
    flash('Asset checked out successfully.', 'success')
    return redirect(url_for('view_asset', asset_id=asset.id))


@app.route('/assets/<int:asset_id>/checkin', methods=['POST'])
def checkin_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    notes = request.form.get('notes', '').strip()
    previous_user = asset.assigned_to
    asset.status = 'Available'
    asset.assigned_to = None
    db.session.add(AssetLog(asset_id=asset.id, action='Checked In', user_name=previous_user, notes=notes))
    db.session.commit()
    flash('Asset checked in successfully.', 'success')
    return redirect(url_for('view_asset', asset_id=asset.id))


@app.route('/assets/<int:asset_id>/delete', methods=['POST'])
def delete_asset(asset_id):
    asset = Asset.query.get_or_404(asset_id)
    db.session.delete(asset)
    db.session.commit()
    flash('Asset deleted successfully.', 'success')
    return redirect(url_for('dashboard'))


@app.route('/seed')
def seed_data():
    if Asset.query.count() > 0:
        flash('Sample data already exists.', 'info')
        return redirect(url_for('dashboard'))
    sample_assets = [
        Asset(asset_tag='LAP-1001', device_type='Laptop', brand='Dell', model='Latitude 5420', serial_number='SN-DL-5420-001', status='Assigned', assigned_to='Amina Yusuf', department='Finance', location='Phoenix Office'),
        Asset(asset_tag='MON-2001', device_type='Monitor', brand='HP', model='EliteDisplay E243', serial_number='SN-HP-E243-001', status='Available', location='Storage Room'),
        Asset(asset_tag='PHN-3001', device_type='Phone', brand='Cisco', model='IP Phone 8841', serial_number='SN-CS-8841-001', status='Maintenance', location='IT Bench'),
    ]
    db.session.add_all(sample_assets)
    db.session.commit()
    for asset in sample_assets:
        db.session.add(AssetLog(asset_id=asset.id, action='Created', notes='Seed sample asset'))
    db.session.commit()
    flash('Sample assets added.', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
