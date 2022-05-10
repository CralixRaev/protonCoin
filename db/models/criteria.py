from db.database import db


class Criteria(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    basis_id = db.Column(db.Integer, db.ForeignKey("basis.id"), index=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

    basis = db.relation("Basis", back_populates='criteria')

    def __str__(self) -> str:
        return f"{self.name} - {self.cost}"

    def __repr__(self) -> str:
        return self.__str__()

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

    @staticmethod
    def get_criteria_by_id(criteria_id) -> Criteria:
        return Criteria.query.get(criteria_id)
