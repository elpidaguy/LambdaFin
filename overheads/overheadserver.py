from flask import Flask,render_template,request,redirect,session,jsonify,send_from_directory
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_uploads import UploadSet, configure_uploads
import requests,time
from bson.objectid import ObjectId
from datetime import datetime
from datetime import date
import pandas as pd
from datetime import timedelta

from pandas import ExcelWriter

app = Flask("__name__")
CORS(app)
app.config["MONGO_DBNAME"] = "mouseclicksys"
mongo = PyMongo(app)

@app.route("/saveSheet",methods=["POST"])
def saveSheet():
	schema={}
	schema["ucc"]=request.get_json()["ucc"]["UCC"]
	schema["uccid"]=request.get_json()["ucc"]["_id"]
	schema["sheetName"]=request.get_json()["sheetName"]
	schema["department"]=request.get_json()["department"]
	schema["NoOfDepartments"]=request.get_json()["NoOfDepartments"]
	#print(schema)
	dd=mongo.db.overheadschema.insert(schema)
	dd=str(dd)
	#print dd
	#dd="5b699cd2e657f41b9a7faab9"
	createdata(dd)

	#sheet=mongo.db.overheadschema.find({'uccid':request.get_json()["ucc"]["_id"],"ucc"})
	return jsonify({"success":"true","message":"Schema Created Successfully"})


@app.route("/getSheetByUcc",methods=["POST"])
def getSheetByUcc():
	sheets=mongo.db.overheadschema.find({'uccid':request.get_json()["id"]})
	sheets=list(sheets)
	for s in sheets:
		s["_id"]=str(s["_id"])

	if len(sheets):
		return jsonify({"success":"true","Sheets":sheets})
	else:
		return jsonify({"success":"false","message":"No Sheets Present"})

@app.route("/saveEditedSheet",methods=["POST"])
def saveEditedSheet():
	print request.get_json()
	idd=request.get_json()["_id"]
	mongo.db.overheadschema.update_one({"_id":ObjectId(idd)} ,{"$set":{"NoOfDepartments":request.get_json()["NoOfDepartments"],"department":request.get_json()["department"]}},upsert=False)

	return jsonify({"success":"true","message":"Sheet updated Successfully"})

@app.route("/saveCalculatedSheet",methods=["POST"])
def saveCalculatedSheet():
	print request.get_json()
	idd=request.get_json()["sheetData"][0]["_id"]
	print(idd)
	mongo.db.overheaddata.update_one({"_id":ObjectId(idd)} ,{"$set":{"department":request.get_json()["sheetData"][0]["department"]}},upsert=False)

	return jsonify({"success":"true","message":"Sheet updated Successfully"})


def createdata(idd):
	sheets=mongo.db.overheadschema.find({'_id':ObjectId(idd)})
	sheets=list(sheets)
	for s in sheets:
		s["_id"]=str(s["_id"])
	d=[]
	date=datetime.now()
	ddate=date.strftime('%b-%Y')
	newmonth={}
	newmonth["id"]=idd
	newmonth["month"]=ddate
	temp=date.strftime('1-%b-%Y')
	startdate=datetime.strptime(temp, '1-%b-%Y').date()
 	curdate=startdate
 	pmonth=curdate.strftime('%b')
 	while(pmonth==curdate.strftime('%b')):
 		d.append(curdate.strftime('%d'))
 		curdate=curdate + timedelta(days=1)
 	newmonth["date"]=d
 	departments=[]
 	for dept in sheets[0]["department"]:
 		dd={}
 		dd["departName"]=dept["departName"]
 		coll=[]
 		for col in dept["col"]:
 			temp={}
 			temp["colName"]=col["colName"]
 			nn=[]
 			for date in d:
 				nn.append("")
 			temp["data"]=nn
 		
 			coll.append(temp)
 		dd["col"]=coll
 		departments.append(dd)
 	newmonth["department"]=departments
 	mongo.db.overheaddata.insert(newmonth)

	
	return jsonify({"success":"true","message":"msg From Server !"})


@app.route("/test",methods=["POST"])
def test():
	a="3"
	b="4"
	a=int(a)
	b=int(b)
	print(eval("((a+b)*a)-(a-b)"))
	return jsonify({"success":"true","message":"msg From Server !"})

@app.route("/createNewSheet",methods=["POST"])
def createNewSheet():
	idd=request.get_json()["id"];
	date=request.get_json()["month"];
	date = datetime.strptime(date, '%m-%Y')
	#print d
	# print request.get_json()
	sheets=mongo.db.overheadschema.find({'_id':ObjectId(idd)})
	sheets=list(sheets)
	for s in sheets:
		s["_id"]=str(s["_id"])
	d=[]
	#date=datetime.now()
	ddate=date.strftime('%b-%Y')
	newmonth={}
	newmonth["id"]=idd
	newmonth["month"]=ddate
	temp=date.strftime('1-%b-%Y')
	startdate=datetime.strptime(temp, '1-%b-%Y').date()
 	curdate=startdate
 	pmonth=curdate.strftime('%b')
 	while(pmonth==curdate.strftime('%b')):
 		d.append(curdate.strftime('%d'))
 		curdate=curdate + timedelta(days=1)
 	newmonth["date"]=d
 	departments=[]
 	for dept in sheets[0]["department"]:
 		dd={}
 		dd["departName"]=dept["departName"]
 		coll=[]
 		for col in dept["col"]:
 			temp={}
 			temp["colName"]=col["colName"]
 			if(col["isCarryForward"]==True):
 				temp["opening"]=""
 			nn=[]
 			for date in d:
 				nn.append("")
 			temp["data"]=nn
 		
 			coll.append(temp)
 		dd["col"]=coll
 		departments.append(dd)
 	newmonth["department"]=departments
 	mongo.db.overheaddata.insert(newmonth)
	# a="3"
	# b="4"
	# a=int(a)
	# b=int(b)
	# print(eval("((a+b)*a)-(a-b)"))
	return jsonify({"success":"true","message":"msg From Server !"})

@app.route("/getSheetDataById",methods=["POST"])
def getSheetDataById():
	idd=request.get_json()["id"]
	print idd
	sheetdata=mongo.db.overheaddata.find({'id':idd})
	sheetdata=list(sheetdata)
	for s in sheetdata:
		s["_id"]=str(s["_id"])
	print sheetdata
	return jsonify({"success":"true","sheetdata":sheetdata})
	# if len(sheetdata):
	# 	return jsonify({"success":"true","sheetdata":sheetdata})
	# else:
	# 	return jsonify({"success":"false","sheetdata":[]})




if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=2840, threaded=True)