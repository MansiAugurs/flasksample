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
        query_params =request.args.to_dict()
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
@app.route('/newusers', methods=['GET'])
def get_newusers():
    
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
        data = request.get_json()
        fname=data.get('fname')
        lname=data.get('lname')
        personid=data.get('personid')
        cursor.execute("INSERT into personsdemo (fname, lname, personid) VALUES (?, ?, ?)", (fname, lname, personid))
        cnxn.commit()
        return jsonify({"message": "user added successfully"})
    except Exception as e:
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

