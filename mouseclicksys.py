# import datetime
from flask import Flask,render_template,request,redirect,session,jsonify,send_from_directory
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from flask_uploads import UploadSet, configure_uploads
import requests,time
from bson.objectid import ObjectId
from datetime import datetime
from datetime import date
import pandas as pd
from pandas import ExcelWriter

app = Flask("__name__")
CORS(app)
app.config["MONGO_DBNAME"] = "mouseclicksys"
mongo = PyMongo(app)

@app.route("/uploadclientlist", methods=["POST"])
def uploadclientlist():
	filename =""
	target="/opt/lampp/htdocs/mouseclicksys/uploads/clientlist"
	
	for upload in request.files.getlist("file"):
		filename = upload.filename
		destination = "/".join([target, filename])

		upload.save(destination)
		df = pd.read_excel(destination, sheet_name='ClientList')
		for i in df.index:
			clientlist = mongo.db.clientlist.find_one({"UCC":df['UCC'][i]})
			# print clientlist
			if clientlist!=None:
				# mongo.db.clientlist.update_one({"_id":ObjectId(clientlist['_id'])} ,{"$set":{"NAV":df['NAV'][i]}},upsert=False)
				print("already present")
			else:
				print str(df['ClientName'][i])
				if str(df['ClientName'][i]) == 'nan':
					df['ClientName'][i] = ""
				
				if str(df['Family'][i]) == 'nan':
					df['Family'][i] = ""
				
				if str(df['UCC'][i]) == 'nan':
					df['UCC'][i] = ""
				
				if str(df['Bank1'][i]) == 'nan':
					df['Bank1'][i] = ""
				
				if str(df['AccountNo'][i]) == 'nan':
					AccountNo = ""
				else:
					AccountNo = str(int(float(df['AccountNo'][i])))

				if str(df['AccountNo2'][i]) == 'nan':
					AccountNo2 = ""
				else:
					AccountNo2 = str(int(float(df['AccountNo2'][i])))
					print AccountNo2

				if str(df['AccountNo3'][i]) == 'nan':
					AccountNo3 = ""
				else:
					AccountNo3 = str(int(float(df['AccountNo3'][i])))
				
				if str(df['Bank2'][i]) == 'nan':
					df['Bank2'][i] = ""
				
				if str(df['Bank3'][i]) == 'nan':
					df['Bank3'][i] = ""
				
				mongo.db.clientlist.insert({"ClientName":str(df['ClientName'][i]),"Family":str(df['Family'][i]),"UCC":str(df['UCC'][i]),"Bank1":str(df['Bank1'][i]),"Acc1":AccountNo,"Bank2":str(df['Bank2'][i]),"Acc2":AccountNo2,"Bank3":str(df['Bank3'][i]),"Acc3":AccountNo3,"familyhead":False})
				
	return jsonify({"success":"true","message":"Successfully Uploaded"})


@app.route("/uploadchequinexcel", methods=["POST"])
def uploadchequinexcel():
	filename =""
	target="/opt/lampp/htdocs/mouseclicksys/uploads/chequin"
	
	for upload in request.files.getlist("file"):
		filename = upload.filename
		destination = "/".join([target, filename])

		upload.save(destination)
		df = pd.read_excel(destination, sheet_name='ChqIn')	
		# df = df.astype(float).sum().astype(int).astype(str)
		# print("Column headings:")
		# print(df.columns)
		for i in df.index:
			ifexists = mongo.db.chqueIn.find_one({"ChqNo":df['ChqNo'][i],"UCC":df['UCC'][i]})
			# print ifexists
			if ifexists==None:
				# chqno = str(df['ChqNo'][i]).replace(':','')
				# print chqno
				
				if str(df['Bank'][i]) == 'nan':
					df['Bank'][i] = ""
				
				if str(df['ChqNo'][i]) == 'nan':
					chqno = ""
				else:
					chqno = str(df['ChqNo'][i]).replace(':','')

				if str(df['Comments'][i]) == 'nan':
					df['Comments'][i] = ""

				if str(df['Amount'][i]) == 'nan':
					df['Amount'][i] = ""

				if str(df['DepositedDate'][i]) == 'NaT' or str(df['DepositedDate'][i]) == 'nan' :
					depositeddate = ""
					# df['DepositedDate'][i] = ""
				else:
					depositeddate = df['DepositedDate'][i].strftime('%d-%b-%y')					

				if str(df['Slip'][i]) == 'nan':
					slip = ""
				else:
					slip = str(int(float(df['Slip'][i])))

				if str(df['AccountNo'][i]) != 'WRONG ORDERS':
					# accno = mongo.db.clientlist.find_one({"UCC":str(df['UCC'][i]),"$or":[{"Bank1":str(df['Bank'][i])},{"Bank2":str(df['Bank'][i])},{"Bank3":str(df['Bank'][i])}]},{"Acc1":True,"Acc2":True,"Acc3":True,"_id":False})
					accexists = mongo.db.clientlist.find_one({"UCC":str(df['UCC'][i]),"Bank1":str(df['Bank'][i])},{"Acc1":True,"_id":False})
					if accexists:
						# print accexists
						accno = accexists['Acc1']
					else:
						accexists2 = mongo.db.clientlist.find_one({"UCC":str(df['UCC'][i]),"Bank2":str(df['Bank'][i])},{"Acc2":True,"_id":False})
						if accexists2:
							# print accexists2
							accno = accexists2['Acc2']
						else:
							accexists3 = mongo.db.clientlist.find_one({"UCC":str(df['UCC'][i]),"Bank3":str(df['Bank'][i])},{"Acc3":True,"_id":False})
							if accexists3:
								# print accexists3
								accno = accexists3['Acc3']
				else:
					accno = str(df['AccountNo'][i])

				# mongo.db.amcs.update_one({"_id":ObjectId(amc['_id'])} ,{"$set":{"NAV":df['NAV'][i]}},upsert=False)
				# print ({"Bank":str(df['Bank'][i]),"UCC":str(df['UCC'][i]),"AccountNo":accno,"Family":str(df['Family'][i]),"ChqNo":chqno,"Amount":str(df['Amount'][i]),"DepositedDate":str(depositeddate),"Slip":slip,"Comments":str(df['Comments'][i])})
				if str(df['UCC'][i]) != 'nan':
					mongo.db.chqueIn.insert({"Bank":str(df['Bank'][i]),"UCC":str(df['UCC'][i]),"AccountNo":accno,"Family":str(df['Family'][i]),"ChqNo":chqno,"Amount":str(df['Amount'][i]),"DepositedDate":str(depositeddate),"Slip":slip,"Comments":str(df['Comments'][i]),"preas":False,"finas":True,"dishon":False})
				print("not present insert")
			else:
				print("already present")
				# mongo.db.chqueIn.insert({"Bank":str(df['Bank'][i]),"UCC":str(df['UCC'][i]),"AccountNo":str(df['AccountNo'][i]),"Family":str(df['Family'][i]),"ChqNo":str(df['ChqNo'][i]),"Amount":str(df['Amount'][i]),"DepositedDate":str(df['DepositedDate'][i]),"TotalSum":str(df['TotalSum'][i]),"Slip":str(df['Slip'][i]),"Comments":str(df['Comments'][i])})
				# print("not present insert")
	return jsonify({"success":"true","message":"Successfully Uploaded"})



