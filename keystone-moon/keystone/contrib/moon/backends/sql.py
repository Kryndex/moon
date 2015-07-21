# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

import six
from uuid import uuid4
import copy

from keystone import config
from oslo_log import log
from keystone.common import sql
from keystone import exception
from keystone.contrib.moon.exception import *
from oslo_serialization import jsonutils
from keystone.contrib.moon import IntraExtensionDriver
from keystone.contrib.moon import TenantDriver
# from keystone.contrib.moon import InterExtensionDriver

CONF = config.CONF
LOG = log.getLogger(__name__)


class IntraExtension(sql.ModelBase, sql.DictBase):
    __tablename__ = 'intra_extensions'
    attributes = ['id', 'intra_extension']
    id = sql.Column(sql.String(64), primary_key=True)
    intra_extension = sql.Column(sql.JsonBlob(), nullable=True)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Tenant(sql.ModelBase, sql.DictBase):
    __tablename__ = 'tenants'
    attributes = ['id', 'tenant']
    id = sql.Column(sql.String(64), primary_key=True, nullable=False)
    tenant = sql.Column(sql.JsonBlob(), nullable=True)

    @classmethod
    def from_dict(cls, d):
        """Override parent from_dict() method with a different implementation.
        """
        new_d = d.copy()
        uuid = new_d.keys()[0]
        return cls(id=uuid, **new_d[uuid])

    def to_dict(self):
        """
        """
        tenant_dict = {}
        for key in ("id", "name", "authz", "admin"):
            tenant_dict[key] = getattr(self, key)
        return tenant_dict


