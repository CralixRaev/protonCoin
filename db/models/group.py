from typing import Mapping

from db.database import db
from db.models.user import User


class Group(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    stage: int = db.Column(db.Integer, nullable=False)
    letter: str = db.Column(db.String(8), nullable=False)

    users = db.relationship('User', back_populates='group', order_by=User.surname)

    @property
    def name(self) -> str:
        return f'{self.stage}{self.letter}'


class GroupQuery:
    @staticmethod
    def get_all_groups() -> list[Group]:
        return Group.query.all()

    @staticmethod
    def _fill_from_attributes(attributes: Mapping[str, str], group: Group):
        types = group.__annotations__
        for k, v in attributes.items():
            if k.startswith("group"):
                k = k.split(".")[-1]
                if hasattr(group, k):
                    setattr(group, k, types.get(k, str)(v))

    @staticmethod
    def create_group(attributes: Mapping[str, str]) -> Group:
        db.session.rollback()
        group = Group()
        GroupQuery._fill_from_attributes(attributes, group)
        db.session.add(group)
        db.session.commit()
        return group

    @staticmethod
    def create_or_update(attributes: Mapping[str, str]) -> Group:
        group_query = Group.query.filter(Group.id == attributes['group.id'])
        if group_query.count() > 0:
            return GroupQuery.update_group(group_query.first(), attributes)
        else:
            return GroupQuery.create_group(attributes)

    @staticmethod
    def get_group_by_id(group_id) -> Group:
        return Group.query.get(group_id)\


    @staticmethod
    def get_group_by_stage_letter(stage, letter) -> Group:
        return Group.query.filter(Group.stage == stage, Group.letter == letter).first()

    @staticmethod
    def update_group(group: Group, attributes: Mapping[str, str]) -> Group:
        db.session.rollback()
        GroupQuery._fill_from_attributes(attributes, group)
        db.session.commit()
        return group

    @staticmethod
    def delete_group(group: Group):
        Group.query.filter(Group.id == group.id).delete()
        db.session.commit()
