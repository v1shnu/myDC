#!C:\Python26\python.exe -u

mysql_hostname = '127.0.0.1'
mysql_username = 'user';
mysql_password = 'password'
mysql_database = 'verlihub'

banned_nicks = []
banned_nicks.extend(['fuck','ass','dick','choot','land','penis','rape','bur','balatkar','chood','madar','beti','bhosar','bharwa','porn','p0rn','sex','nude','naked','osha','tera','gandu','0SHA','hinduja','debjit','saha','chod'])
banned_nicks.extend(['Anonymous','dchub','dcadmin','sheriffbot','sherifbot','ntweat','applegrew', 'dchub','himanshu','ojha','abc','adimania','pratyush','verma','VacuumHead','khajjal_VacuumHead','Vinit','kumar','DJ','Vishnu','SourceCode','Kaustubh','Karkare'])
category = ["Applications / Programs","Development Tools / OS","EBooks / Comics","Games / Fun","Miscellaneous / Random","Movies / Documentaries","Music / Songs","Studies / Useless Stuff","Television / Anime"]
founders = ['SourceCode','DJ']
verlihub_logfile = "/home/kaustubh/vh.log"
default_page_size = 5
default_motd_size = 5
# The following 2 files should have the permissions 777 so that www-data can modify it.
verlihub_content = "/etc/verlihub/motd"
verlihub_notice = "/etc/verlihub/motd_reg"

import cgi, copy, hashlib, MySQLdb, os, re, sys, time, urllib

class class_mysql:
	def __init__(self):
		"Connect to the MySQL Server using the details provided and create a Cursor."
		global mysql_hostname, mysql_username, mysql_password, mysql_database
		self.error = False
		try: self.link = MySQLdb.connect(mysql_hostname,mysql_username,mysql_password,mysql_database);
		except: self.error = True
		try: self.cursor = self.link.cursor(MySQLdb.cursors.DictCursor);
		except: self.error = True
	def __del__(self):
		"Disconnect from server."
		try: self.cursor.close()
		except: self.error = True
		try: self.link.close()
		except: self.error = True
	def query(self,text):
		try:
			self.cursor.execute(text)
			return self.cursor.fetchall()
		except:
			self.error = True
			return None
	def value(self,text):
		"Uses query() to obtain results and returns only the value at the first column from the first row."
		data = self.query(text)
		if data==None or len(data)==0 : return None;
		else: return data[0][ data[0].keys()[0] ]



