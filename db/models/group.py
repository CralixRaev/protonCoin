from db.database import db
from db.models.user import User


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    stage = db.Column(db.Integer, nullable=False)
    letter = db.Column(db.String(8), nullable=False)

    users = db.relationship('User', back_populates='group', order_by=User.surname)

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

    @staticmethod
    def get_group_by_id(group_id) -> Group:
        return Group.query.get(group_id)\


    @staticmethod
    def get_group_by_stage_letter(stage, letter) -> Group:
        return Group.query.filter(Group.stage == stage, Group.letter == letter).first()

    @staticmethod
    def update_group(group: Group, stage: int, letter: str) -> Group:
        db.session.rollback()

        group.stage = stage
        group.letter = letter

        db.session.commit()
        return group

    @staticmethod
    def delete_group(group: Group):
        Group.query.filter(Group.id == group.id).delete()
        db.session.commit()
