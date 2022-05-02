from db.database import db


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    stage = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(8), nullable=False)

    users = db.relationship('User', back_populates='group')

    @property
    def name(self) -> str:
        return f'{self.stage}{self.letter}'


class GroupQuery:
    @staticmethod
    def get_all_groups() -> list[Group]:
        return Group.query.all()

    @staticmethod
    def create_group(stage: int, letter) -> Group:
        db.session.rollback()
        group = Group()
        group.stage = stage
        group.letter = letter
        db.session.add(group)
        db.session.commit()
        return group
