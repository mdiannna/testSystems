from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, PasswordField, SubmitField


class testForm(Form):
	first_sys_name = TextField('First system name:')
	first_sys_param = TextField('Console parameters:')
	second_sys_name = TextField('Second system name:')
	second_sys_param = TextField('Console parameters:')
	nr_tests = IntegerField('Nr. of tests:')
	submit = SubmitField('Show results')
