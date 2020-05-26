class DoesNotExist(Exception):
	pass

class MultipleObjectsReturned(Exception):
	pass

class InvalidField(Exception):
	pass

def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor()
	crsr.execute("PRAGMA foreign_keys=on;")
	crsr.execute(sql_query)
	connection.commit()
	connection.close()
	

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query)
	ans= crsr.fetchall()
	connection.close()
	return ans
	

class Student:
    
    def __init__(self, name, age, score):
        self.name = name
        self.student_id = None
        self.age = age
        self.score = score
    
    def __repr__(self):
        return "Student(student_id={0}, name={1}, age={2}, score={3})".format(
            self.student_id,
            self.name,
            self.age,
            self.score)
            
    def save(self):
        if self.student_id is None:
            query="insert into student(name,age,score) values ('{}',{},{})".format(self.name,self.age,self.score)
            write_data(query)
            q1='select student_id from student where name="{}" and age={} and score={}'.format(self.name,self.age,self.score)
            a=read_data(q1)   
            self.student_id=a[0][0]
        else:
            sql_query="update student set student_id={},name='{}',age={},score={} where student_id={}".format(self.student_id,self.name,self.age,self.score,self.b)
            write_data(sql_query)
            
    def delete(self):
        sql_query='delete from student where student_id={}'.format(self.student_id)
        write_data(sql_query)
    
	
    @classmethod
    def get(cls,**kwarg):
        for x,y in kwarg.items():
            
            cls.a=x
            cls.b=y
            
            if str(x) not in ('name','age','score','student_id'):
                raise InvalidField
           
        query="select * from student where {} = '{}'".format(cls.a,cls.b)
        
        obj=read_data(query)
        
        if len(obj)>1:
            raise MultipleObjectsReturned
            
        elif len(obj)==0:
            raise DoesNotExist
            
        elif len(obj)==1:
            c=Student(obj[0][1],obj[0][2],obj[0][3])
            c.student_id=obj[0][0]
            return c
		
    @classmethod
    def filter(cls,**kwargs):
        objects_list=[]
        operator={'lt' : '<', 'lte' : '<=', 'gt' : '>', 'gte' : '>=', 'neq' : '!=', 'in' : 'in'}
        
        for key, value in kwargs.items():
                    
            keys = key
            value=value
            keys = keys.split('__')
            if keys[0] not in ('name', 'age', 'score', 'student_id'):
                raise InvalidField 
            
            if len(keys) == 1:
                sql_query= f" {key} = '{value}'"
                    
            elif keys[1] == 'in':
                sql_query = f"{keys[0]} {operator[keys[1]]} {tuple(value)}"
                    
            elif keys[1] == 'contains':
                sql_query = f"{keys[0]} like '%{value}%'"
                    
            else:    
                sql_query = f"{keys[0]} {operator[keys[1]]} '{value}'"
                
            objects_list.append(sql_query)
                    
        mul_conditions = " and ".join(objects_list)      
        sql_query = " " + mul_conditions
            
        return sql_query
        
    @classmethod
    def avg(cls,field,**kwargs):
        if field not in ('student_id','name','age','score'):
            raise InvalidField
        else:
            if len(kwargs)==0:
                sql_query="select avg({}) from Student".format(field)
                r=read_data(sql_query)
            else:
                query=Student.filter(**kwargs)
                sql_query="select avg({}) from Student where {}".format(field,query)
                r=read_data(sql_query)
        return r[0][0]
        
    @classmethod
    def min(cls,field,**kwargs):
        if field not in ('student_id','name','age','score'):
            raise InvalidField
        else:
            if len(kwargs)==0:
                sql_query="select min({}) from Student".format(field)
                r=read_data(sql_query)
            else:
                query=Student.filter(**kwargs)
                sql_query="select min({}) from Student where {}".format(field,query)
                r=read_data(sql_query)
        return r[0][0]
        
    @classmethod
    def max(cls,field,**kwargs):
        if field not in ('student_id','name','age','score'):
            raise InvalidField
        else:
            if len(kwargs)==0:
                sql_query="select max({}) from Student".format(field)
                r=read_data(sql_query)
            else:
                query=Student.filter(**kwargs)
                sql_query="select max({}) from Student where {}".format(field,query)
                r=read_data(sql_query)
        return r[0][0]
    
    @classmethod
    def count(cls,field=None,**kwargs):
        if field==None:
            sql_query="select count(*) from student"
        elif field not in ('student_id','name','age','score'):
            raise InvalidField
        elif len(kwargs)==0:
                sql_query="select count({}) from Student".format(field)
        else:
                query=Student.filter(**kwargs)
                sql_query="select count({}) from Student where {}".format(field,query)
        r=read_data(sql_query)
        return r[0][0]
        
    @classmethod
    def sum(cls,field,**kwargs):
        if field not in ('student_id','name','age','score'):
            raise InvalidField
        else:
            if len(kwargs)==0:
                sql_query="select sum({}) from Student".format(field)
                r=read_data(sql_query)
            else:
                query=Student.filter(**kwargs)
                sql_query="select sum({}) from Student where {}".format(field,query)
                r=read_data(sql_query)
        return r[0][0]
    
#count = Student.avg('age', score__gt=30, age__lt=30)
#print(count)
