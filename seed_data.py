from app import create_app, db
from app.models import Role, Department

app = create_app()
with app.app_context():
    # --- Seed roles ---
    roles = ["citizen", "admin", "superadmin"]
    for r in roles:
        if not Role.query.filter_by(name=r).first():
            db.session.add(Role(name=r))
    
    # --- Seed sample departments ---
    departments = ["Sanitation", "Roads", "Water Supply", "Electricity"]
    for d in departments:
        if not Department.query.filter_by(name=d).first():
            db.session.add(Department(name=d))
    
    db.session.commit()
    print("✅ Roles and Departments seeded successfully!")

