#!/usr/bin/env python


# Copyright 2015 Open Platform for NFV Project, Inc. and its contributors
# This software is distributed under the terms and conditions of the 'Apache-2.0'
# license which can be found in the file 'LICENSE' in this package distribution
# or at 'http://www.apache.org/licenses/LICENSE-2.0'.

PROJECT = 'python-moonclient'

# Change docs/sphinx/conf.py too!
VERSION = '0.1'

from setuptools import setup, find_packages

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='Python Moon client',
    long_description=long_description,

    author='Thomas Duval',
    author_email='thomas.duval@orange.com',

    url='https://github.com/...',
    download_url='https://github.com/.../tarball/master',

    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: Apache Software License',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.2',
                 'Intended Audience :: Developers',
                 'Environment :: Console',
                 ],

    platforms=['Any'],

    scripts=[],

    provides=[],
    install_requires=['cliff'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'moon = moonclient.shell:main'
        ],
        'moon.client': [
            'policy_list = moonclient.authz_policy:AuthzPolicies',
            'intraextension_tenant_set = moonclient.intraextension:TenantSet',
            'intraextension_create = moonclient.intraextension:IntraExtensionCreate',
            'intraextension_list = moonclient.intraextension:IntraExtensionList',
            'intraextension_delete = moonclient.intraextension:IntraExtensionDelete',
            'intraextension_show = moonclient.intraextension:IntraExtensionShow',
            'subject_list = moonclient.subjects:SubjectsList',
            'subject_add = moonclient.subjects:SubjectsAdd',
            'subject_delete = moonclient.subjects:SubjectsDelete',
            'object_list = moonclient.objects:ObjectsList',
            'object_add = moonclient.objects:ObjectsAdd',
            'object_delete = moonclient.objects:ObjectsDelete',
            'action_list = moonclient.actions:ActionsList',
            'action_add = moonclient.actions:ActionsAdd',
            'action_delete = moonclient.actions:ActionsDelete',
            'action_assignment_list = moonclient.action_assignments:ActionAssignmentsList',
            'action_assignment_add = moonclient.action_assignments:ActionAssignmentsAdd',
            'action_assignment_delete = moonclient.action_assignments:ActionAssignmentsDelete',
            'object_assignment_list = moonclient.object_assignments:ObjectAssignmentsList',
            'object_assignment_add = moonclient.object_assignments:ObjectAssignmentsAdd',
            'object_assignment_delete = moonclient.object_assignments:ObjectAssignmentsDelete',
            'subject_assignment_list = moonclient.subject_assignments:SubjectAssignmentsList',
            'subject_assignment_add = moonclient.subject_assignments:SubjectAssignmentsAdd',
            'subject_assignment_delete = moonclient.subject_assignments:SubjectAssignmentsDelete',
            'subject_category_list = moonclient.subject_categories:SubjectCategoriesList',
            'subject_category_add = moonclient.subject_categories:SubjectCategoriesAdd',
            'subject_category_delete = moonclient.subject_categories:SubjectCategoriesDelete',
            'object_category_list = moonclient.object_categories:ObjectCategoriesList',
            'object_category_add = moonclient.object_categories:ObjectCategoriesAdd',
            'object_category_delete = moonclient.object_categories:ObjectCategoriesDelete',
            'action_category_list = moonclient.action_categories:ActionCategoriesList',
            'action_category_add = moonclient.action_categories:ActionCategoriesAdd',
            'action_category_delete = moonclient.action_categories:ActionCategoriesDelete',
            'subject_category_scope_list = moonclient.subject_category_scope:SubjectCategoryScopeList',
            'subject_category_scope_add = moonclient.subject_category_scope:SubjectCategoryScopeAdd',
            'subject_category_scope_delete = moonclient.subject_category_scope:SubjectCategoryScopeDelete',
            'object_category_scope_list = moonclient.object_category_scope:ObjectCategoryScopeList',
            'object_category_scope_add = moonclient.object_category_scope:ObjectCategoryScopeAdd',
            'object_category_scope_delete = moonclient.object_category_scope:ObjectCategoryScopeDelete',
            'action_category_scope_list = moonclient.action_category_scope:ActionCategoryScopeList',
            'action_category_scope_add = moonclient.action_category_scope:ActionCategoryScopeAdd',
            'action_category_scope_delete = moonclient.action_category_scope:ActionCategoryScopeDelete',
            'aggregation_algorithm_list = moonclient.metarules:AggregationAlgorithmsList',
            'aggregation_algorithm_show = moonclient.metarules:AggregationAlgorithmShow',
            'aggregation_algorithm_set = moonclient.metarules:AggregationAlgorithmSet',
            'submetarule_show = moonclient.metarules:SubMetaRuleShow',
            'submetarule_set = moonclient.metarules:SubMetaRuleSet',
            'submetarule_relation_list = moonclient.metarules:SubMetaRuleRelationList',
            'rule_list = moonclient.rules:RulesList',
            'rule_add = moonclient.rules:RuleAdd',
            'rule_delete = moonclient.rules:RuleDelete',
            'log = moonclient.logs:LogsList',
        ],
    },

    zip_safe=False,
)