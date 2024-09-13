from flask import Flask, jsonify, request
from db import get_db_connection
import pyodbc


#from flask_restful import 
app= Flask(__name__)



#its better to have models for this and then import it but we are declaring it globally as of now to use it in the program
cnxn = get_db_connection()         #connection is established
cursor = cnxn.cursor()             #cursor for database is created




def insert_db_connection(fname, lname, id):
        """
        Creates a new DB connection with the provided details.
        """
        # cnxn = get_db_connection()
        # cursor = cnxn.cursor()

        cursor.execute(
            "INSERT INTO [db] (fname, lname, id ) "
            "VALUES (?, ?, ?)",
            (fname, lname, id)
        )
        cnxn.commit()
        # cursor.close()
        # cnxn.close()


#get method to gEt all th data of the table
@app.route('/users', methods=['GET'])
def get_users():
    #this query is used to display all data from table
    try:

        cursor.execute("SELECT * from personsdemo")
        data = cursor.fetchall()
        print(data)
        #we need the data in dictionary format therefor mapping the data into dictionary format
        json_data = []
        for ele in data:
            #firstname is at index 0, lastmae is at index1 and so on
            json_data.append( { "First_name":ele[0] , "Last_Name":ele[1] , "Person_ID":ele[2] } )
        #this function is used for POSTMAN
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'message':"some error has occured"}), 500


#function to update users from existing table
@app.route('/usersUpdate', methods=['PATCH'])
def update_user():
    try:
        #adding validations
        query_params =request.args.to_dict()
       
     
        #adding validation to check if person name is blank
        if query_params.get('person_name') == None  or len(query_params.get('person_name')) == 0:
            return jsonify({ "message":"person_name is missing " }) , 400
        
        #adding validation to check if person id is blank
        if query_params.get('person_id') == None  or len(query_params.get('person_id')) == 0:
            return jsonify({ "message":"person_id is missing " }) , 400
        
        #adding validation to check we are updating user and its  personid is present or not
        cursor.execute(f"SELECT * from personsdemo WHERE personid={query_params.get('person_id')} ")
        data = len(cursor.fetchall())
        print(data)
        
        if data==0:
            return jsonify({"message":"user does not exist"}),400
            
       
        



        # print( f" UPDATE  personsdemo SET fname='{query_params['person_name']}' WHERE personid={query_params['person_id']}")
        cursor.execute(
             f" UPDATE  personsdemo SET lname='{query_params['person_name']}' WHERE personid={query_params['person_id']}"
         )
        cnxn.commit()
     # cursor.close()
     # cnxn.close()


        return jsonify({ "message":"User Updated" })
    except Exception as e:
        return jsonify({'message':"No user is updated"}), 500            

#this endpoint is used to search users on specific condition
# @app.route('/newusers', methods=['GET'])
# def get_newusers():
    
    try:
        cursor.execute("SELECT * from personsdemo WHERE fname LIKE '%AHAD'")
        data = cursor.fetchall()
        print(data)
        #we need the data in dictionary format therefor mapping the data into dictionary format
        json_data = []
        for ele in data:
            #firstname is at index 0, lastmae is at index1 and so on
            json_data.append( { "First_name":ele[0] , "Last_Name":ele[1] , "Person_ID":ele[2] } )
        #this function is used for POSTMAN
        return jsonify(json_data)
    except Exception as e:
        return jsonify({'message':"some error has occured"}), 500
    

#api to delete users from existing table
@app.route('/delusers', methods=['DELETE'])
def deleteusers():
    try:
        query_params =request.args.to_dict()
       
     
        #adding validation to check if person name is blank
        if query_params.get('person_name') == None  or len(query_params.get('person_name')) == 0:
            return jsonify({ "message":"person_name is missing " }) , 400
        
        #adding validation to check if person id is blank or 0
        if query_params.get('person_id') == None  or len(query_params.get('person_id')) == 0:
            return jsonify({ "message":"person_id is missing " }) , 400
        
        query_params =request.args.to_dict()

        query1= cursor.execute(f"SELECT * from personsdemo WHERE personid='{query_params.get('person_id')}'")
        #to fetch the data of the requested query
        data1= query1.fetchall()
        

        if len(data1) ==0:
            return jsonify({"message":"user already deleted"})
            
        sql_query = f"DELETE FROM personsdemo WHERE personid={query_params['person_id']}"
        print(sql_query)
        cursor.execute(sql_query)
        cnxn.commit()
        return jsonify({ "message":"Record Deleted" })
    except Exception as e:
        print(e)
        return jsonify({'message':"some error has occured"}), 500
    



#api to insert data into the existing table
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        #in POST method we get data from body and not by param string
        data = request.get_json()
        fname=data.get('fname')
        lname=data.get('lname')
        personid=data.get('personid')

         #adding validation to check if person fname and lname is not even sent
        if fname == None  or lname == None:
            return jsonify({ "message":"person first or last name is missing " }) , 400
        
         #adding validation to check if person fname and lname is blank value
        if fname == ""  or lname == "" or personid== 0:
            return jsonify({ "message":"person first or last name is invalid value" }) , 400

        #query to see the fname, lname, personid we are getting by body above  is present in the table or not
        query1= cursor.execute(f"SELECT * from personsdemo WHERE (fname='{fname}' and lname='{lname}') or personid='{personid}'")
        print(f"SELECT * from personsdemo WHERE fname='{fname}' and lname='{lname}' and personid='{personid}'")
       
        #to fetch the data of the requested query
        data1= query1.fetchall()

        print(data1)

       

        #adding validation by checking if the length of the data receive is  greater than 0, if true then printing the desired result
        if len(data1) >0:
            return jsonify({ "message":"person already exist with same first and last name and personid" }) , 400
        
        #query to insert data into the table
        cursor.execute("INSERT into personsdemo (fname, lname, personid) VALUES (?, ?, ?)", (fname, lname, personid))
        cnxn.commit()
        return jsonify({"message": "user added successfully"})

    except Exception as e:
        print(e)
        return jsonify({"message":"no user is added"})

    




    
    

@app.route('/')
def hello():
    return jsonify({ "message":"Hello World Masni" })

@app.route('/sample_post' , methods=['POST'])
def sample_post():
    body = request.get_json()

    print(body.get('name'))
    print(body.get('designation'))
    return jsonify({ "message":"Data Accepted" })

if __name__=='__main__':
    app.run(debug= True)