class class_http:
	
	def __init__(self):
		# Define Class Constansts
		self.session_table = "sessions" # This is the name of the table in the database which will be used to store session data
		self.session_timeout = 5*60 # This is the amount of time in seconds for which session data is considered valid
		try: self.script = "http://"+os.environ["SERVER_NAME"]+os.environ["SCRIPT_NAME"]
		except: self.script = None
		# Load GET, POST, ENV variables
		self.get = dict()
		self.post = dict()
		self.env = os.environ
		# Load form data into the GET or POST dictionaries, whichever is appropriate
		form = cgi.FieldStorage()
		for key in form:
			if type(form[key]) is list: continue
			if urllib.urlencode({key:form[key].value}) in self.env["QUERY_STRING"]:
				self.get[key]=form[key].value
			else: self.post[key]=form[key].value
		# Load session and cookie variables
		self.cookie = dict()
		self.pysessid = None # Initially assume session ID is not available
		sql.query("DELETE FROM "+self.session_table+" WHERE expire<"+str(int(time.time()))); # Delete all old session data
		try: # try-catch is for the case when http_cookie doesnt exist
			for pair in self.env["HTTP_COOKIE"].split("; "): # Load cookies
				key, value = pair.split("=")
				self.cookie[key] = value
				if key=="pysessid": self.pysessid = value # Try to locate session ID in cookies
		except: pass
		self._cookie = copy.deepcopy(self.cookie) # Create backup of cookies
		if self.pysessid==None: # If no session ID found in cookies, create one
			x = str(int(time.time()))
			try: x+=self.env["HTTP_USER_AGENT"]
			except: pass
			try: x+=self.env["REMOTE_ADDR"]
			except: pass
			self.pysessid = hashlib.md5(x).hexdigest()
			self.cookie["pysessid"] = self.pysessid
		# Load session data
		temp = sql.value("SELECT data FROM "+self.session_table+" WHERE pysessid=\""+self.pysessid+"\"")
		self.session = {}
		if temp is not None :
			self.session = eval(str(temp).replace("\n","\\n"))
	
	def __del__(self):
		# Save updated session data into database
		if sql.value("SELECT count(*) FROM "+self.session_table+" WHERE pysessid=\""+self.pysessid+"\"")==0:
			sql.query("INSERT INTO "+self.session_table+" (pysessid,data,expire) VALUES (\""+self.pysessid+"\",\""+str(self.session).replace("\"","\\\"")+"\","+str(int(time.time())+self.session_timeout)+")")
		else: sql.query("UPDATE "+self.session_table+" SET data=\""+str(self.session).replace("\"","\\\"")+"\", expire="+str(int(time.time())+self.session_timeout)+" WHERE pysessid=\""+self.pysessid+"\"")
	
	def headers(self):
		data="Content-type: text/html\n"
		# Write cookies
		for key in self.cookie:
			if key not in self._cookie or self.cookie[key]!=self._cookie[key]:
				data+="Set-Cookie: "+key+"="+self.cookie[key].replace("\n","\\n")+"\n"
		data+="\n"
		return data
		
	def redirect(self, address=None):
		# Default redirect to HTTP_REFERER or else self
		if address==None:
			try: address = self.env["HTTP_REFERER"]
			except: address = self.script
		address = str(address).replace("\'","\\'")
		data="Content-type: text/html\n"
		# Write cookies
		for key in self.cookie:
			if key not in self._cookie or self.cookie[key]!=self._cookie[key]:
				data+="Set-Cookie: "+key+"="+self.cookie[key].replace("\n","\\n")+"\n"
		data+="Location: "+address+"\n\n"
		return data



