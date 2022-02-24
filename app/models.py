from flask import current_app, url_for
from app.search import add_to_index, remove_from_index, query_index
from app import db
import redis
import rq

access_rights = db.Table(
    'AccessRights',
    db.Column('group_id', db.String(128), db.ForeignKey(
        'group.id'), primary_key=True),
    db.Column('access_id', db.String(128), db.ForeignKey('access.id'), primary_key=True))


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data
    
    @staticmethod
    def _to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query
        data = {
            'items': [item.to_dict() for item in resources]
        }
        return data


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class Task(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    complete = db.Column(db.Boolean, default=False)
    user_redirected = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        return '<Task {}>'.format(self.name + " " + self.desscription)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100


class Group(PaginatedAPIMixin, db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(128), index=True)
    module_id = db.Column(db.Integer, db.ForeignKey('module.id'))
    rights = db.relationship(
        'Access', secondary=access_rights, back_populates="groups")
    permission = db.Column(db.Integer)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'module_id': self.module_id,
            'permission': self.permission,
            'links': {
                'access_rights': url_for('api.get_access_rights', id=self.id),
            }
        }
        return data


class Access(db.Model):
    id = db.Column(db.String(128), primary_key=True)
    name = db.Column(db.String(120), index=True)
    model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
    read = db.Column(db.Boolean, default=False)
    write = db.Column(db.Boolean, default=False)
    create = db.Column(db.Boolean, default=False)
    delete = db.Column(db.Boolean, default=False)
    groups = db.relationship(
        'Group', secondary=access_rights, back_populates="rights")
    
    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'model_id': self.model_id,
            'read': self.read,
            'write': self.write,
            'create': self.create,
            'delete': self.delete,
            'links': {
                # 'access_groups': url_for('api.get_access_groups', id=self.id),
            }
        }
        return data


