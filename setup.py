from setuptools import setup

setup(
   name='api',
   version='1.0',
   description='Basic API',
   author='BenTStark',
   author_email='',
   packages=['api'], 
   install_requires=[
     # 'flask_swagger_ui'
    #  , 'flask_restful_swagger'
     # , 'flask-mysql'
       'flask-cors' #, 'flask_restful'
      , 'flask-restx'
      , 'psycopg2'
      ,'werkzeug'
      ,'pyyaml']
)
