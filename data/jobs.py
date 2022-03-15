import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from datetime import date
from sqlalchemy_serializer import SerializerMixin


class Job(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)
    job = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    collaborators = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.Date, default=date(1, 1, 1))
    end_date = sqlalchemy.Column(sqlalchemy.Date, default=date(1, 1, 1))
    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False)
    user = orm.relation('User')
    categories = orm.relation("Category", secondary="jobs_to_categories", backref="jobs")