@app.route("/uploadsofile", methods=['POST'])
def uploadsofile():
	filename =""
	target="/opt/lampp/htdocs/mouseclicksys/uploads/switchout"
	
	for upload in request.files.getlist("file"):
		filename = upload.filename
		destination = "/".join([target, filename])

		upload.save(destination)
		df = pd.read_excel(destination, sheet_name='Sheet1')	
		for i in df.index:
			pnl = 0
			if str(df['Comments'][i]) == 'nan':
				# df['Comments'][i] = ""
				com = ""
			else:
				com = str(df['Comments'][i])

			schemecode = str(df['SchemeCode'][i]).replace(':','')
			soschemecode = str(df['SOSchemeCode'][i]).replace(':','')
			
			if str(df['SINO'][i]) != 'nan' and str(df['SONO'][i]) != 'nan':
				# print {"Units":str(df['Units'][i]),"SwitchDate":str(df['SwitchDate'][i]),"SOSchemeCode":str(soschemecode),"SOSchemeName":str(df['SOSchemeName'][i]),"SOFolio":str(df['SOFolio'][i]),"SOCategory":str(df['SOCategory'][i]),"SOAmount":str(df['SOAmount'][i]),"OrderNo":str(df['OrderNo'][i]),"NAV":str(df['NAV'][i]),"Folio":str(df['Folio'][i]),"Family":str(df['Family'][i]),"AMC":str(df['AMC'][i]),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i]),"Date":str(df['Date'][i])}
				ifexists = mongo.db.switchout.find_one({"Units":str(df['Units'][i]),"SwitchDate":str(df['SwitchDate'][i]),"SOSchemeCode":str(soschemecode),"SOSchemeName":str(df['SOSchemeName'][i]),"SOFolio":str(df['SOFolio'][i]),"SOCategory":str(df['SOCategory'][i]),"SOAmount":str(df['SOAmount'][i]),"OrderNo":str(df['OrderNo'][i]),"NAV":str(df['NAV'][i]),"Folio":str(df['Folio'][i]),"Family":str(df['Family'][i]),"AMC":str(df['AMC'][i]),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i]),"Date":str(df['Date'][i])})
				if ifexists == None:
					# print ifexists
					print "no match yet"
				else:
					# print ifexists
					mongo.db.switchout.update_one({'_id':ifexists['_id']},{"$set":{"SONO":str(df['SONO'][i]),"SINO":str(df['SINO'][i])}},upsert=False)
					mongo.db.today.insert({'BuyDate':str(df['SwitchDate'][i]),'Category':str(df['SOCategory'][i]),'ChqNo':'Switch','Folio':str(df['SOFolio'][i]),'Amount':str(df['SOAmount'][i]),'SchemeName':str(df['SchemeName'][i]),'SchemeCode':str(df['SchemeCode'][i]),'Family':str(df['Family'][i]),'AMC':str(df['AMC'][i]),'UCC':str(df['UCC'][i]),'OrderNo':str(df['SINO'][i]),'dep':'b'})

				ifexists2 = mongo.db.residue.find_one({'OrderNo':str(df['OrderNo'][i])})
				if ifexists2 == None:
					mongo.db.residue.insert({'SONO':str(df['SONO'][i]),'Family':str(df['Family'][i]),'UCC':str(df['UCC'][i]),'AMC':str(df['AMC'][i]),'Category':str(df['Category'][i]),'SchemeCode':str(df['SchemeCode'][i]),'SchemeName':str(df['SchemeName'][i]),'Folio':str(df['Folio'][i]),'Amount':str(df['Amount'][i]),'NAV':str(df['NAV'][i]),'Units':str(df['Units'][i]),'OrderNo':str(df['OrderNo'][i]),'Date':str(df['Date'][i]),'Comments':str(df['Comments'][i])})
					# mongo.db.chqueIn.update_one({"ChqNo":chqno,"UCC":str(df['UCC'][i])}, {"$set":{"DepositedDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))}})

			else:
				print "no SINO SONO"

	return jsonify({"success":"true","message":"Successfully Uploaded"})