class class_user:
	
	def __init__(self,nick=None):
		# Class Constants
		self.table = "reglist"
		self.columns = ["nick","class","pwd_crypt","login_pwd","login_ip","reg_date","reg_op","email","name","roll","branch","sec_q","sec_a"]
		# If nick is left empty, do nothing
		if nick==None or nick=="":
			self.data = None; self._data = None;
			return
		# If nick is specified, load data from the database
		self.data = sql.query("SELECT "+",".join(self.columns)+" FROM "+self.table+" WHERE nick='"+nick+"'")
		# If nick was not found in the database, do nothing
		if self.data==None or len(self.data)==0 :
			self.data = None; self._data = None;
		# If nick was found in database, load data and create a backup for later comparison so that updates can be appropriately made
		else:
			self.data = self.data[0]
			self._data = copy.deepcopy(self.data)
	
	def __del__(self):
		# If backup data doesnt exist, dont do anything
		if self.data==None or self._data==None: return
		# Compare each item from current data with original data
		set = []
		for key in self._data:
			if self._data[key]!=self.data[key]:
				if type(self._data[key]) is str:
					set.append( key+"=\""+self.data[key].replace("\"","\\\"")+"\"" )
				if type(self._data[key]) in (int,long,float):
					set.append( key+"="+str(self.data[key]) )
		# Update changes in database
		if len(set)>0:
			set = ", ".join(set)
			sql.query("UPDATE "+self.table+" SET "+set+" WHERE nick='"+self._data["nick"]+"'")
	
	def register(self):
		# Set specific post data
		http.post["pwd_crypt"]=0
		http.post["class"]=1
		http.post["reg_date"]=int(time.time())
		http.post["reg_op"]="web3"
		http.post["login_ip"]=http.env["REMOTE_ADDR"]
		# Form Validation
		if http.post["login_pwd1"]!=http.post["login_pwd2"]:
			http.session["error"].append("Registeration Error : Password Mismatch.")
			return self
		elif http.post["login_pwd1"]=="":
			http.session["error"].append("Registeration Error : Password Empty.")
			return self
		else: http.post["login_pwd"] = http.post["login_pwd1"]
		# Load data from post variables
		k = 0
		self.data = {}
		for i in self.columns:
			try: self.data[i] = http.post[i]
			except KeyError as (errstr):
				http.session["error"].append("Registeration Error : Data field '"+j+"' unavailable.")
				k = 1
		if k==1: return self
		# Check non-alphanumeric characters in nick
		if re.search("A-Za-z0-9_",self.data["nick"])!=None:
			http.session["error"].append("Registeration Error : Invalid characters in nickname.")
			return self
		if len(self.data["nick"])<3 or len(self.data["nick"])>30:
			http.session["error"].append("Registeration Error : Nickname too short/long.")
			return self
		# Check for banned nicks
		global banned_nicks
		for x in banned_nicks:
			if self.data["nick"].find(x)>-1:
				http.session["error"].append("Registeration Error : Specified nickname contains a banned/reserved term.")
				return self
		# Confirm that the nickname doesnt already exist in the database
		if sql.value("SELECT count(*) FROM "+self.table+" WHERE nick=\""+self.data["nick"]+"\"")>0:
			http.session["error"].append("Registeration Error : The nickname you specified is already taken.")
			return self
		# Check that there are only two nicks per IP Address
		if sql.value("SELECT count(*) FROM "+self.table+" WHERE login_ip=\""+http.env["REMOTE_ADDR"]+"\"")>=2:
			http.session["error"].append("Registeration Error : Two nicknames have already been registered from this IP Address.")
			return self
		# Insert data into database
		col = []; val = [];
		for i in self.columns:
			col.append(i)
			k = self.data[i]
			if type(k) is str:
				val.append("\""+k.replace("\"","\\\"")+"\"")
			if type(k) in (int,long,float):
				val.append(str(k))
		sql.query("INSERT INTO "+self.table+" ("+",".join(col)+") VALUES ("+",".join(val)+")")
		# Create backups of data to track changes.
		self._data = copy.deepcopy(self.data)
		http.session["message"].append("Registeration Successful : You may now login using the details you provided.")
		return self
	
	def login(self,password):
		# Requires POST variables : nickname, password
		if self.data is None:
			http.session["error"].append("Login Error : Could not find specified nickname in database.")
		elif self.data["pwd_crypt"]!=0: # If registerations are done using a one of the other method (and not this website), the password is stored in an encrypted form and hence cannot be used here.
			http.session["error"].append("Login Error : Password currently encrypted. Please reset it.")
		elif self.data["login_pwd"]!=password:
			http.session["error"].append("Login Error : Password Mismatch")
		elif False and self.data["login_ip"]!=http.env["REMOTE_ADDR"]:
			http.session["error"].append("Login Error : IP Address Mismatch")
		else:
			http.session["current"]=self.data
			http.session["message"].append("You have successfully logged into MyDC.")
		return self
	
	def logout(self):
		# Doesnt require loading of user data
		http.session["current"]={"nick":"Anonymous","class":0}
		http.session["message"].append("You have logged out of MyDC.")
		return self
	
	def password_update(self,pass0,pass1,pass2):
		if self.data["login_pwd"]!=pass0: http.session["error"].append("Password Updation Error : Current password incorrect.")
		elif pass1!=pass2: http.session["error"].append("Password Updation Error : New password mismatch.")
		else:
			self.data["login_pwd"] = http.post["pass1"]
			http.session["message"].append("Your password has been successfully updated.")
		return self
	
	def password_reset(self,email,sec_a):
		if self.data==None: http.session["error"].append("Password Reset Error : Nickname not found in database.")
		elif str(sec_a)=="None": http.session["error"].append("Password Reset Error : Security Answer cannot be None.")
		elif http.env["REMOTE_ADDR"]!=self.data["login_ip"]:
			http.session["error"].append("Password Reset Error : YOur IP Address does not match that which is stored in the database.")
		elif self.data["email"]!=email or self.data["sec_a"]!=sec_a:
			http.session["error"].append("Password Reset Error : Your answers do not match those stored in the database.")
		else:
			password = hashlib.md5(http.pysessid+str(time.time())).hexdigest()[::2]
			self.data["login_pwd"] = password
			http.session["message"].append("Your password has been reset to '"+password+"'. Please change it immediately.")
		return self
	
	def delete(self):
		if self.data==None or type(self.data["nick"]) is not int: return self
		sql.query("DELETE FROM "+self.table+" WHERE nick=\""+str(self.data["nick"])+"\"")
		self._data = None; self.data = None;
		http.session["message"].append("User Account (Nickname : "+self.data["nick"]+") Deletion Successful")
		return self



