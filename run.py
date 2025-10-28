from app import create_app

app = create_app()

# ---------- TEMPORARY SEED ROUTE ----------
from app import db
from app.models import Role, Department

@app.route("/seed")
def seed_data():
    with app.app_context():
        roles = ["citizen", "admin", "superadmin"]
        for r in roles:
            if not Role.query.filter_by(name=r).first():
                db.session.add(Role(name=r))

        departments = ["Sanitation", "Roads", "Water Supply", "Electricity"]
        for d in departments:
            if not Department.query.filter_by(name=d).first():
                db.session.add(Department(name=d))

        db.session.commit()
    return "✅ Roles and Departments seeded successfully!"
# ---------- END TEMP ROUTE ----------


if __name__ == "__main__":
    app.run(debug=True)
