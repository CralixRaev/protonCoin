from db.database import db


class Criteria(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    basis_id = db.Column(db.Integer, db.ForeignKey("basis.id"), index=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    basis = db.relation("Basis", back_populates='criteria')


class CriteriaQuery:
    @staticmethod
    def get_all_criterias() -> list[Criteria]:
        return Criteria.query.all()

    @staticmethod
    def create_criteria(name, basis_id, cost) -> Criteria:
        criteria = Criteria()
        criteria.name = name
        criteria.basis_id = basis_id
        criteria.cost = cost
        db.session.add(criteria)
        db.session.commit()
        return criteria