class class_content():
	
	def __init__(self,id=None):
		# Define class constants
		self.table = "content"
		self.columns = ["id","timex","nick","content","category","magnet","likex"]
		# Do nothing if there is no ID
		if type(id) not in (int,long):
			self.data = None; self._data = None;
			return
		# Load content data
		self.data = sql.query("SELECT "+",".join(self.columns)+" FROM "+self.table+" WHERE id="+str(id))
		if self.data is None or len(self.data)==0:
			self.data = None; self._data = None;
			return
		self.data = self.data[0]
		# Create backup
		self._data = copy.deepcopy(self.data)
	
	def __del__(self):
		# Save updated data into database
		if self.data==None or self._data==None: return
		set = []
		for key in self._data:
			if self._data[key]!=self.data[key]:
				if type(self.data[key]) is str: set.append(key+"=\""+self.data[key]+"\"");
				if type(self.data[key]) in (int,long,float): set.append(key+"="+self.data[key]);
		if len(set)>0: sql.query("UPDATE "+self.table+" SET "+",".join(set)+" WHERE id="+str(self._data["id"]))
		
	def create(self):
		global category
		http.post["timex"] = int(time.time()) # submission time
		http.post["likex"] = "" # initially no likes
		http.post["nick"] = http.session["current"]["nick"]
		try: http.post["category"] = int(http.post["category"])
		except:
			http.session["error"].append("Content Submission Error : Invalid Category.")
			return self
		# Load data from POST variables
		k=0
		self.data = {}
		for key in self.columns:
			if key in ['id','magnet']: continue
			try: self.data[key] = http.post[key]
			except KeyError as (errstr):
				http.session["error"].append("Content Submission Error : Data field '"+key+"' unavailable.")
				k = 1
		try: self.data["magnet"] = http.post["magnet"]
		except: pass
		if k==1: return self
		# Save data into database
		col = []; val = [];
		for key in self.data:
			if key=='id': continue
			col.append(key)
			if type(self.data[key]) is str: val.append("\""+self.data[key]+"\"")
			if type(self.data[key]) in (int,long,float): val.append(str(self.data[key]))
		sql.query("INSERT INTO "+self.table+" ("+",".join(col)+") VALUES ("+",".join(val)+")")
		# Save backup of data
		self._data = copy.deepcopy(self.data)
		http.session["message"].append("Content Submission Successful.")
		http.env["HTTP_REFERER"] = re.sub("&?offset=[^&]","",http.env["HTTP_REFERER"])
		return self

	def like(self,nick,add):
		if self.data==None: return self # Data not loaded
		if self.data["likex"] is None: x = [] # Empty Cell
		else: x = self.data["likex"].split()
		if add and nick not in x:
			x.append(nick)
		if not add:
			try: x.remove(http.session["current"]["nick"])
			except ValueError: pass
		self.data["likex"] = " ".join(x)
		return self
		
	def liked(self):
		if self.data==None: return False # Data not loaded
		return http.session["current"]["nick"] in self.data["likex"].split()
		
	def delete(self):
		if self.data is None or type(self.data["nick"]) is not str: return self
		if self.data["nick"] != http.session["current"]["nick"] and not mydc.auth(5):
			http.session["error"].append("Content Deletion Error : You are not authorized to perform this action.")
		sql.query("DELETE FROM "+self.table+" WHERE id="+str(self.data["id"]))
		x = str(self.data["id"]); self._data = None; self.data = None;
		http.session["message"].append("Content Deletion Successful")
		return self
		