class SubjectCategory(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject_categories'
    attributes = ['id', 'subject_category', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    subject_category = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ObjectCategory(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object_categories'
    attributes = ['id', 'object_category', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    object_category = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ActionCategory(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action_categories'
    attributes = ['id', 'action_category', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    action_category = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Subject(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subjects'
    attributes = ['id', 'subject', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    subject = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Object(sql.ModelBase, sql.DictBase):
    __tablename__ = 'objects'
    attributes = ['id', 'object', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    object = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Action(sql.ModelBase, sql.DictBase):
    __tablename__ = 'actions'
    attributes = ['id', 'action', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    action = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class SubjectScope(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject_scopes'
    attributes = ['id', 'subject_scope', 'intra_extension_id', 'subject_category_id']
    id = sql.Column(sql.String(64), primary_key=True)
    subject_scope = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    subject_category_id = sql.Column(sql.ForeignKey("subject_categories.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ObjectScope(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object_scopes'
    attributes = ['id', 'object_scope', 'intra_extension_id', 'object_category_id']
    id = sql.Column(sql.String(64), primary_key=True)
    object_scope = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    object_category_id = sql.Column(sql.ForeignKey("object_categories.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ActionScope(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action_scopes'
    attributes = ['id', 'action_scope', 'intra_extension_id', 'action_category']
    id = sql.Column(sql.String(64), primary_key=True)
    action_scope = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    action_category_id = sql.Column(sql.ForeignKey("action_categories.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class SubjectAssignment(sql.ModelBase, sql.DictBase):
    __tablename__ = 'subject_assignments'
    attributes = ['id', 'subject_assignment', 'intra_extension_id', 'subject_id', 'subject_category_id']
    id = sql.Column(sql.String(64), primary_key=True)
    subject_assignment = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    subject_id = sql.Column(sql.ForeignKey("subjects.id"), nullable=False)
    subject_category_id = sql.Column(sql.ForeignKey("subject_categories.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ObjectAssignment(sql.ModelBase, sql.DictBase):
    __tablename__ = 'object_assignments'
    attributes = ['id', 'object_assignment', 'intra_extension_id', 'object_id', 'object_category_id']
    id = sql.Column(sql.String(64), primary_key=True)
    object_assignment = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    object_id = sql.Column(sql.ForeignKey("objects.id"), nullable=False)
    object_category_id = sql.Column(sql.ForeignKey("object_categories.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class ActionAssignment(sql.ModelBase, sql.DictBase):
    __tablename__ = 'action_assignments'
    attributes = ['id', 'action_assignment', 'intra_extension_id', 'action_id', 'action_category_id']
    id = sql.Column(sql.String(64), primary_key=True)
    action_assignment = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    action_id = sql.Column(sql.ForeignKey("actions.id"), nullable=False)
    action_category_id = sql.Column(sql.ForeignKey("action_categories.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class AggregationAlgorithm(sql.ModelBase, sql.DictBase):
    __tablename__ = 'aggregation_algorithm'
    attributes = ['id', 'aggregation_algorithm', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    aggregation_algorithm = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class SubMetaRule(sql.ModelBase, sql.DictBase):
    __tablename__ = 'sub_meta_rules'
    attributes = ['id', 'sub_meta_rule', 'intra_extension_id']
    id = sql.Column(sql.String(64), primary_key=True)
    sub_meta_rule = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


class Rule(sql.ModelBase, sql.DictBase):
    __tablename__ = 'rules'
    attributes = ['id', 'rule', 'intra_extension_id', 'sub_meta_rule_id']
    id = sql.Column(sql.String(64), primary_key=True)
    rule = sql.Column(sql.JsonBlob(), nullable=True)
    intra_extension_id = sql.Column(sql.ForeignKey("intra_extensions.id"), nullable=False)
    sub_meta_rule_id = sql.Column(sql.ForeignKey("sub_meta_rules.id"), nullable=False)

    @classmethod
    def from_dict(cls, d):
        new_d = d.copy()
        return cls(**new_d)

    def to_dict(self):
        return dict(six.iteritems(self))


__all_objects__ = (
    IntraExtensionUnknown,
    Tenant,
    Subject,
    Object,
    Action,
    SubjectCategory,
    ObjectCategory,
    ActionCategory,
    SubjectScope,
    ObjectScope,
    ActionScope,
    SubjectAssignment,
    ObjectAssignment,
    ActionAssignment,
    AggregationAlgorithm,
    SubMetaRule,
    Rule,
)

class TenantConnector(TenantDriver):

    def get_tenants_dict(self):
        with sql.transaction() as session:
            query = session.query(Tenant)
            tenants = query.all()
            return {tenant.id: Tenant.to_dict(tenant) for tenant in tenants}

    def add_tenant_dict(self, tenant_id, tenant_dict):
        with sql.transaction() as session:
            new_ref = Tenant.from_dict(
                {
                    "id": tenant_id,
                    'tenant': tenant_dict
                }
            )
            session.add(new_ref)
            return new_ref.to_dict()

    def del_tenant(self, tenant_id):
        with sql.transaction() as session:
            query = session.query(Tenant)
            query = query.filter_by(id=tenant_id)
            tenant = query.first()
            session.delete(tenant)

    def set_tenant_dict(self, tenant_id, tenant_dict):
        with sql.transaction() as session:
            query = session.query(Tenant)
            query = query.filter_by(id=tenant_id)
            ref = query.first()
            tenant_ref = ref.to_dict()
            tenant_ref.update(tenant_dict)
            new_tenant = Tenant(
                id=tenant_id,
                tenant=tenant_ref
            )
            for attr in Tenant.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_tenant, attr))
            return Tenant.to_dict(ref)


class IntraExtensionConnector(IntraExtensionDriver):

    # Tenant functions

    def get_intra_extensions_dict(self):
        with sql.transaction() as session:
            query = session.query(IntraExtension.id)
            ref_list = query.all()
            return {_ref.id: _ref.intraextension for _ref in ref_list}

    # TODO (dthom): load_intra_extension(self):

    def del_intra_extension(self, intra_extension_id):
        with sql.transaction() as session:
            ref = session.query(IntraExtension).get(intra_extension_id)
            # Must delete all references to that IntraExtension
            for _object in __all_objects__:
                query = session.query(_object)
                query = query.filter_by(intra_extension_id=intra_extension_id)
                _ref = query.first()
                if _ref:
                    session.delete(_ref)
            session.flush()
            session.delete(ref)

    def set_intra_extension_dict(self, intra_extension_id, intra_extension_dict):
        with sql.transaction() as session:
            query = session.query(IntraExtension)
            query = query.filter_by(id=intra_extension_id)
            ref = query.first()
            intra_extension_ref = ref.to_dict()
            intra_extension_ref.update(intra_extension_dict)
            new_intra_extension = IntraExtension(id=intra_extension_id, intra_extension=intra_extension_ref)
            for attr in Tenant.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_intra_extension, attr))
            return IntraExtension.to_dict(ref)

    # Getter and Setter for subject_category

    def get_subject_categories_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref_list = query.all()
            return {_ref.id: _ref.subject_category for _ref in ref_list}

    def set_subject_category_dict(self, intra_extension_id, subject_category_id, subject_category_dict):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            new_ref = SubjectCategory.from_dict(
                {
                    "id": subject_category_id,
                    'subject_category': subject_category_dict,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in SubjectCategory.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_subject_categories_dict(intra_extension_id)[subject_category_id]

    def del_subject_category(self, intra_extension_id, subject_category_id):
        with sql.transaction() as session:
            query = session.query(SubjectCategory)
            query = query.filter_by(subject_category_id=subject_category_id)
            ref = query.first()
            session.delete(ref)

    # Getter and Setter for object_category

    def get_object_categories_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            return ref.to_dict()

    def set_object_category_dict(self, intra_extension_id, object_category_id, object_category_dict):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            new_ref = ObjectCategory.from_dict(
                {
                    "id": uuid4().hex,
                    'object_categories': object_categories,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in ObjectCategory.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def del_object_category(self, intra_extension_id, object_category_id):
        with sql.transaction() as session:
            query = session.query(ObjectCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            else:
                old_ref = ref.to_dict()
                object_categories = dict(old_ref["object_categories"])
                try:
                    object_categories.pop(object_category_id)
                except KeyError:
                    pass
                else:
                    new_ref = ObjectCategory.from_dict(
                        {
                            "id": old_ref["id"],
                            'object_categories': object_categories,
                            'intra_extension_id': old_ref["intra_extension_id"]
                        }
                    )
                    for attr in ObjectCategory.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for action_category

    def get_action_categories_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            return ref.to_dict()

    def set_action_category_dict(self, intra_extension_id, action_category_id, action_category_dict):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            new_ref = ActionCategory.from_dict(
                {
                    "id": uuid4().hex,
                    'action_categories': action_categories,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in ActionCategory.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def del_action_category(self, intra_extension_id, action_category_id):
        with sql.transaction() as session:
            query = session.query(ActionCategory)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            else:
                old_ref = ref.to_dict()
                action_categories = dict(old_ref["action_categories"])
                try:
                    action_categories.pop(action_category_id)
                except KeyError:
                    pass
                else:
                    new_ref = ActionCategory.from_dict(
                        {
                            "id": old_ref["id"],
                            'action_categories': action_categories,
                            'intra_extension_id': old_ref["intra_extension_id"]
                        }
                    )
                    for attr in ActionCategory.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Perimeter

    def get_subjects_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict()['subjects'] for _ref in ref_list}

    def set_subject_dict(self, intra_extension_id, subject_id, subject_dict):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(subject_id=subject_id)
            ref = query.first()
            new_ref = Subject.from_dict(
                {
                    "id": subject_id,
                    'subjects': subject_dict,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Subject.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_subjects_dict(intra_extension_id)[subject_id]

    def del_subject(self, intra_extension_id, subject_id):
        with sql.transaction() as session:
            query = session.query(Subject)
            query = query.filter_by(subject_id=subject_id)
            ref = query.first()
            session.delete(ref)

    def get_objects_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            return ref.to_dict()

    def set_object_dict(self, intra_extension_id, object_id, object_dict):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_id=intraa_extension_id)
            ref = query.first()
            new_ref = Object.from_dict(
                {
                    "id": uuid4().hex,
                    'objects': object_id,
                    'intra_extension_id': intraa_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Object.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def del_object(self, intra_extension_id, object_id):
        with sql.transaction() as session:
            query = session.query(Object)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            else:
                old_ref = ref.to_dict()
                objects = dict(old_ref["objects"])
                try:
                    objects.pop(object_id)
                except KeyError:
                    LOG.error("KeyError in remove_object {} | {}".format(object_id, objects))
                else:
                    new_ref = Object.from_dict(
                        {
                            "id": old_ref["id"],
                            'objects': objects,
                            'intra_extension_id': old_ref["intra_extension_id"]
                        }
                    )
                    for attr in Object.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))

    def get_actions_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            return ref.to_dict()

    def set_action_dict(self, intra_extension_id, action_id, action_dict):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            new_ref = Action.from_dict(
                {
                    "id": uuid4().hex,
                    'actions': action_id,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Action.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def del_action(self, intra_extension_id, action_id):
        with sql.transaction() as session:
            query = session.query(Action)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            else:
                old_ref = ref.to_dict()
                actions = dict(old_ref["actions"])
                try:
                    actions.pop(action_id)
                except KeyError:
                    LOG.error("KeyError in remove_action {} | {}".format(action_id, actions))
                else:
                    new_ref = Action.from_dict(
                        {
                            "id": old_ref["id"],
                            'actions': actions,
                            'intra_extension_id': old_ref["intra_extension_id"]
                        }
                    )
                    for attr in Action.attributes:
                        if attr != 'id':
                            setattr(ref, attr, getattr(new_ref, attr))

    # Getter and Setter for subject_scope

    def get_subject_scopes_dict(self, intra_extension_id, subject_category_id):
        with sql.transaction() as session:
            query = session.query(SubjectScope)
            query = query.filter_by(
                intra_extension_id=intra_extension_id,
                subject_category_id=subject_category_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict()['subject_scope'] for _ref in ref_list}

    def set_subject_scope_dict(self, intra_extension_id, subject_category_id, subject_scope_id, subject_scope_dict):
        with sql.transaction() as session:
            query = session.query(SubjectScope)
            query = query.filter_by(subject_scope_id=subject_scope_id)
            ref = query.first()
            new_ref = SubjectScope.from_dict(
                {
                    "id": subject_scope_id,
                    'subject_scope': subject_scope_dict,
                    'intra_extension_id': intra_extension_id,
                    'subject_category_id': subject_category_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in Subject.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_subject_scopes_dict(intra_extension_id, subject_category_id)[subject_scope_id]

    def del_subject_scope(self, intra_extension_id, subject_category_id, subject_scope_id):
        with sql.transaction() as session:
            query = session.query(SubjectScope)
            query = query.filter_by(subject_scope_id=subject_scope_id)
            ref = query.first()
            session.delete(ref)

    # Getter and Setter for object_category_scope

    def get_object_scopes_dict(self, intra_extension_id, object_category_id):
        with sql.transaction() as session:
            query = session.query(ObjectScope)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            result = copy.deepcopy(ref.to_dict())
            if object_category_id not in result["object_scopes"].keys():
                raise ObjectScopeUnknown()
            return result

    def set_object_scope_dict(self, intra_extension_id, object_category_id, object_scope_id, object_scope_dict):
        with sql.transaction() as session:
            query = session.query(ObjectScope)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                new_ref = ObjectScope.from_dict(
                    {
                        "id": uuid4().hex,
                        'object_scope': {object_category_id: object_scope_id},
                        'intra_extension_id': intra_extension_id
                    }
                )
                session.add(new_ref)
            else:
                tmp_ref = ref.to_dict()
                tmp_ref['object_scope'].update({object_category_id: object_scope_id})
                session.delete(ref)
                new_ref = ObjectScope.from_dict(tmp_ref)
                session.add(new_ref)
            return new_ref.to_dict()

    def del_object_scope(self, intra_extension_id, object_category_id, object_scope_id):
        with sql.transaction() as session:
            query = session.query(ObjectScope)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            old_ref = ref.to_dict()
            scope = dict(old_ref["object_scope"])
            if object_category_id not in scope:
                return
            try:
                scope[object_category_id].pop(object_scope_id)
            except KeyError:
                return
            new_ref = ObjectScope.from_dict(
                {
                    "id": old_ref["id"],
                    'object_scope': scope,
                    'intra_extension_id': old_ref["intra_extension_id"]
                }
            )
            for attr in ObjectScope.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for action_scope
 
    def get_action_scopes_dict(self, intra_extension_id, action_category_id):
        with sql.transaction() as session:
            query = session.query(ActionScope)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            result = copy.deepcopy(ref.to_dict())
            if action_category_id not in result["action_scope"].keys():
                raise ActionScopeUnknown()
            return result

    def set_action_scope_dict(self, intra_extension_id, action_category_id, action_scope_id, action_scope_dict):
        with sql.transaction() as session:
            query = session.query(ActionScope)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                new_ref = ActionScope.from_dict(
                    {
                        "id": uuid4().hex,
                        'action_scope': {action_category_id: action_scope_id},
                        'intra_extension_id': intra_extension_id
                    }
                )
                session.add(new_ref)
            else:
                tmp_ref = ref.to_dict()
                tmp_ref['action_scope'].update({action_category_id: action_scope_id})
                session.delete(ref)
                new_ref = ActionScope.from_dict(tmp_ref)
                session.add(new_ref)
            return new_ref.to_dict()

    def del_action_scope(self, intra_extension_id, action_category_id, action_scope_id):
        with sql.transaction() as session:
            query = session.query(ActionScope)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            old_ref = ref.to_dict()
            scope = dict(old_ref["action_scope"])
            if action_category_id not in scope:
                return
            try:
                scope[action_category_id].pop(action_scope_id)
            except KeyError:
                return
            new_ref = ActionScope.from_dict(
                {
                    "id": old_ref["id"],
                    'action_scope': scope,
                    'intra_extension_id': old_ref["intra_extension_id"]
                }
            )
            for attr in ActionScope.attributes:
                if attr != 'id':
                    setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    # Getter and Setter for subject_category_assignment

    def get_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id):
        with sql.transaction() as session:
            query = session.query(SubjectAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id, subject_id=subject_id, subject_category_id=subject_category_id)
            ref = query.first()
            return ref.to_dict()['subject_assignment']

    def set_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id, subject_assignment_list=[]):
        with sql.transaction() as session:
            query = session.query(SubjectAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id, subject_id=subject_id, subject_category_id=subject_category_id)
            ref = query.first()
            new_ref = SubjectAssignment.from_dict(
                {
                    "id": uuid4().hex,
                    'subject_assignment': subject_assignment_list,
                    'intra_extension_id': intra_extension_id,
                    'subject_id': subject_id,
                    'subject_category_id': subject_category_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                for attr in SubjectAssignment.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id)

    def add_subject_assignment_list(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        new_subject_assignment_list = self.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id)
        new_subject_assignment_list.append(subject_scope_id)
        return self.set_subject_assignment_list(intra_extension_id, subject_id, subject_category_id, new_subject_assignment_list)

    def del_subject_assignment(self, intra_extension_id, subject_id, subject_category_id, subject_scope_id):
        new_subject_assignment_list = self.get_subject_assignment_list(intra_extension_id, subject_id, subject_category_id)
        new_subject_assignment_list.pop(subject_scope_id)
        return self.set_subject_assignment_list(intra_extension_id, subject_id, subject_category_id, new_subject_assignment_list)

    # Getter and Setter for object_category_assignment

    def get_object_assignment_list(self, intra_extension_id, object_id, object_category_id):
        """ From a object_uuid, return a dictionary of (category: scope for that object)

        :param intra_extension_id: intra extension UUID
        :param object_id: object UUID
        :return: a dictionary of (keys are category nd values are scope for that object)
        """
        with sql.transaction() as session:
            query = session.query(ObjectAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            _ref = ref.to_dict()
            if object_id in _ref["object_assignment"]:
                _backup_dict = _ref["object_assignment"][object_id]
                _ref["object_assignment"] = dict()
                _ref["object_assignment"][object_id] = _backup_dict
            else:
                _ref["object_assignment"] = dict()
                _ref["object_assignment"][object_id] = dict()
            return _ref

    def set_object_assignment_list(self, intra_extension_id, object_id, object_category_id, object_assignment_list=[]):
        with sql.transaction() as session:
            query = session.query(ObjectAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if type(object_assignment_dict) is not dict:
                raise IntraExtensionError()
            for value in object_assignment_dict.values():
                if type(value) is not list:
                    raise IntraExtensionError(str(value))
            new_ref = ObjectAssignment.from_dict(
                {
                    "id": uuid4().hex,
                    'object_assignment': {object_id: object_assignment_dict},
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                new_ref.object_assignment[object_id] = object_assignment_dict
                for attr in ObjectAssignment.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_object_assignment_list(self, intra_extension_id, object_id, object_category_id, object_scope_id):
        with sql.transaction() as session:
            query = session.query(ObjectAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            assignments = ref.to_dict()['object_assignment']
            if object_id not in assignments:
                assignments[object_id] = dict()
            if object_category_id not in assignments[object_id]:
                assignments[object_id][object_category_id] = list()
            if object_scope_id not in assignments[object_id][object_category_id]:
                assignments[object_id][object_category_id].append(object_scope_id)
            return self.set_object_assignment_list(
                intra_extension_id,
                object_id,
                assignments[object_id])

    def del_object_assignment(self, intra_extension_id, object_id, object_category_id, object_scope_id):
        with sql.transaction() as session:
            query = session.query(ObjectAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            old_ref = ref.to_dict()
            if object_id in old_ref["object_assignment"]:
                if object_category_id in old_ref["object_assignment"][object_id]:
                    old_ref["object_assignment"][object_id][object_category_id].remove(object_scope_id)
                    if not old_ref["object_assignment"][object_id][object_category_id]:
                        old_ref["object_assignment"][object_id].pop(object_category_id)
                    if not old_ref["object_assignment"][object_id]:
                        old_ref["object_assignment"].pop(object_id)
            self.set_object_assignment_list(
                intra_extension_id,
                object_id,
                old_ref["object_assignment"][object_id])

    # Getter and Setter for action_category_assignment

    def get_action_assignment_list(self, intra_extension_id, action_id, action_category_id):
        """ From a action_id, return a dictionary of (category: scope for that action)

        :param intra_extension_id: intra extension UUID
        :param action_id: action UUID
        :return: a dictionary of (keys are category nd values are scope for that action)
        """
        with sql.transaction() as session:
            query = session.query(ActionAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            _ref = ref.to_dict()
            if action_id in _ref["action_assignment"]:
                _backup_dict = _ref["action_assignment"][action_id]
                _ref["action_assignment"] = dict()
                _ref["action_assignment"][action_id] = _backup_dict
            else:
                _ref["action_assignment"] = dict()
                _ref["action_assignment"][action_id] = dict()
            return _ref

    def set_action_assignment_list(self, intra_extension_id, action_id, action_category_id, action_assignment_list=[]):
        with sql.transaction() as session:
            query = session.query(ActionAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if type(action_assignment_dict) is not dict:
                raise IntraExtensionError()
            for value in action_assignment_dict.values():
                if type(value) is not list:
                    raise IntraExtensionError(str(value))
            new_ref = ActionAssignment.from_dict(
                {
                    "id": uuid4().hex,
                    'action_assignment': {action_id: action_assignment_dict},
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
                ref = new_ref
            else:
                new_ref.action_assignment[action_id] = action_assignment_dict
                for attr in ActionAssignment.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return ref.to_dict()

    def add_action_assignment_list(self, intra_extension_id, action_id, action_category_id, action_scope_id):
        with sql.transaction() as session:
            query = session.query(ActionAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            assignments = ref.to_dict()['action_assignment']
            if action_id not in assignments:
                assignments[action_id] = dict()
            if action_category_id not in assignments[action_id]:
                assignments[action_id][action_category_id] = list()
            if action_scope_id not in assignments[action_id][action_category_id]:
                assignments[action_id][action_category_id].append(action_scope_id)
            return self.set_action_assignment_list(
                intra_extension_id,
                action_id,
                assignments[action_id])

    def del_action_assignment(self, intra_extension_id, action_id, action_category_id, action_scope_id):
        with sql.transaction() as session:
            query = session.query(ActionAssignment)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            if not ref:
                raise IntraExtensionUnknown()
            old_ref = ref.to_dict()
            if action_id in old_ref["action_assignment"]:
                if action_category_id in old_ref["action_assignment"][action_id]:
                    old_ref["action_assignment"][action_id][action_category_id].remove(action_scope_id)
                    if not old_ref["action_assignment"][action_id][action_category_id]:
                        old_ref["action_assignment"][action_id].pop(action_category_id)
                    if not old_ref["action_assignment"][action_id]:
                        old_ref["action_assignment"].pop(action_id)
            self.set_action_assignment_list(
                intra_extension_id,
                action_id,
                old_ref["action_assignment"][action_id])

    # Getter and Setter for sub_meta_rule

    def set_aggregation_algorithm(self, intra_extension_id, aggregation_algorithm_id, aggregation_algorithm_dict):
        with sql.transaction() as session:
            query = session.query(AggregationAlgorithm)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            new_ref = AggregationAlgorithm.from_dict(
                {
                    "id": aggregation_algorithm_id,
                    'aggregation_algorithm': aggregation_algorithm_dict,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
            else:
                for attr in AggregationAlgorithm.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_aggregation_algorithm(intra_extension_id)

    def get_aggregation_algorithm(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(AggregationAlgorithm)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            return {ref.to_dict()['id']: ref.to_dict()['aggregation_algorithm']}

    # Getter and Setter for sub_meta_rule

    def get_sub_meta_rules_dict(self, intra_extension_id):
        with sql.transaction() as session:
            query = session.query(SubMetaRule)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict()['sub_meta_rule'] for _ref in ref_list}

    def set_sub_meta_rule_dict(self, intra_extension_id, sub_meta_rule_id, sub_meta_rule_dict):
        with sql.transaction() as session:
            query = session.query(SubMetaRule)
            query = query.filter_by(intra_extension_id=intra_extension_id)
            ref = query.first()
            new_ref = SubMetaRule.from_dict(
                {
                    "id": sub_meta_rule_id,
                    'sub_meta_rule': sub_meta_rule_dict,
                    'intra_extension_id': intra_extension_id
                }
            )
            if not ref:
                session.add(new_ref)
            else:
                for attr in SubMetaRule.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_sub_meta_rules_dict(intra_extension_id)

    def del_sub_meta_rule(self, intra_extension_id, sub_meta_rule_id):
        with sql.transaction() as session:
            query = session.query(SubMetaRule)
            query = query.filter_by(sub_meta_rule_id=sub_meta_rule_id)
            ref = query.first()
            session.delete(ref)

    # Getter and Setter for rules

    def get_rules_dict(self, intra_extension_id, sub_meta_rule_id):
        with sql.transaction() as session:
            query = session.query(Rule)
            query = query.filter_by(intra_extension_id=intra_extension_id, sub_meta_rule_id=sub_meta_rule_id)
            ref_list = query.all()
            return {_ref.id: _ref.to_dict()['rule'] for _ref in ref_list}

    def set_rule_dict(self, intra_extension_id, sub_meta_rule_id, rule_id, rule_list):
        with sql.transaction() as session:
            query = session.query(Rule)
            query = query.filter_by(rule_id=rule_id)
            ref = query.first()
            new_ref = Rule.from_dict(
                {
                    "id": rule_id,
                    'rule': rule_list,
                    'intra_extension_id': intra_extension_id,
                    'sub_meta_rule_id': sub_meta_rule_id
                }
            )
            if not ref:
                session.add(new_ref)
            else:
                for attr in Rule.attributes:
                    if attr != 'id':
                        setattr(ref, attr, getattr(new_ref, attr))
            return self.get_rules_dict(intra_extension_id, sub_meta_rule_id)[rule_id]

    def del_rule(self, intra_extension_id, sub_meta_rule_id, rule_id):
        with sql.transaction() as session:
            query = session.query(Rule)
            query = query.filter_by(rule_id=rule_id)
            ref = query.first()
            session.delete(ref)


# class InterExtension(sql.ModelBase, sql.DictBase):
#     __tablename__ = 'inter_extension'
#     attributes = [
#         'id',
#         'requesting_intra_extension_id',
#         'requested_intra_extension_id',
#         'virtual_entity_uuid',
#         'genre',
#         'description',
#     ]
#     id = sql.Column(sql.String(64), primary_key=True)
#     requesting_intra_extension_id = sql.Column(sql.String(64))
#     requested_intra_extension_id = sql.Column(sql.String(64))
#     virtual_entity_uuid = sql.Column(sql.String(64))
#     genre = sql.Column(sql.String(64))
#     description = sql.Column(sql.Text())
#
#     @classmethod
#     def from_dict(cls, d):
#         """Override parent from_dict() method with a simpler implementation.
#         """
#         new_d = d.copy()
#         return cls(**new_d)
#
#     def to_dict(self):
#         """Override parent to_dict() method with a simpler implementation.
#         """
#         return dict(six.iteritems(self))
#
#
# class InterExtensionConnector(InterExtensionDriver):
#
#     def get_inter_extensions(self):
#         with sql.transaction() as session:
#             query = session.query(InterExtension.id)
#             interextensions = query.all()
#             return [interextension.id for interextension in interextensions]
#
#     def create_inter_extensions(self, inter_id, inter_extension):
#         with sql.transaction() as session:
#             ie_ref = InterExtension.from_dict(inter_extension)
#             session.add(ie_ref)
#         return InterExtension.to_dict(ie_ref)
#
#     def get_inter_extension(self, uuid):
#         with sql.transaction() as session:
#             query = session.query(InterExtension)
#             query = query.filter_by(id=uuid)
#             ref = query.first()
#             if not ref:
#                 raise exception.NotFound
#             return ref.to_dict()
#
#     def delete_inter_extensions(self, inter_extension_id):
#         with sql.transaction() as session:
#             ref = session.query(InterExtension).get(inter_extension_id)
#             session.delete(ref)

