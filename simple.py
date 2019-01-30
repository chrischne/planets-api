from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}

class AstroData(Resource):
    def get(self,_day,_month,_year,_hour,_minute):
        return { 'day': _day,
                  'month': _month,
                  'year': _year,
                  'hour': _hour,
                  'minute': _minute
                }
    
class TodoSimple(Resource):
    def get(self,todo_id):
        return {todo_id: todos[todo_id]}
    
    def put(self,todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}
        
    
api.add_resource(AstroData,'/<int:_day>/<int:_month>/<int:_year>/<int:_hour>/<int:_minute>')

if __name__ == '__main__':
    app.run(debug=True)
