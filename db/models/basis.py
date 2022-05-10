from db.database import db


class Basis(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    name = db.Column(db.String(255))

    criteria = db.relation("Criteria", back_populates='basis')


class BasisQuery:
    @staticmethod
    def get_all_basises() -> list[Basis]:
        return Basis.query.all()

    @staticmethod
    def create_basis(name) -> Basis:
        basis = Basis()
        basis.name = name
        db.session.add(basis)
        db.session.commit()
        return basis