@app.route("/uploadtodayfile", methods=['POST'])
def uploadtodayfile():

	# slipcount = mongo.db.chqueIn.find({'dishon':False,'finas':True}).count()
	# slipcount = int(slipcount) + 1

	filename =""
	target="/opt/lampp/htdocs/mouseclicksys/uploads/today"
	
	for upload in request.files.getlist("file"):
		filename = upload.filename
		destination = "/".join([target, filename])

		upload.save(destination)
		df = pd.read_excel(destination, sheet_name='Sheet1')	
		for i in df.index:
			pnl = 0
			if str(df['Comments'][i]) == 'nan':
				# df['Comments'][i] = ""
				com = ""
			else:
				com = str(df['Comments'][i])

			if str(df['ChqNo'][i]) == 'nan':
				chqno = ""
			else:
				chqno = str(df['ChqNo'][i]).replace(':','')

			schemecode = str(df['SchemeCode'][i]).replace(':','')
			
			if str(df['NAV'][i]) == 'nan' and str(df['Units'][i]) == 'nan':

				# print {"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))}
				# ifexists = mongo.db.today.find_one({"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i])})
				ifexists = mongo.db.today.find_one({"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"Folio":str(df['Folio'][i]),"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i])})
				# print ifexists
				if ifexists == None:
					print "no match yet"
				else:
					# print {"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"Folio2":str(df['Folio'][i]),"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"Amount2":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))}
					# if str(df['Folio'][i]) != "New":
					# 	print "inside if folio new"
					# 	mongo.db.today.update_one({"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))} ,{"$set":{"OrderNo":str(df['OrderNo'][i])}},upsert=False)
					# else:
					# 	print "inside else folio new"
					mongo.db.today.update_one({"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i])} ,{"$set":{"Folio":str(df['Folio'][i]),"OrderNo":str(df['OrderNo'][i])}},upsert=False)

				# mongo.db.chqueIn.update_one({"ChqNo":chqno,"UCC":str(df['UCC'][i])}, {"$set":{"Slip":slipcount,"DepositedDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))}})
				mongo.db.chqueIn.update_one({"ChqNo":chqno,"UCC":str(df['UCC'][i])}, {"$set":{"DepositedDate":str(df['BuyDate'][i])}})

			
			else:
				
				ifexistsfornewfolio = mongo.db.today.find_one({"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i])})
				# ifexistsfornewfolio = list(ifexistsfornewfolio)
				print ifexistsfornewfolio
				if ifexistsfornewfolio['Folio'] == 'New':
					ifexists = mongo.db.today.find_one({"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i])})
				else:
					ifexists = mongo.db.today.find_one({"Folio":str(df['Folio'][i]),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i])})

				# ifexists = mongo.db.today.find_one({"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Folio":str(df['Folio'][i]),"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))})
				# ifexists = mongo.db.today.find_one({"Folio":str(df['Folio'][i]),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i])})
				# ifexists = mongo.db.today.find_one({"Folio":str(df['Folio'][i]),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i])})
			# ifexists = mongo.db.today.find_one({"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"Folio":str(df['Folio'][i]),"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i])})
			# print ifexists
				if ifexists == None:
					print "no match yet"
				else:
					print ifexists
					# if str(df['Folio'][i]) != 'New':
					ifexists2 = mongo.db.daywise.find_one({"Units":str(round(df['Units'][i],2)),"NAV":str(round(df['NAV'][i],2)),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"BuyDate":str(df['BuyDate'][i])})
					# else:
					# ifexists2 = mongo.db.daywise.find_one({"Units":str(round(df['Units'][i],2)),"NAV":str(round(df['NAV'][i],2)),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(int(float(df['Amount'][i]))),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))})

					if ifexists2 == None:
						navtoday = mongo.db.amcs.find_one({'SchemeCode':schemecode},{'NAV':True,'_id':False})
						pnl = (float(df['NAV'][i]) - float(navtoday['NAV'])) * float(df['Units'][i])

						# print {"Units":str(df['Units'][i]),"NAV":str(df['NAV'][i]),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))}
						if str(df['Category'][i]) == 'Liquid':
							mongo.db.daywise.insert({"liquid":True,"preaslqd":False,"dep":ifexists['dep'],"Comments":str(df['Comments'][i]),"reject":False,"AMC":str(df['AMC'][i]),'pnl':str(pnl),"Family":str(df['Family'][i]),"SchemeName":str(df['SchemeName'][i]),"Comments":com,"Units":str(round(df['Units'][i],2)),"NAV":str(round(df['NAV'][i],2)),"OrderNo":str(df['OrderNo'][i]),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"Date":str(df['BuyDate'][i])})
						else:
							mongo.db.daywise.insert({"liquid":False,"preaslqd":False,"dep":ifexists['dep'],"Comments":str(df['Comments'][i]),"reject":False,"AMC":str(df['AMC'][i]),'pnl':str(pnl),"Family":str(df['Family'][i]),"SchemeName":str(df['SchemeName'][i]),"Comments":com,"Units":str(round(df['Units'][i],2)),"NAV":str(round(df['NAV'][i],2)),"OrderNo":str(df['OrderNo'][i]),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"Date":str(df['BuyDate'][i])})
						# mongo.db.daywise.insert({"Units":str(round(df['Units'][i],2)),"NAV":str(round(df['NAV'][i],2)),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"Folio":str(int(float(df['Folio'][i]))),"Amount":str(int(float(df['Amount'][i]))),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))})
						# mongo.db.today.remove({"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Folio":str(df['Folio'][i]),"Amount":str(df['Amount'][i]),"BuyDate":str(df['BuyDate'][i].strftime('%d-%b-%y'))})
						mongo.db.today.remove({"AMC":str(df['AMC'][i]),"OrderNo":str(df['OrderNo'][i]),"ChqNo":str(chqno),"UCC":str(df['UCC'][i]),"Category":str(df['Category'][i]),"SchemeCode":schemecode,"Amount":str(df['Amount'][i])})
					else:
						print "Duplicate Entry"

	return jsonify({"success":"true","message":"Successfully Uploaded"})

@app.route("/uploaddailyamc", methods=["POST"])
def uploaddailyamc():
	filename =""
	target="/opt/lampp/htdocs/mouseclicksys/uploads/dailyamc"
	
	for upload in request.files.getlist("file"):
		filename = upload.filename
		destination = "/".join([target, filename])

		upload.save(destination)
		df = pd.read_excel(destination, sheet_name='AMC')	 
		# print("Column headings:")
		# print(df.columns)
		for i in df.index:
			# print str(df['SchemeCode'][i])
			amc = mongo.db.amcs.find_one({"SchemeCode":str(df['SchemeCode'][i])})
			if amc == None:
				amc = mongo.db.amcs.find_one({"SchemeName":str(df['SchemeName'][i])})
			# print amc
			if amc!=None:
				mongo.db.amcs.update_one({"_id":ObjectId(amc['_id'])} ,{"$set":{"NAV":str(df['NAV'][i])}},upsert=False)
				daywisenav = mongo.db.daywise.find({"SchemeName":str(df['SchemeName'][i])},{"Units":True,"NAV":True,"OrderNo":True,"_id":False})
				daywisenav = list(daywisenav)
				# print daywisenav
				for k in daywisenav:
					print k
					print float(df['NAV'][i])
					pnl = (float(df['NAV'][i]) - float(k['NAV'])) * float(k['Units'])
					print pnl
					mongo.db.daywise.update_one({"SchemeName":str(df['SchemeName'][i]),"OrderNo":k['OrderNo']},{"$set":{"pnl":str(pnl)}},upsert=False)
				print("already present")
			else:
				mongo.db.amcs.insert({"AMC":str(df['AMC'][i]),"Category":str(df['Category'][i]),"SchemeCode":str(df['SchemeCode'][i]),"SchemeName":str(df['SchemeName'][i]),"NAV":str(df['NAV'][i])})
				print("not present")
        # wb = load_workbook(filename = destination)
        # sheet_name =wb.get_sheet_names()[0]
        # sheet = wb.get_sheet_by_name(sheet_name)
        # max_rows= sheet.max_row
        # max_cols = sheet.max_column
        # studentinfo_keys =["rollno","name","email","mobile","parent_mobile"]
        # for r in range(2,max_rows+1):
        #     cntr=0
        #     tmp= {}
        #     for c in range(1,6):
        #         tmp[studentinfo_keys[cntr]] =sheet.cell(row=r,column=c).value
        #         cntr+=1
        #     if tmp['rollno'] != None:
        #         if tmp["mobile"] != None:
        #             tmp["class"] = class_selected
        #             tmp["rollno"]= str(tmp["rollno"])
        #             tmp["mobile"]=str(tmp["mobile"])[:10]
        #             tmp['email'] = str(tmp['email'])
        #             dupl = mongo.db.students.find_one({"mobile":tmp["mobile"]})
        #             print dupl
        #             mongo.db.students.insert(tmp)
        # os.remove(destination)
	return jsonify({"success":"true","message":"Successfully Uploaded"})


@app.route("/getsliplesscheques",methods=['POST'])
def getsliplesscheques():
	dep = request.get_json()['Dep']
	slipless = mongo.db.chqueIn.find({"dep":dep,"Slip":"","finas":True,"DepositedDate": { "$ne" : ""}},{"_id":False})
	# slipless = mongo.db.chqueIn.find({"$and": [{"Slip": "","finas":True}, {"DepositedDate": { "$ne" : ""}}]},{"_id":False})
	slipless = list(slipless)
	if len(slipless):
		return jsonify({"success":"true","slipless":slipless})
	else:
		return jsonify({"success":"false","message":"No Slip Assign Remaining!"})


@app.route("/addslipnumber", methods=['POST'])
def addslipnumber():
	formdata = request.get_json()
	# print formdata
	for x in formdata:
		print x
		ifexists = mongo.db.chqueIn.find_one({"Slip":x['Slip'],"finas":True},{"_id":False})
		print ifexists
		if ifexists == None:
			mongo.db.chqueIn.update_one({"ChqNo":x['ChqNo'],"UCC":x['UCC'],"AccountNo":x['AccountNo']},{"$set":{"Slip":x['Slip']}})
		else:
			return jsonify({"success":"false","message":"Duplicate Slip Number Detected!"})
		
	return jsonify({"success":"true"})

@app.route("/getuccdatewisetransactions", methods=['POST'])
def getuccdatewisetransactions():
	formdata = request.get_json()

	rejtrans = mongo.db.daywise.find({"UCC":formdata['UCC'],"Date":formdata['Date']},{"_id":False})
	rejtrans = list(rejtrans)
	headers=["Category","SchemeCode","SchemeName","Folio","Amount","OrderNo","Date"]	
	
	return jsonify({"success":"true","rejtrans":rejtrans,"headers":headers})

@app.route("/getDishonChqs", methods=['POST'])
def getDishonChqs():
	dep = request.get_json()['Dep']
	dishon = mongo.db.chqueIn.find({'dep':dep,"dishon":True},{"_id":False})
	headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","Slip","Comments"]
	dishon = list(dishon)
	# print finas
	if len(dishon):
		for x in dishon:
			if str(x['Slip']) == "nan":
				x['Slip'] = ""
			elif x['Slip'] == "":
				x['Slip'] = ""
			else:
				x["Slip"]=int(x["Slip"])
			# x['DepositedDate'] = datetime.strptime(x['DepositedDate'], '%d-%b-%y')


	if len(dishon):	
		return jsonify({"success":"true","dishonlist":dishon,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Dishonored Cheques!"})

@app.route("/getAssignedCheques", methods=['POST'])
def getAssignedCheques():
	dep = request.get_json()['Dep']
	finas = mongo.db.chqueIn.find({"dep":dep,"finas":True},{"_id":False})
	headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","Slip","Comments"]
	finas = list(finas)
	# print finas
	if len(finas):
		for x in finas:
			if str(x['Slip']) == "nan":
				x['Slip'] = ""
			elif x['Slip'] == "":
				x['Slip'] = ""
			else:
				x["Slip"]=int(x["Slip"])
			# x['DepositedDate'] = datetime.strptime(x['DepositedDate'], '%d-%b-%y')


	if len(finas):	
		return jsonify({"success":"true","finas":finas,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Assigned Cheques!"})

@app.route("/getClientByucc",methods=["POST"])
def getClientByucc():
	clientData = mongo.db.clientlist.find_one({"UCC":request.get_json()['ucc']},{"_id":False})
	print clientData
	if len(clientData):	
		return jsonify({"success":"true","clientData":clientData})
	else:
		return jsonify({"success":"false","message":"Something Went Wrong!"})

@app.route("/getFamilyHeads",methods=["POST"])
def getFamilyHeads():
	familyheads = mongo.db.familylist.find({})
	familyheads=list(familyheads)
	if len(familyheads):
		for familyhead in familyheads:
			familyhead["_id"]=str(familyhead["_id"])
		headers=["ClientName","Family","UCC","Bank1","Acc1","Bank2","Acc2","Bank3","Acc3","username","password"]
		return jsonify({"success":"true","familyheads":familyheads,"headers":headers,"message":"Client List Loaded Successfully"})
	else:
		return jsonify({"success":"false","message":"No Client Found!"})

@app.route("/getfamilynames",methods=["POST"])
def getfamilynames():
	fnames = mongo.db.clientlist.find({},{"Family":True}).distinct('Family')
	return jsonify({"success":"true","fnames":fnames,"message":"Family Names Loaded Successfully!"})

@app.route("/getChqIns",methods=['POST'])
def getChqIns():
	dep = request.get_json()['Dep']
	chqinlist = mongo.db.chqueIn.find({'finas':False,'dep':dep},{'Slip':False,'DepositedDate':False})
	chqinlist=list(chqinlist)
	if len(chqinlist):
		for x in chqinlist:
			x["_id"]=str(x["_id"])
		#headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","TotalSum","Slip","Comments"]
		headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","Comments"]

		return jsonify({"success":"true","chqinlist":chqinlist,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Cheques Found!"})




@app.route("/exportswitchdone",methods=['POST'])
def exportswitchdone():
	data =  request.get_json()
	dep = data['Dep']
	# print data
	date = datetime.strptime(data['sodate'], '%Y-%m-%d')
	date = date.strftime('%d-%b-%y')

	switchdonelist = mongo.db.switchout.find({'SwitchDate':date,'dep':dep},{"_id":False,"SOUnits":False,"SONAV":False})
	switchdonelist = list(switchdonelist)

	if len(switchdonelist):

	# 	for x in switchdonelist:
	# 		x['NAV'] = ""
	# 		x['Units'] = ""

	# 	print todaylist
		switchdonelistdf= pd.DataFrame(switchdonelist)
		
		writer = ExcelWriter('switchout.xlsx')
		switchdonelistdf.to_excel(writer,'Sheet1')
		writer.save()
		# return send_from_directory(directory=target, filename="today.xslx",as_attachment=True)
		# return send_from_directory(target,"today.xslx", as_attachment=True)
		return jsonify({"success":"true"})
		# if len(todaylist):
		# 	for x in todaylist:
		# 		x["_id"]=str(x["_id"])
		# 	headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","BuyDate","OrderNo","ChqNo"]
		# 	return jsonify({"success":"true","todaylist":todaylist,"headers":headers})
		# else:
		# 	return jsonify({"success":"false","message":"No Today Found!"})
	else:
		return jsonify({"success":"false","message":"No Switch Done for the date found!"})





@app.route("/exportTodays",methods=['POST'])
def exportTodays():
	data =  request.get_json()
	dep = data['Dep']
	# print data
	# date = datetime.strptime(data['todaydate'], '%Y-%m-%d')
	# date = date.strftime('%d-%b-%y')

	todaylist = mongo.db.today.find({'BuyDate':data['todaydate'],'dep':dep},{'Slip':False,"_id":False})
	todaylist = list(todaylist)

	if len(todaylist):

		for x in todaylist:
			x['NAV'] = ""
			x['Units'] = ""
			x['Comments'] = ""

		print todaylist
		todaylistdf= pd.DataFrame(todaylist)

		todaylistdf = todaylistdf[["Family","UCC","AMC","Category","SchemeCode","SchemeName","Folio","Amount","Units","NAV","BuyDate","OrderNo","ChqNo","Comments"]]
		
		writer = ExcelWriter('today.xlsx')
		todaylistdf.to_excel(writer,'Sheet1')
		writer.save()
		# return send_from_directory(directory=target, filename="today.xslx",as_attachment=True)
		# return send_from_directory(target,"today.xslx", as_attachment=True)
		return jsonify({"success":"true"})
		# if len(todaylist):
		# 	for x in todaylist:
		# 		x["_id"]=str(x["_id"])
		# 	headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","BuyDate","OrderNo","ChqNo"]
		# 	return jsonify({"success":"true","todaylist":todaylist,"headers":headers})
		# else:
		# 	return jsonify({"success":"false","message":"No Today Found!"})
	else:
		return jsonify({"success":"false","message":"No Today for date found!"})


@app.route("/getTodays",methods=['POST'])
def getTodays():
	dep = request.get_json()['Dep']
	todaylist = mongo.db.today.find({'dep':dep},{'Slip':False})
	todaylist=list(todaylist)
	if len(todaylist):
		for x in todaylist:
			x["_id"]=str(x["_id"])
		headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","BuyDate","OrderNo","ChqNo"]

		return jsonify({"success":"true","todaylist":todaylist,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Today Found!"})

@app.route("/getDaywiseliquid",methods=['POST'])
def getDaywiseliquid():
	dep = request.get_json()['Dep']
	liquidlist = mongo.db.daywise.find({'liquid':True,'dep':dep})
	liquidlist = list(liquidlist)
	if len(liquidlist):
		for x in liquidlist:
			x["_id"]=str(x["_id"])
			# print x['pnl']
			if x['pnl'] :
				x['pnl'] = round(float(x['pnl']))
		#headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","TotalSum","Slip","Comments"]
		headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","Units","NAV","OrderNo","Date","pnl","Comments"]

		return jsonify({"success":"true","liquidlist":liquidlist,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Liquid Found!"})


@app.route("/getResidue",methods=['POST'])
def getResidue():
	residuelist = mongo.db.residue.find({})
	residuelist=list(residuelist)
	if len(residuelist):
		for x in residuelist:
			x["_id"]=str(x["_id"])
			# print x['pnl']
			# if x['pnl'] :
			# 	x['pnl'] = round(float(x['pnl']))
		#headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","TotalSum","Slip","Comments"]
		headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","Units","NAV","OrderNo","Date","pnl","Comments",'SONO']

		return jsonify({"success":"true","residuelist":residuelist,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Residue Found!"})



@app.route("/getDaywise",methods=['POST'])
def getDaywise():
	daywiselist = mongo.db.daywise.find({}).limit(1000)
	daywiselist=list(daywiselist)
	if len(daywiselist):
		for x in daywiselist:
			x["_id"]=str(x["_id"])
			# print x['pnl']
			if x['pnl'] :
				x['pnl'] = round(float(x['pnl']))
		#headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","TotalSum","Slip","Comments"]
		headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","Units","NAV","OrderNo","Date","pnl","Comments"]

		return jsonify({"success":"true","daywiselist":daywiselist,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Cheques Found!"})

@app.route("/getdaywisewithfilter",methods=['POST'])
def getdaywisewithfilter():
	data = request.get_json()
	print data
	if data['Date'] != "none":
		pass
		temp = data['Date'].split('T')
		buydate = datetime.strptime(temp[0], '%Y-%m-%d')
		findate = buydate.strftime('%d-%b-%y')
		print findate
	else:
		findate = 'none'

	if data['Dep'] == "none":
		if data['UCC'] == "none" and data['family'] == "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({})
		elif data['UCC'] != "none" and data['family'] == "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC']})
		elif data['UCC'] == "none" and data['family'] != "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'Family':data['family']})
		elif data['UCC'] == "none" and data['family'] == "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'Date':findate})
		elif data['UCC'] != "none" and data['family'] != "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'Family':data['family']})
		elif data['UCC'] == "none" and data['family'] != "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'Date':str(findate),'Family':data['family']})
		elif data['UCC'] != "none" and data['family'] == "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'Date':str(findate)})
		elif data['UCC'] != "none" and data['family'] != "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'Family':data['family'],'Date':str(findate)})
	else:
		if data['UCC'] == "none" and data['family'] == "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'dep':data['Dep']})
		elif data['UCC'] != "none" and data['family'] == "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'dep':data['Dep']})
		elif data['UCC'] == "none" and data['family'] != "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'Family':data['family'],'dep':data['Dep']})
		elif data['UCC'] == "none" and data['family'] == "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'Date':findate,'dep':data['Dep']})
		elif data['UCC'] != "none" and data['family'] != "none" and data['Date'] == "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'Family':data['family'],'dep':data['Dep']})
		elif data['UCC'] == "none" and data['family'] != "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'Date':str(findate),'Family':data['family'],'dep':data['Dep']})
		elif data['UCC'] != "none" and data['family'] == "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'Date':str(findate),'dep':data['Dep']})
		elif data['UCC'] != "none" and data['family'] != "none" and data['Date'] != "none":
			pass
			daywiselist = mongo.db.daywise.find({'UCC':data['UCC'],'Family':data['family'],'Date':str(findate),'dep':data['Dep']})

	# amounttotal = 0
	daywiselist=list(daywiselist)
	if len(daywiselist):
		for x in daywiselist:
			x["_id"]=str(x["_id"])
			# amounttotal += int(x['Amount'])
			# print x['pnl']
			if x['pnl'] :
				x['pnl'] = round(float(x['pnl']))
	#headers=["Family","UCC","Bank","AccountNo","ChqNo","Amount","DepositedDate","TotalSum","Slip","Comments"]

		headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","Units","NAV","OrderNo","Date","pnl","Comments"]
		return jsonify({"success":"true","daywiselist":daywiselist,"headers":headers})
	else:
		return jsonify({"success":"false","message":"Wrong combination of input!"})

@app.route("/getallswitchout",methods=['POST'])
def getallswitchout():
	dep = request.get_json()['Dep']
	so = mongo.db.switchout.find({'dep':dep})
	so=list(so)
	if len(so):
		for s in so:
			s["_id"]=str(s["_id"])

		headers=["Family","UCC","Category","SchemeCode","SchemeName","Folio","Amount","Units","NAV","OrderNo","Date","Comments","SODate","SICategory","SISchemeCode","SISchemeName","SIFolio","SONO","SINO"]
		
		return jsonify({"success":"true","so":so,"headers":headers})
	else:
		return jsonify({"success":"false","message":"No Switch Out Found!"})

@app.route("/getalldep",methods=['POST'])
def getalldep():
	deps = mongo.db.departments.find({},{'_id':False})
	deps=list(deps)
	if len(deps):
		return jsonify({"success":"true","deps":deps})
	else:
		return jsonify({"success":"false","message":"No Departments Found!"})

@app.route("/getallucc",methods=['POST'])
def getallucc():
	uccs = mongo.db.clientlist.find({},{"UCC":True})
	uccs=list(uccs)
	if len(uccs):
		for ucc in uccs:
			ucc["_id"]=str(ucc["_id"])
		return jsonify({"success":"true","uccs":uccs})
	else:
		return jsonify({"success":"false","message":"No Client Found!"})

@app.route("/getallclients",methods=["POST"])
def getallclients():
	clists = mongo.db.clientlist.find({})
	clists=list(clists)
	if len(clists):
		for clist in clists:
			clist["_id"]=str(clist["_id"])
		headers=["ClientName","Family","UCC","Bank1","Acc1","Bank2","Acc2","Bank3","Acc3",]
		return jsonify({"success":"true","clists":clists,"headers":headers,"message":"Client List Loaded Successfully"})
	else:
		return jsonify({"success":"false","message":"No Client Found!"})

@app.route("/getallamcs",methods=["POST"])
def getallamcs():
	amcs = mongo.db.amcs.find({})
	amcs=list(amcs)
	if len(amcs):	
		for amc in amcs:
			amc["_id"]=str(amc["_id"])
		return jsonify({"success":"true","amcs":amcs,"message":"Scheme Loaded Successfully"})
	else:
		return jsonify({"success":"false","message":"no amc Found"})

@app.route("/getamcinfo",methods=["POST"])
def getamcinfo():
	amcs = mongo.db.amcs.find({"_id":ObjectId(request.get_json()["id"])})
	return jsonify({"success":"true","message":"Scheme Info Updated Successfully"})

@app.route("/editamc",methods=["POST"])
def editamc():
	print(request.get_json())
	mongo.db.amcs.update_one({"_id":ObjectId(request.get_json()["id"])} ,{"$set":request.get_json()["info"]},upsert=False)
	return jsonify({"success":"true","message":"Scheme Info Updated Successfully"})

@app.route("/deleteamc",methods=["POST"])
def deleteamc():
	mongo.db.amcs.remove({"_id":ObjectId(request.get_json()["id"])})
	return jsonify({"success":"true","message":"Scheme Deleted Successfully"})


@app.route("/editFamilyhead",methods=["POST"])
def editFamilyhead():
	ucc = request.get_json()['ucc']
	family = request.get_json()['family']
	familylist = mongo.db.familylist.find_one({"UCC":ucc})
	if familylist == None :
		oldfhd = mongo.db.familylist.find_one({"Family" : family})
		if oldfhd != None:
			mongo.db.clientlist.update_one({"UCC":oldfhd['UCC']} ,{"$set":{"familyhead":False}},upsert=False)
			oldfh = mongo.db.familylist.remove({'Family':family})
		
		clientdata = mongo.db.clientlist.find_one({"UCC":ucc})
		# print clientdata
		mongo.db.clientlist.update_one({"UCC":ucc} ,{"$set":{"familyhead":True}},upsert=False)
		mongo.db.familylist.insert({"ClientName":str(clientdata['ClientName']),"Family":str(clientdata['Family']),"UCC":str(clientdata['UCC']),"Bank1":str(clientdata['Bank1']),"Acc1":str(clientdata['Acc1']),"Bank2":str(clientdata['Bank2']),"Acc2":str(clientdata['Acc2']),"Bank3":str(clientdata['Bank3']),"Acc3":str(clientdata['Acc3']),"username":str(clientdata['UCC']),"password":str(clientdata['Family'])})
		return jsonify({"success":"true","message":"Family Head Set Successfully!"})	
	else:
		# mongo.db.clientlist.insert({"ClientName":str(df['ClientName'][i]),"Family":str(df['Family'][i]),"UCC":str(df['UCC'][i]),"Bank1":str(df['Bank1'][i]),"Acc1":str(df['AccountNo'][i]),"Bank2":str(df['Bank2'][i]),"Acc2":str(df['AccountNo2'][i]),"Bank3":str(df['Bank3'][i]),"Acc3":str(df['AccountNo3'][i]),"familyhead":False})
		return jsonify({"success":"false","message":"Alredy a Family Head!"})		


@app.route("/addNewAMC",methods=["POST"])
def addNewAMC():
	data = request.get_json()
	print data
	
	ifexists = mongo.db.amcs.find_one({"SchemeCode":data['SchemeCode']})
	if ifexists == None :
		mongo.db.amcs.insert(data)
		return jsonify({"success":"true","message":"New Scheme Inserted Successfully!"})	
	else:
		return jsonify({"success":"false","message":"Scheme Already Exists!"})

@app.route("/addNewClient",methods=["POST"])
def addNewClient():
	ucc = request.get_json()['UCC']
	ifexists = mongo.db.clientlist.find_one({"UCC":ucc})
	if ifexists == None :
		mongo.db.clientlist.insert({"ClientName":str(request.get_json()['ClientName']),"Family":str(request.get_json()['Family']),"UCC":str(ucc),"Bank1":str(request.get_json()['Bank1']),"Acc1":str(request.get_json()['Acc1']),"Bank2":str(request.get_json()['Bank2']),"Acc2":str(request.get_json()['Acc2']),"Bank3":str(request.get_json()['Bank3']),"Acc3":str(request.get_json()['Acc3']),"familyhead":False})
		return jsonify({"success":"true","message":"New Client Inserted Successfully!"})	
	else:
		return jsonify({"success":"false","message":"UCC Already Exists!"})

@app.route("/editClient",methods=["POST"])
def editClient():
	ucc = request.get_json()
	print ucc
	ifexists = mongo.db.clientlist.find_one({"UCC":ucc['UCC']})
	if ifexists != None :
		if ifexists['familyhead'] == False:
			if ucc.get('ClientName') != None:
				mongo.db.clientlist.update_one({"UCC":ucc['UCC']} ,{"$set":{"ClientName":str(ucc['ClientName']),"Family":str(ucc['Family']),"UCC":str(ucc['UCC']),"Bank1":str(ucc['Bank1']),"Acc1":str(ucc['Acc1']),"Bank2":str(ucc['Bank2']),"Acc2":str(ucc['Acc2']),"Bank3":str(ucc['Bank3']),"Acc3":str(ucc['Acc3'])}},upsert=False)
			else:
				mongo.db.clientlist.update_one({"UCC":ucc['UCC']} ,{"$set":{"ClientName":"","Family":str(ucc['Family']),"UCC":str(ucc['UCC']),"Bank1":str(ucc['Bank1']),"Acc1":str(ucc['Acc1']),"Bank2":str(ucc['Bank2']),"Acc2":str(ucc['Acc2']),"Bank3":str(ucc['Bank3']),"Acc3":str(ucc['Acc3'])}},upsert=False)

		else:
			if ucc.get('ClientName') != None:
				mongo.db.clientlist.update_one({"UCC":ucc['UCC']} ,{"$set":{"ClientName":str(ucc['ClientName']),"Family":str(ucc['Family']),"UCC":str(ucc['UCC']),"Bank1":str(ucc['Bank1']),"Acc1":str(ucc['Acc1']),"Bank2":str(ucc['Bank2']),"Acc2":str(ucc['Acc2']),"Bank3":str(ucc['Bank3']),"Acc3":str(ucc['Acc3'])}},upsert=False)
				mongo.db.familylist.update_one({"UCC":ucc['UCC']} ,{"$set":{"ClientName":str(ucc['ClientName']),"Family":str(ucc['Family']),"UCC":str(ucc['UCC']),"Bank1":str(ucc['Bank1']),"Acc1":str(ucc['Acc1']),"Bank2":str(ucc['Bank2']),"Acc2":str(ucc['Acc2']),"Bank3":str(ucc['Bank3']),"Acc3":str(ucc['Acc3'])}},upsert=False)
			else:
				mongo.db.clientlist.update_one({"UCC":ucc['UCC']} ,{"$set":{"ClientName":"","Family":str(ucc['Family']),"UCC":str(ucc['UCC']),"Bank1":str(ucc['Bank1']),"Acc1":str(ucc['Acc1']),"Bank2":str(ucc['Bank2']),"Acc2":str(ucc['Acc2']),"Bank3":str(ucc['Bank3']),"Acc3":str(ucc['Acc3'])}},upsert=False)
				mongo.db.familylist.update_one({"UCC":ucc['UCC']} ,{"$set":{"ClientName":"","Family":str(ucc['Family']),"UCC":str(ucc['UCC']),"Bank1":str(ucc['Bank1']),"Acc1":str(ucc['Acc1']),"Bank2":str(ucc['Bank2']),"Acc2":str(ucc['Acc2']),"Bank3":str(ucc['Bank3']),"Acc3":str(ucc['Acc3'])}},upsert=False)
				

		return jsonify({"success":"true","message":"Client Data Updated Successfully!"})	
	else:
		return jsonify({"success":"false","message":"Client Does Not Exists!"})

@app.route("/addnewchqin",methods=["POST"])
def addnewchqin():
	formdata = request.get_json()
	dep = formdata['Dep']
	ucc = formdata['ucc']['UCC']
	chqno = formdata['ChqNo']
	print formdata
	ifexists = mongo.db.chqueIn.find_one({"UCC":ucc,"ChqNo":chqno})
	if ifexists == None :
		mongo.db.chqueIn.insert({'dep':dep,"DepositedDate":"","Bank":str(formdata['Bank']),"UCC":str(ucc),"AccountNo":str(formdata['AccountNo']),"Family":str(formdata['Family']),"ChqNo":str(chqno),"Amount":str(formdata['Amount']),"preas":False,"finas":False,"dishon":False,"Slip":""})
		# mongo.db.chqueIn.insert({"Bank":str(formdata['Bank']),"UCC":str(ucc),"AccountNo":str(formdata['AccountNo']),"Family":str(formdata['Family']),"ChqNo":str(chqno),"Amount":str(formdata['Amount']),"DepositedDate":str(formdata['DepositedDate'].strftime('%d-%b-%y')),"Slip":str(formdata['Slip']),"Comments":str(formdata['Comments'])})
		return jsonify({"success":"true","message":"Cheque In Successfully!"})
	else:
		return jsonify({"success":"false","message":"Entry Already Exists!"})

@app.route("/editchqin",methods=["POST"])
def editchqin():
	formdata = request.get_json()
	ifexists = mongo.db.chqueIn.find_one({"UCC":formdata['UCC'],"ChqNo":formdata['ChqNo']})
	if ifexists != None :
		mongo.db.chqueIn.update_one({"UCC":formdata['UCC'],"ChqNo":formdata['ChqNo']} ,{"$set":{"Bank":str(formdata['Bank']),"UCC":str(formdata['UCC']),"AccountNo":str(formdata['AccountNo']),"Family":str(formdata['Family']),"ChqNo":str(formdata['ChqNo']),"Amount":str(formdata['Amount']),"DepositedDate":str(formdata['DepositedDate'].strftime('%d-%b-%y')),"TotalSum":str(formdata['TotalSum']),"Slip":str(formdata['Slip']),"Comments":str(formdata['Comments'])}},upsert=False)
		return jsonify({"success":"true","message":"Cheque Entry Updated Successfully!"})	
	else:
		return jsonify({"success":"false","message":"Entry Does Not Exists!"})	


@app.route("/preassignLqd",methods=['POST'])
def preassignLqd():
	formdata = request.get_json()
	print formdata
	for key, value in dict.items(formdata):
		# print key, value
		# res = value.split(",")
		# print res
		mongo.db.daywise.update_one({"OrderNo":value}, {"$set":{"preaslqd":True}})
	
	return jsonify({"success":"true","message":"Cheque Preassigned Successfully!"})


@app.route("/preassignlqdremove",methods=['POST'])
def preassignlqdremove():
	formdata = request.get_json()
	# print formdata
	# for key, value in dict.items(formdata):
		#print key, value
	mongo.db.daywise.update_one({"OrderNo":formdata['orderno']}, {"$set":{"preaslqd":False}})
	
	return jsonify({"success":"true","message":"Cheque Restored Successfully!"})


@app.route("/preassign",methods=['POST'])
def preassign():
	formdata = request.get_json()
	# print formdata
	for key, value in dict.items(formdata):
		# print key, value
		res = value.split(",")
		# print res
		mongo.db.chqueIn.update_one({"ChqNo":res[0],"AccountNo":res[1]}, {"$set":{"preas":True}})
	
	return jsonify({"success":"true","message":"Cheque Preassigned Successfully!"})

@app.route("/preassignremove",methods=['POST'])
def preassignremove():
	formdata = request.get_json()
	# print formdata
	# for key, value in dict.items(formdata):
		#print key, value
	mongo.db.chqueIn.update_one({"ChqNo":formdata['chqno']}, {"$set":{"preas":False}})
	
	return jsonify({"success":"true","message":"Cheque Restored Successfully!"})


@app.route("/getuccdatafromdaywiseold", methods=['POST'])
def getuccdatafromdaywiseold():
	ucc = request.get_json()
	uccdaywise = []
	result = mongo.db.daywise.find({'UCC':ucc['UCC']}).distinct('SchemeCode')
	# result = mongo.db.daywise.find({'UCC':ucc['UCC']},{'Category':True,'SchemeCode':True,'SchemeName':True,'Folio':True,'Amount':True}).distinct('SchemeCode')
	result = list(result)
	if len(result):
		for x in result:
			temp = mongo.db.daywise.find_one({'SchemeCode':x,'UCC':ucc['UCC']},{'Category':True,'SchemeCode':True,'SchemeName':True,'Folio':True,'pnl':True,'_id':False})
			#temp = list(temp)

			uccdaywise.append(temp)
	
	# print uccdaywise
	headers=["Category","SchemeCode","SchemeName","Folio","PNL","Amount"]	
	return jsonify({"success":"true","uccdaywise":uccdaywise,"uccheaders":headers})


@app.route("/getamcwiseuccdataamc",methods=["POST"])
def getamcwiseuccdataamc():
	data = request.get_json()
	finaldata = []
	prefinaldata = []
	print data

	for x,y in dict.items(data['schemenames']):
		# res = y.split(",")
		# print res
		schemedata = mongo.db.amcs.find_one({'SchemeName':y},{"_id":False})
		schemedata['pnl'] = 0
		finaldata.append(schemedata)

	print finaldata
	return jsonify({"success":"true","finaldataamc":finaldata})


@app.route("/getamcwiseuccdata",methods=["POST"])
def getamcwiseuccdata():
	data = request.get_json()
	finaldata = []
	prefinaldata = []
	print data

	for x,y in dict.items(data['newschemeamc']):
		res = y.split(",")
		# print res

		ifexists = mongo.db.daywise.find_one({'UCC':data['UCC'],'AMC':res[0]},{'Folio':True,'_id':False})
		if ifexists != None:
			schemedata = mongo.db.amcs.find_one({'SchemeCode':res[1]},{"_id":False})
			schemedata['Folio'] = ifexists['Folio']
			schemedata['pnl'] = 0
			# print schemedata

			finaldata.append(schemedata)
		else:
			schemedata = mongo.db.amcs.find_one({'SchemeCode':res[1]},{"_id":False})
			schemedata['Folio'] = "New"
			schemedata['pnl'] = 0
			# print schemedata
			finaldata.append(schemedata)

	print finaldata
	return jsonify({"success":"true","finaldata":finaldata})


@app.route("/getuccamcwisenewschemes",methods=['POST'])
def getuccamcwisenewschemes():
	data = request.get_json()
	print data
	newschemes = []
	result = mongo.db.daywise.find({'UCC':data['UCC'],'AMC':data['AMC']}).distinct('SchemeName')
	result = list(result)

	print result

	result2 = mongo.db.amcs.find({'AMC':data['AMC']},{"_id":False})
	result2 = list(result2)

	# print result2

	for x in result2:
		if x['SchemeName'] not in result:
			# print x
			newschemes.append(x)
	
	newschemehead=["Category","SchemeCode","SchemeName"]
	return jsonify({"success":"true","uccamcnewscheme":newschemes,"newschemehead":newschemehead})



@app.route("/getuccwisenewschemes",methods=['POST'])
def getuccwisenewschemes():
	ucc = request.get_json()
	newschemes = []
	result = mongo.db.daywise.find({'UCC':ucc['UCC']}).distinct('SchemeCode')
	result = list(result)

	print result

	result2 = mongo.db.amcs.find({},{"_id":False})
	result2 = list(result2)

	# print result2

	for x in result2:
		if x['SchemeCode'] not in result:
			# print x
			newschemes.append(x)
	
	newschemehead=["AMC","Category","SchemeCode","SchemeName"]
	return jsonify({"success":"true","uccnewscheme":newschemes,"newschemehead":newschemehead})


@app.route("/getuccdatafromdaywiseamc",methods=['POST'])
def getuccdatafromdaywiseamc():
	data = request.get_json()
	uccdaywiseamc = []
	pnltotal = 0
	result = mongo.db.daywise.find({'UCC':data['UCC'],'AMC':data['AMC']}).distinct('SchemeName')
	result = list(result)
	if len(result):
		for x in result:
			pnltotal = 0
			singleschemedata = mongo.db.daywise.find_one({'SchemeName':x,'UCC':data['UCC'], 'AMC':data['AMC']},{'AMC':True,'Category':True,'SchemeCode':True,'SchemeName':True,'_id':False})
			temp = mongo.db.daywise.find({'SchemeName':x,'UCC':data['UCC'],'AMC':data['AMC']},{'pnl':True,'_id':False})
			temp = list(temp)

			if len(temp):
				for x in temp:
					if x['pnl']:
						pnltotal += round(float(x['pnl']))
				# print pnltotal
				# print "next scheme"
				singleschemedata['pnl'] = pnltotal
			
			# print singleschemedata
			uccdaywiseamc.append(singleschemedata)
			# print uccdaywiseamc

	headers=["Category","SchemeCode","SchemeName","PNL","Amount"]	
	return jsonify({"success":"true","uccdaywiseamc":uccdaywiseamc,"uccheadersamc":headers})	


@app.route("/getuccdatafromdaywise", methods=['POST'])
def getuccdatafromdaywise():
	ucc = request.get_json()
	uccdaywise = []
	pnltotal = 0
	result = mongo.db.daywise.find({'UCC':ucc['UCC']}).distinct('SchemeCode')
	# result = mongo.db.daywise.find({'UCC':ucc['UCC']},{'Category':True,'SchemeCode':True,'SchemeName':True,'Folio':True,'Amount':True}).distinct('SchemeCode')
	result = list(result)
	if len(result):
		for x in result:
			pnltotal = 0
			singleschemedata = mongo.db.daywise.find_one({'SchemeCode':x,'UCC':ucc['UCC']},{'AMC':True,'Category':True,'SchemeCode':True,'SchemeName':True,'Folio':True,'_id':False})
			temp = mongo.db.daywise.find({'SchemeCode':x,'UCC':ucc['UCC']},{'pnl':True,'_id':False})
			temp = list(temp)			
			if len(temp):
				for x in temp:
					if x['pnl']:
						pnltotal += round(float(x['pnl']))
				# print pnltotal
				# print "next scheme"
				singleschemedata['pnl'] = int(pnltotal)
			
			# print singleschemedata
			uccdaywise.append(singleschemedata)
			# print uccdaywise
	
	# print uccdaywise
	headers=["AMC","Category","SchemeCode","SchemeName","Folio","PNL","Amount"]	
	return jsonify({"success":"true","uccdaywise":uccdaywise,"uccheaders":headers})

@app.route("/finalassignliquid", methods=['POST'])
def finalassignliquid():
	newamt = 0
	formdata = request.get_json()
	buydate = datetime.strptime(formdata['SwitchDate'], '%Y-%m-%d')
	print formdata
	if formdata.get('origamt') == None:
		print "Full Entry"
		ifexists = mongo.db.daywise.find_one({'OrderNo':formdata['OrderNo']},{"_id":False})
		if ifexists != None:
			print ifexists
			for x in formdata['uccdaywiseamc']:
				print x
				if x.get('values') != None:
					if x['values'] != '':
						mongo.db.switchout.insert({"Category":ifexists['Category'],"Folio":ifexists['Folio'],"AMC":ifexists['AMC'],"Family":ifexists['Family'],"Comments":ifexists['Comments'],"Date":ifexists['Date'],"Units":ifexists['Units'],"Amount":ifexists['Amount'],"UCC":ifexists['UCC'],"SchemeName":ifexists['SchemeName'],"SchemeCode":ifexists['SchemeCode'],"NAV":ifexists['NAV'],"OrderNo":ifexists['OrderNo'],"SICategory":x['Category'],"SISchemeCode":x['SchemeCode'],"SISchemeName":x['SchemeName'],"SIFolio":ifexists['Folio'],"SIAmount":x['values'],"SwitchDate":str(buydate.strftime('%d-%b-%y')),"SONO":"","SINO":""})
			
			mongo.db.daywise.remove({"OrderNo":str(formdata['OrderNo'])})
		else:
			print "Order No Not Matched!"
	else:
		print "Partial Entry"
		newamt = int(formdata['origamt']) - int(formdata['liquidamount'])
		# newunits1 = float(formdata['liquidamount']) / 
		ifexists = mongo.db.daywise.find_one({'OrderNo':formdata['OrderNo']},{"_id":False})
		if ifexists != None:
			print ifexists
			newunits1 = float(formdata['liquidamount']) / float(ifexists['NAV'])
			newunits2 = float(newamt) / float(ifexists['NAV'])
			for x in formdata['uccdaywiseamc']:
				if x.get('values') != None:
					if x['values'] != '':
						mongo.db.switchout.insert({"Category":ifexists['Category'],"Folio":ifexists['Folio'],"AMC":ifexists['AMC'],"Family":ifexists['Family'],"Comments":ifexists['Comments'],"Date":ifexists['Date'],"Units":str(round(newunits1,4)),"Amount":formdata['liquidamount'],"UCC":ifexists['UCC'],"SchemeName":ifexists['SchemeName'],"SchemeCode":ifexists['SchemeCode'],"NAV":ifexists['NAV'],"OrderNo":ifexists['OrderNo'],"SICategory":x['Category'],"SISchemeCode":x['SchemeCode'],"SISchemeName":x['SchemeName'],"SIFolio":ifexists['Folio'],"SIAmount":x['values'],"SwitchDate":str(buydate.strftime('%d-%b-%y')),"SONO":"","SINO":""})
			
			mongo.db.daywise.update_one({"UCC":formdata['UCC'],"OrderNo":formdata['OrderNo']} ,{"$set":{"Amount":newamt,"Units":round(newunits2,4),"preaslqd":False}},upsert=False)
		else:
			print "Order No Not Matched!"

	return jsonify({"success":"true","message":"Liquid Assigned Successfully!"})

@app.route("/finalassigncheque", methods=['POST'])
def finalassigncheque():
	formdata = request.get_json()
	dep = formdata['Dep']
	print formdata['daywiseuccdata']
	for x in formdata['daywiseuccdata']:
		print x
		# formdata['BuyDate'].strftime('%d-%b-%y')
		buydate = datetime.strptime(formdata['BuyDate'], '%Y-%m-%d')
		if x.get('values') != None:
			if x['values'] != '':
				mongo.db.today.insert({'dep':dep,"AMC":str(x['AMC']),"UCC":str(formdata['UCC']),"Family":str(formdata['Family']),"Category":str(x['Category']),"ChqNo":str(formdata['ChqNo']),"Amount":str(x['values']),"SchemeCode":str(x['SchemeCode']),"SchemeName":str(x['SchemeName']),"Folio":str(x['Folio']),"OrderNo":"","BuyDate":str(buydate.strftime('%d-%b-%y'))})

	mongo.db.chqueIn.update_one({"UCC":formdata['UCC'],"ChqNo":formdata['ChqNo']} ,{"$set":{"finas":True}},upsert=False)	
	# mongo.db.chqueIn.remove({"ChqNo":str(formdata['ChqNo'])})
	return jsonify({"success":"true","message":"Cheque Assigned Successfully!"})


@app.route("/dishonourcheque",methods=['POST'])
def dishonourcheque():
	formdata = request.get_json()
	print formdata

	print ({"UCC":formdata['UCC'],"ChqNo":formdata['ChqNo'],"Slip":formdata['Slip']})
	mongo.db.chqueIn.update_one({"UCC":str(formdata['UCC']),"ChqNo":str(formdata['ChqNo']),"Slip":str(formdata['Slip'])} ,{"$set":{"dishon":True}},upsert=False)

	for key, value in dict.items(formdata['rejlist']):
		# print value
		mongo.db.daywise.update_one({"OrderNo":value} ,{"$set":{"reject":True}},upsert=False)

	return jsonify({"success":"true","message":"Cheque Dishonoured Successfully!"})

@app.route("/exportexceltoday",methods=['POST'])
def exportexceltoday():
	print "Hello"
	return hello



#Reports Code
@app.route("/generateValuationReport",methods=['POST'])
def generateValuationReport():
	data = request.get_json()

	print data

	if (data.get('ucc') != None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
		print "ucc vali condition"
		result1 = mongo.db.daywise.find({"UCC":data['ucc']['UCC']},{'_id':False})
		result1 = list(result1)
		print result1
		if len(result1):
			for x in result1:
				if x['pnl'] :
					x['pnl'] = round(float(x['pnl']))

		result2 = mongo.db.chqueIn.find({"UCC":data['ucc']['UCC']},{'_id':False})
		result2 = list(result2)
		print result2

		return jsonify({'success':'true','result1':result1,'result2':result2})
	
	elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') == None and data.get('edate') == None):
		print "Family vali condition"
		result1 = mongo.db.daywise.find({"Family":data['family']},{'_id':False})
		result1 = list(result1)
		print result1
		if len(result1):
			for x in result1:
				if x['pnl'] :
					x['pnl'] = round(float(x['pnl']))

		result2 = mongo.db.chqueIn.find({"Family":data['family']},{'_id':False})
		result2 = list(result2)
		print result2

		return jsonify({'success':'true','result1':result1,'result2':result2})
	
	elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') != None and data.get('edate') != None):
		print "ucc with date vali condition"
	elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') != None and data.get('edate') != None):
		print "Family with date vali condition"
	else:
		return jsonify({'success':'false','message':'Not valid combination'})

@app.route("/generateAUMReport", methods=['POST'])
def generateAUMReport():
	data = request.get_json()
	finaumlist = []
	amount = {}
	amount2 = []

	# print data

	if data.get('type') == None:
		return jsonify({'success':'false','message':'Please select Report Type!'})
	#AMC Wise AUM Report
	if data['type'] == 'amc':
		#if none selected
		if (data.get('ucc') == None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
			# print 'all'
			amcltpdata = mongo.db.amcs.find({},{'_id':False,'AMC':True,'SchemeName':True,'NAV':True})
			amcltpdata = list(amcltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({},{'_id':False,'AMC':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['AMC']) == None:
						amount[x['AMC']] = {'AMC':x['AMC'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['AMC']) != None:
						amount[x['AMC']]['amount'] += round(float(x['Amount']))
						for y in amcltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['AMC']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["AMC","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})
		
		#else if ucc is selected but date is not AMC report
		elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
			# print 'amc chi ucc vali condition'
			amcltpdata = mongo.db.amcs.find({},{'_id':False,'AMC':True,'SchemeName':True,'NAV':True})
			amcltpdata = list(amcltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'UCC':data['ucc']['UCC']},{'_id':False,'AMC':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['AMC']) == None:
						amount[x['AMC']] = {'AMC':x['AMC'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['AMC']) != None:
						amount[x['AMC']]['amount'] += round(float(x['Amount']))
						for y in amcltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['AMC']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["AMC","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if family is selected and date is not AMC report
		elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') == None and data.get('edate') == None):
			# print 'amc chi family valid condition'
			amcltpdata = mongo.db.amcs.find({},{'_id':False,'AMC':True,'SchemeName':True,'NAV':True})
			amcltpdata = list(amcltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'Family':data['family']},{'_id':False,'AMC':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['AMC']) == None:
						amount[x['AMC']] = {'AMC':x['AMC'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['AMC']) != None:
						amount[x['AMC']]['amount'] += round(float(x['Amount']))
						for y in amcltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['AMC']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["AMC","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})
		
		#else if ucc and date is selected AMC report
		elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') != None and data.get('edate') != None):
			# print "amc chi ucc with date vali condition"
			amcltpdata = mongo.db.amcs.find({},{'_id':False,'AMC':True,'SchemeName':True,'NAV':True})
			amcltpdata = list(amcltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'UCC':data['ucc']['UCC']},{'_id':False,'AMC':True,'Date':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			for i in daywiseaumdata:
				a = datetime.strptime(i['Date'], '%d-%b-%y')
				b = datetime.strptime(data['sdate'], '%Y-%m-%d')
				c = datetime.strptime(data['edate'], '%Y-%m-%d')
				
				if a > b and a < c:
					# print a
					# print i
					finaumlist.append(i)
			# print finaumlist

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['AMC']) == None:
						amount[x['AMC']] = {'AMC':x['AMC'],'amount':0,'newamount':0}

				# print amount
				
				for x in finaumlist:
					# print x['AMC']
					if amount.get(x['AMC']) != None:
						amount[x['AMC']]['amount'] += round(float(x['Amount']))
						for y in amcltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['AMC']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["AMC","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if family and date is selected AMC report
		elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') != None and data.get('edate') != None):
			amcltpdata = mongo.db.amcs.find({},{'_id':False,'AMC':True,'SchemeName':True,'NAV':True})
			amcltpdata = list(amcltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'Family':data['family']},{'_id':False,'AMC':True,'Date':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			for i in daywiseaumdata:
				a = datetime.strptime(i['Date'], '%d-%b-%y')
				b = datetime.strptime(data['sdate'], '%Y-%m-%d')
				c = datetime.strptime(data['edate'], '%Y-%m-%d')
				
				if a > b and a < c:
					print a
					print i
					finaumlist.append(i)

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['AMC']) == None:
						amount[x['AMC']] = {'AMC':x['AMC'],'amount':0,'newamount':0}

				# print amount
				
				for x in finaumlist:
					# print x['AMC']
					if amount.get(x['AMC']) != None:
						amount[x['AMC']]['amount'] += round(float(x['Amount']))
						for y in amcltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['AMC']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["AMC","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})
		else:
			return jsonify({'success':'false','message':'Wrong combination!'})
	
	#SchemeWise AUM Report
	elif data['type'] == 'scheme':
		#if none is selected SchemeWise
		if (data.get('ucc') == None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
			schemeltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'NAV':True})
			schemeltpdata = list(schemeltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({},{'_id':False,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['SchemeName']) == None:
						amount[x['SchemeName']] = {'SchemeName':x['SchemeName'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['SchemeName']) != None:
						amount[x['SchemeName']]['amount'] += round(float(x['Amount']))
						for y in schemeltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['SchemeName']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["SchemeName","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if ucc is selected SchemeWise
		elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
			# print 'amc chi ucc vali condition'
			schemeltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'NAV':True})
			schemeltpdata = list(schemeltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'UCC':data['ucc']['UCC']},{'_id':False,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['SchemeName']) == None:
						amount[x['SchemeName']] = {'SchemeName':x['SchemeName'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['SchemeName']) != None:
						amount[x['SchemeName']]['amount'] += round(float(x['Amount']))
						for y in schemeltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['SchemeName']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["SchemeName","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if Family is selected SchemeWise
		elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') == None and data.get('edate') == None):
			print 'amc chi family valid condition'
			schemeltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'NAV':True})
			schemeltpdata = list(schemeltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'Family':data['family']},{'_id':False,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['SchemeName']) == None:
						amount[x['SchemeName']] = {'SchemeName':x['SchemeName'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['SchemeName']) != None:
						amount[x['SchemeName']]['amount'] += round(float(x['Amount']))
						for y in schemeltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['SchemeName']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["SchemeName","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if ucc and date is selected SchemeWise
		elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') != None and data.get('edate') != None):
			schemeltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'NAV':True})
			schemeltpdata = list(schemeltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'UCC':data['ucc']['UCC']},{'_id':False,'Date':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			for i in daywiseaumdata:
				a = datetime.strptime(i['Date'], '%d-%b-%y')
				b = datetime.strptime(data['sdate'], '%Y-%m-%d')
				c = datetime.strptime(data['edate'], '%Y-%m-%d')
				
				if a > b and a < c:
					# print a
					# print i
					finaumlist.append(i)

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['SchemeName']) == None:
						amount[x['SchemeName']] = {'SchemeName':x['SchemeName'],'amount':0,'newamount':0}

				# print amount
				
				for x in finaumlist:
					# print x['AMC']
					if amount.get(x['SchemeName']) != None:
						amount[x['SchemeName']]['amount'] += round(float(x['Amount']))
						for y in schemeltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['SchemeName']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["SchemeName","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if family and date is selected SchemeWise
		elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') != None and data.get('edate') != None):
			
			schemeltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'NAV':True})
			schemeltpdata = list(schemeltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'Family':data['family']},{'_id':False,'Date':True,'SchemeName':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			for i in daywiseaumdata:
				a = datetime.strptime(i['Date'], '%d-%b-%y')
				b = datetime.strptime(data['sdate'], '%Y-%m-%d')
				c = datetime.strptime(data['edate'], '%Y-%m-%d')
				
				if a > b and a < c:
					# print a
					# print i
					finaumlist.append(i)

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['SchemeName']) == None:
						amount[x['SchemeName']] = {'SchemeName':x['SchemeName'],'amount':0,'newamount':0}

				# print amount
				
				for x in finaumlist:
					# print x['AMC']
					if amount.get(x['SchemeName']) != None:
						amount[x['SchemeName']]['amount'] += round(float(x['Amount']))
						for y in schemeltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['SchemeName']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["SchemeName","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		else:
			return jsonify({'success':'false','message':'Wrong combination!'})
	
	#Category Wise AUM Report
	elif data['type'] == 'category':
		#if none is selected
		if (data.get('ucc') == None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
			catltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'Category':True,'NAV':True})
			catltpdata = list(catltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({},{'_id':False,'SchemeName':True,'Date':True,'Category':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['Category']) == None:
						amount[x['Category']] = {'Category':x['Category'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['Category']) != None:
						amount[x['Category']]['amount'] += round(float(x['Amount']))
						for y in catltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['Category']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["Category","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if ucc is selected categorywise
		elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') == None and data.get('edate') == None):
			# print 'amc chi ucc vali condition'
			catltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'Category':True,'NAV':True})
			catltpdata = list(catltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'UCC':data['ucc']['UCC']},{'_id':False,'SchemeName':True,'Date':True,'Category':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['Category']) == None:
						amount[x['Category']] = {'Category':x['Category'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['Category']) != None:
						amount[x['Category']]['amount'] += round(float(x['Amount']))
						for y in catltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['Category']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["Category","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if family is selected categorywise
		elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') == None and data.get('edate') == None):
			# print 'cat chi family valid condition'
			catltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'Category':True,'NAV':True})
			catltpdata = list(catltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'Family':data['family']},{'_id':False,'SchemeName':True,'Date':True,'Category':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['Category']) == None:
						amount[x['Category']] = {'Category':x['Category'],'amount':0,'newamount':0}

				# print amount
				
				for x in daywiseaumdata:
					# print x['AMC']
					if amount.get(x['Category']) != None:
						amount[x['Category']]['amount'] += round(float(x['Amount']))
						for y in catltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['Category']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["Category","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if ucc and date is selected Category wise
		elif (data.get('ucc') != None and data.get('family') == None and data.get('sdate') != None and data.get('edate') != None):
			catltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'Category':True,'NAV':True})
			catltpdata = list(catltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'UCC':data['ucc']['UCC']},{'_id':False,'SchemeName':True,'Date':True,'Category':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			for i in daywiseaumdata:
				a = datetime.strptime(i['Date'], '%d-%b-%y')
				b = datetime.strptime(data['sdate'], '%Y-%m-%d')
				c = datetime.strptime(data['edate'], '%Y-%m-%d')
				
				if a > b and a < c:
					# print a
					# print i
					finaumlist.append(i)


			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['Category']) == None:
						amount[x['Category']] = {'Category':x['Category'],'amount':0,'newamount':0}

				# print amount
				
				for x in finaumlist:
					# print x['AMC']
					if amount.get(x['Category']) != None:
						amount[x['Category']]['amount'] += round(float(x['Amount']))
						for y in catltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['Category']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["Category","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})

		#else if family and daye is selected categorywise
		elif (data.get('ucc') == None and data.get('family') != None and data.get('sdate') != None and data.get('edate') != None):
			catltpdata = mongo.db.amcs.find({},{'_id':False,'SchemeName':True,'Category':True,'NAV':True})
			catltpdata = list(catltpdata)
			# print amcltpdata
			daywiseaumdata = mongo.db.daywise.find({'Family':data['family']},{'_id':False,'SchemeName':True,'Date':True,'Category':True,'Amount':True,'Units':True})
			daywiseaumdata = list(daywiseaumdata)
			# print daywiseaumdata

			for i in daywiseaumdata:
				a = datetime.strptime(i['Date'], '%d-%b-%y')
				b = datetime.strptime(data['sdate'], '%Y-%m-%d')
				c = datetime.strptime(data['edate'], '%Y-%m-%d')
				
				if a > b and a < c:
					# print a
					# print i
					finaumlist.append(i)


			if (daywiseaumdata):
				for x in daywiseaumdata:
					if amount.get(x['Category']) == None:
						amount[x['Category']] = {'Category':x['Category'],'amount':0,'newamount':0}

				# print amount
				
				for x in finaumlist:
					# print x['AMC']
					if amount.get(x['Category']) != None:
						amount[x['Category']]['amount'] += round(float(x['Amount']))
						for y in catltpdata:
							if y['SchemeName'] == x['SchemeName']:
								amount[x['Category']]['newamount'] += round(float(x['Units'])*float(y['NAV']))
				
				for key, value in amount.iteritems():
					amount2.append(value)

				# print amount2
				# print amount
				headaum = ["Category","InvestedAmt","Valuation"]
				return jsonify({'success':'true','aumrep':amount2,'headaum':headaum})
		else:
			return jsonify({'success':'false','message':'Wrong combination!'})

	return jsonify({'success':'true'})

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port=9876, threaded=True)