from flask import Flask, jsonify , request, json
from flask import Response
import requests 
  
app = Flask(__name__)

        
@app.route('/')
def index():
    return jsonify({
       'author': 'Ajay Gurav',
       'author_url': 'http://ajaygurav.online',
      
       
   })


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
  
@app.route('/gettop3repos',methods=["POST"])
def gettop3repos():
    
    ## validate Content Type
    if request.headers['Content-Type'] == 'application/json':
        ## value Key error 
        if not request.json or not 'org' in request.json:
            err=[{"Key Error":'Org Name cannot be empty'}]
            j1=json.dumps(err)
            
            resp = Response(j1, status=400, mimetype='application/json')
            return resp
            
        else:



            org_name=request.json['org']

            # api-endpoint 
            URL = "https://api.github.com/orgs/"+org_name+"/repos"

            # toek for authentication given here 
            location = "ee1aef4353ecb4de5535262e9b46b91c7f86f4d0"

            # defining a params dict for the parameters to be sent to the API 
            PARAMS = {'token':location} 

            # sending get request and saving the response as response object 
            r = requests.get(url = URL, params = PARAMS) 

            # extracting data in json format 
            data = r.json() 
            # create dictionary with name as key and star count as value 
            d1={}

            for i in range(len(data)):
                s1=data[i]['full_name']
                s1=s1.split("/")
                s1=s1[1]
                d1[s1]=data[i]['stargazers_count']

            # sorting dictionary based on star count 
            if len(d1)>3:
                ## if length is greater than 3 return top 3 repos
                toplist=dict(sorted(d1.items(),key=lambda x:x[1],reverse=True)[:3])
            else:
                ## else return all repos 
                toplist=dict(sorted(d1.items(),key=lambda x:x[1],reverse=True)[:3])

            j1=json.dumps(toplist)
            result_l1=[]
            for key,val in toplist.items():
                tm={}
                tm['name']=key
                tm['stars']=val
                result_l1.append(tm)
            response_op={}
            response_op['results']=result_l1
            j2=json.dumps(response_op)
            

            resp = Response(j2, status=200, mimetype='application/json')
            return resp

    else:
        return "415 Unsupported Media Type ;)"