class class_mydc:
	
	def __init__(self):
		# Set session variables to defaults, if reqd
		try: http.session["current"]
		except: http.session["current"]={"nick":"Anonymous","class":0}
		try: http.session["message"]
		except: http.session["message"]=[]
		try: http.session["error"]
		except: http.session["error"]=[]
	
	def action(self,a):
		try:
			if a=="account_login": class_user(http.post["nick"]).login(http.post["pass0"]);
			if a=="account_logout": class_user().logout()
			if a=="password_reset": class_user(http.post["nick"]).password_reset(http.post["email"], http.post["sec_a"])
			if a=="account_register": class_user().register()
			if mydc.auth(1):
				if a=="password_update": class_user(http.session["current"]["nick"]).password_update(http.post["pass0"], http.post["pass1"], http.post["pass2"])
				if a=="content_create":
					class_content().create();
					self.motd_update_content()
				if a=="content_like": class_content(int(http.get["id"])).like(http.session["current"]["nick"],True);
				if a=="content_unlike": class_content(int(http.get["id"])).like(http.session["current"]["nick"],False);
				if a=="content_delete":
					class_content(int(http.get["id"])).delete()
					self.motd_update_content()
			if mydc.auth(5):
				if a=="account_delete": class_user(http.post["nick"]).delete()
				if a=="motd_update_content": self.motd_update_content()
				if a=="motd_update_notice": self.motd_update_notice()
		except KeyError as (errstr):
			http.session["error"].append("Error : Insufficient Data")

	def content(self):
		# Load Filters
		global default_page_size
		try: term = http.get["term"]
		except: term = None
		try: cat = int(http.get["category"])
		except: cat = None
		try: offset = int(http.get["offset"])
		except: offset = 0
		try: size = int(http.get["size"])
		except: size = default_page_size
		try: sort = int(http.get["sort"])
		except: sort = 0
		# Get content IDs
		condition = []
		if sort==0: order = " id DESC "
		else: order = " ((SELECT CHARACTER_LENGTH(likex)-CHARACTER_LENGTH(REPLACE(likex,' ','')) FROM DUAL)+IF(likex='',0,1)-(SELECT count(*) FROM content WHERE id>x.id)) DESC , id ASC "
		if term is not None: condition.append("content LIKE \"%"+term.replace("\"","\\\"")+"%\"")
		if cat is not None: condition.append("category="+str(cat))
		if len(condition)>0: condition = " WHERE "+" AND ".join(condition)
		else: condition = ""
		x = sql.query("SELECT id FROM content x "+condition+" ORDER BY "+order+" LIMIT "+str(offset)+","+str(size))
		y = [];
		for i in x: y.append(i["id"])
		# Get links to be used while displaying the stream
		x = sql.value("SELECT count(*) FROM content x "+condition+" ORDER BY "+order)
		z = {};
		z["first"] = re.sub("&?offset=[^&]*","",http.env["QUERY_STRING"])+"&offset=0"
		z["last"] = re.sub("&?offset=[^&]*","",http.env["QUERY_STRING"])+"&offset="+str(x-size)
		if offset>0: z["prev"] = re.sub("&?offset=[^&]*","",http.env["QUERY_STRING"])+"&offset="+str(max(0,offset-size))
		else: z["prev"]="#"
		if offset+size<x: z["next"] = re.sub("&?offset=[^&]*","",http.env["QUERY_STRING"])+"&offset="+str(offset+size)
		else: z["next"]="#"
		z["category"] = re.sub("&?category=[^&]*","",http.env["QUERY_STRING"])+"&category="
		z["term"] = re.sub("&?term=[^&]*","",http.env["QUERY_STRING"])+"&term="
		z["sort"] = re.sub("&?sort=[^&]*","",http.env["QUERY_STRING"])+"&sort="
		for i in z: z[i] = re.sub("^\?#","#",re.sub("^\?&","?","?"+z[i]))
		return z,y
	
	def users(self):
		return sql.query("SELECT nick,class,login_ip FROM reglist ORDER BY login_ip")

	def motd_display_notice(self):
		f = open(verlihub_notice,"r")
		x = f.read()
		f.close()
		return x

	def motd_update_notice(self):
		f = open(verlihub_notice,"w")
		try: f.write(http.post["notice"].replace("\r",""))
		except: pass
		f.close()

	def motd_update_content(self):
		global verlihub_content, category, default_motd_size
		f = open(verlihub_content,"w")
		f.write("\n \n"+"="*60+"\n")
		f.write("                              LATEST CONTENT ON DC HUB\n")
		f.write("="*60+"\n \n")
		x = sql.query("SELECT id FROM content ORDER BY id DESC LIMIT 0,"+str(default_motd_size))
		if x is not None:
			for i in x:
				item = class_content(i["id"])
				if type(item.data["magnet"]) is not str: link = item.data["content"];
				else: link = item.data["magnet"]
				f.write(link+" ("+category[item.data["category"]]+") by "+item.data["nick"]+"\n")
		f.close()

	def auth(self,level):
		# Doesnt require loading of user data
		if http.session["current"]["nick"] in founders: return True; # Founders have complete access
		else: return (http.session["current"]["class"] >= level); # Check normally for rest



