from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Complaint, Department
import os
from werkzeug.utils import secure_filename
from flask import current_app


admin_bp = Blueprint("admin", __name__, template_folder="../templates")


@admin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role_id != 2:
        flash("Unauthorized access!", "danger")
        return redirect(url_for("citizen.dashboard"))

    dept_id = current_user.department_id
    complaints = (
        Complaint.query.join(Complaint.departments)
        .filter(Department.id == dept_id)
        .order_by(Complaint.created_at.desc())
        .all()
    )

    total = len(complaints)
    pending = len([c for c in complaints if c.status == "pending"])
    in_progress = len([c for c in complaints if c.status == "in_progress"])
    resolved = len([c for c in complaints if c.status == "resolved"])

    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        total_complaints=total,
        pending_count=pending,
        in_progress_count=in_progress,
        resolved_count=resolved,
        GOOGLE_MAPS_API_KEY=current_app.config["GOOGLE_MAPS_API_KEY"]
    )


@admin_bp.route("/complaint/<int:complaint_id>", methods=["POST"])
@login_required
def complaint_detail(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)

    action = request.form.get("action")  # "in_progress" or "resolved"
    resolution_note = request.form.get("resolution_note")
    files = request.files.getlist("resolved_image")

    if action in ["in_progress", "resolved"]:
        complaint.status = action

    if resolution_note:
        complaint.resolution_note = resolution_note

    image_filenames = []
    for file in files:
        if file and file.filename != "":
            filename = secure_filename(f"resolved_{complaint.id}_{file.filename}")
            upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(upload_path)
            image_filenames.append(filename)

    if image_filenames:
        complaint.resolved_images = ",".join(image_filenames)

    db.session.commit()
    flash(f"✅ Complaint marked as {action.replace('_', ' ').title()}!", "success")
    return redirect(url_for("admin.dashboard"))
