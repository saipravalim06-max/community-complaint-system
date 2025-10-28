from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Complaint, Department
from .forms import ComplaintForm
import os
from werkzeug.utils import secure_filename
from flask import current_app

citizen_bp = Blueprint("citizen", __name__, template_folder="../templates")

@citizen_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    form = ComplaintForm()
    form.departments.choices = [(d.id, d.name) for d in Department.query.all()]

    # Handle form submission
    if request.method == "POST":
        if not form.validate_on_submit():
            flash("⚠️ Please fill in all required fields correctly.", "danger")
        else:
            # Create complaint
            complaint = Complaint(
                user_id=current_user.id,
                title=form.title.data,
                description=form.description.data,
                address=form.address.data,
                status="pending",
                latitude=request.form.get("latitude"),
                longitude=request.form.get("longitude"),
            )

            # Handle image upload(s)
            image_filenames = []
            for img in request.files.getlist("images"):
                 if img and img.filename != "":
                      filename = secure_filename(img.filename)
                      img.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                      image_filenames.append(filename)
            complaint.image_filenames = ",".join(image_filenames)

            # Link departments
            for dept_id in form.departments.data:
                dept = Department.query.get(dept_id)
                if dept:
                    complaint.departments.append(dept)

            db.session.add(complaint)
            db.session.commit()

            flash("✅ Complaint submitted successfully!", "success")
            return redirect(url_for("citizen.dashboard"))

    # Fetch complaints for this user
    complaints = Complaint.query.filter_by(user_id=current_user.id).order_by(Complaint.created_at.desc()).all()
    total = len(complaints)
    pending = sum(1 for c in complaints if c.status == "pending")
    in_progress = sum(1 for c in complaints if c.status == "in_progress")
    resolved = sum(1 for c in complaints if c.status == "resolved")

    return render_template(
        "citizen_dashboard.html",
        complaints=complaints,
        total_complaints=total,
        pending_count=pending,
        in_progress_count=in_progress,
        resolved_count=resolved,
        form=form,
        departments=Department.query.all(),
         GOOGLE_MAPS_API_KEY=current_app.config["GOOGLE_MAPS_API_KEY"]
    )
