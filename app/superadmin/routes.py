from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Complaint, Department
from flask import current_app


superadmin_bp = Blueprint("superadmin", __name__, template_folder="../templates")

# ---------------------------
# SUPER ADMIN DASHBOARD
# ---------------------------
@superadmin_bp.route("/dashboard")
@login_required
def dashboard():
    if current_user.role_id != 3:  # 3 = superadmin
        flash("Unauthorized access!", "danger")
        return redirect(url_for("index"))

    # Counts for all complaints
    total = Complaint.query.count()
    pending = Complaint.query.filter_by(status="pending").count()
    in_progress = Complaint.query.filter_by(status="in_progress").count()
    resolved = Complaint.query.filter_by(status="resolved").count()

    # Complaints grouped by department
    department_data = []
    departments = Department.query.all()
    for dept in departments:
        dept_complaints = (
            Complaint.query.join(Complaint.departments)
            .filter(Department.id == dept.id)
            .all()
        )
        department_data.append({
            "id": dept.id,
            "name": dept.name,
            "total": len(dept_complaints),
            "pending": len([c for c in dept_complaints if c.status == "pending"]),
            "in_progress": len([c for c in dept_complaints if c.status == "in_progress"]),
            "resolved": len([c for c in dept_complaints if c.status == "resolved"]),
        })

    # Department filter
    dept_filter = request.args.get("department_id", type=int)
    if dept_filter:
        complaints = (
            Complaint.query.join(Complaint.departments)
            .filter(Department.id == dept_filter)
            .order_by(Complaint.created_at.desc())
            .all()
        )
        selected_dept = Department.query.get(dept_filter)
    else:
        complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
        selected_dept = None

    return render_template(
    "superadmin_dashboard.html",
    complaints=complaints,
    total=total,
    pending=pending,
    in_progress=in_progress,
    resolved=resolved,
    department_data=department_data,
    selected_dept=selected_dept,
    GOOGLE_MAPS_API_KEY=current_app.config["GOOGLE_MAPS_API_KEY"]
)