class string_buffer:
	def __init__(self):
		self.data = []
	def write(self,line):
		self.data.append(line)
	def contents(self):
		return "".join(self.data)



sql = http = mydc = None
def process(theme):
	# Redirect STDERR
	original_stderr = sys.stderr
	sys.stderr = open("error.log","w")
	# Create dependencies
	global sql, http, mydc
	sql = class_mysql()
	if sql.error:
		print "Content-type: text/plain\n"
		print "Could not connect to database."
		return
	http = class_http()
	mydc = class_mydc()
	# Ensure that the given theme is indeed a class
	if str(type(theme))!="<type 'classobj'>":
		print "Content-type: text/plain\n"
		print "Could not load given theme class."
		return
	# Set Defaults
	default_page = "index"
	if "action" not in http.get.keys() and "display" not in http.get.keys(): http.get["display"]=default_page
	# Main Operations
	if "action" in http.get.keys():
		mydc.action(http.get["action"]) # perform action
		print http.redirect() # Send user back to referring page
	elif "ajax" in http.get.keys() and http.get["ajax"]=="sec_q":
		print "Content-type: text/html\n"
		try:
			x = class_user(http.get["nick"])
			print x.data["sec_q"]
		except: print "Please specify a valid nickname."
	elif "display" in http.get.keys():
		# Redirect STDOUT
		original_stdout = sys.stdout
		sys.stdout = theme_stdout = string_buffer()
		# Combine Messages & Errors
		http.session["message"] = "<br>".join(http.session["message"])
		http.session["error"] = "<br>".join(http.session["error"])
		# Call Theme Functions
		if http.get["display"] not in ["__module__","__main__","__init__","__del__"] and http.get["display"] in dir(theme):
			try: eval(str(theme.__name__)+"()."+http.get["display"])()
			except Exception as e: sys.stderr.write(str(e)+"\n")
		else:
			try: eval(str(theme.__name__)+"()."+default_page)()
			except Exception as e: sys.stderr.write(str(e)+"\n")
		# Reset Messages & Errors
		http.session["message"] = []
		http.session["error"] = []
		# Reset STDOUT
		sys.stdout = original_stdout
		# Print Headers and then Content
		print http.headers()
		print theme_stdout.contents()
		del theme_stdout
	del mydc, http, sql
	# Reset STDERR
	sys.stderr.close()
	sys.stderr = original_stderr

if __name__=="__main__":
	print "Content-type: text/plain\n"
	print "This module does not contain a theme."

