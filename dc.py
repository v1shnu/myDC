#!C:\Python26\python.exe -u

import dchub, datetime, re, os;

class theme():
	"Theme for MyDC by DJ"
	
	def __init__(self): # Header images + Menu [Written by DJ]
		
		print '''
<head>
	<link rel="shortcut icon" href="/favicon.jpg">
	<link href="style.css" rel="stylesheet" type="text/css" />
	<script src="./images/jquery.js" type="text/javascript"></script>
</head>
<body>
<div id="header_wrapper">
	<div id="header">    
    	<div id="site_title">
            <a href="./"></a>
        </div> 
		
		'''
		print '''
		<div id="menu">
            <ul>
                <li><a href="?display=main"'''
		if(dchub.http.get["display"]=="main"): print "class=\"current\""
		print '''>Home</a></li>
				<li><a href="?display=register"'''
		if(dchub.http.get["display"]=="register"): print "class=\"current\""
		print '''>Register</a></li>
                <li><a href="?display=repo"'''
		if(dchub.http.get["display"]=="repo"): print "class=\"current\""
		print '''>Repo</a></li>
                <li><a href="?display=faq" '''
		if(dchub.http.get["display"]=="FAQ"): print "class=\"current\""
		print '''>FAQ</a></li>
				<li><a href="/acm">ACM</a></li>
				<li><a href="/bitlug">LUG</a></li>
				<li><a href="/music">Music Club</a></li>
            </ul>    	
        </div> <!-- End Of Menu -->'''
	
	def __del__(self): # Complete Sidebar + Footer  [Written by DJ]
		print '''
		<script>window.setTimeout("$('.delayhide').slideUp(500);",4000);</script>
		<div id="sidebar">'''
		if dchub.http.session["message"]:
			print "<div style='text-align:center; width:250px;border:1px groove #395AF9;' class='delayhide'>"+dchub.http.session["message"]+"</div><br>";
		if dchub.http.session["error"]:
			print "<div style='text-align:center; width:250px;border:1px groove #F71B14;' class='delayhide'>"+dchub.http.session["error"]+"</div><br>";
		if dchub.mydc.auth(1):
			print '''<div class="sidebar_box"><h4>Post Content</h4>'''
			global category
			print "<form action='?action=content_create' method='post'><input type=\"text\"  style=\"width:250px;\" placeholder='Content' name='content'><br><select style=\"width:250px;height:32px;\" name='category'>",
			for i in range(len(dchub.category)): print "<option class= value="+str(i)+">"+dchub.category[i]+"</option>",
			print "</select><br><input type=\"text\" style=\"width:250px;\" placeholder='Magnet Link' name='magnet'><br><input class=\"submit_btn float_l\" style='width:96%;font-weight:bold;' value='Post Content' type='submit'></form>"
	
			print '''
			<br>
		</div>
<script>
$(document).ready(function(){

		$("#info").css("display","block");
		$("#newpass").css("display","none");
		$("#changepass").click(function()
		{
			$("#newpass").show("slow");
			$("#info").hide("slow");
		});
		$("#cancelchange").click(function()
		{
			$("#newpass").hide("slow");
			$("#info").show("slow");
		});
		
	  });
</script>
			
			<div class="sidebar_box">
				<h4>Account Settings</h4>
				<div id="info">
				<table style='font-size: 14px;'><colgroup><col width="200" /><col width="200" /></colgroup>
				<tr><td>Nick</td><td>'''+dchub.http.session["current"]["nick"]+'''</td></tr>
				<tr><td>IP Address</td><td>'''+dchub.http.session["current"]["login_ip"]+'''</td></tr>
				<tr><td>Password</td><td><div id="changepass"><button style='width:90%;' class="submit_btn">Click To Change</button></div></td></tr>
				</table>
				<br><form action='?action=account_logout' method='post'><input type='submit' style='width:96%;font-weight:bold;' class=\"submit_btn float_l\" value='Logout'></form><br>				
				</div>
				<div id="newpass">
				<table style='font-size: 14px;'><colgroup><col width="200" /><col width="200" /></colgroup>
				<form action='?action=password_update' method='post'>
				<input type="hidden" name="nick" value=" '''+dchub.http.session["current"]["nick"]+''' ">
				<tr><td>Current Password </td><td><input class="field" type="password" maxlength="30"  placeholder='**********'name="pass0"/></td></tr>
				<tr><td>New Password </td><td><input class="field" type="password" maxlength="30"  placeholder='**********'name="pass1"/></td></tr>
				<tr><td>Re-Enter Password </td><td><input class="field" type="password" maxlength="30"  placeholder='**********'name="pass2"/></td></tr>
				<tr><td><div id="cancelchange"><input type="button" onclick="" style='width:90%;' class="submit_btn" value="Cancel" /></div></td><td><input type="submit" class="submit_btn" style='width:90%;	font-weight:bold;' value="Update Password" class='button' /></td></tr>
				</form>				
				</table>
				</div>
			</div>
			'''
			
		else:
			try: dchub.http.env["REMOTE_ADDR"]
			except: dchub.http.env["REMOTE_ADDR"]="0.0.0.0"
			print '''			
	<div class="sidebar_box">
<script>
		function loadq(){
			$.get("?ajax=sec_q",{"nick":$('#nick').val()},function(data){
				$('#sec_q').html(data);
				})
			}
$(document).ready(function(){

		$("#forgot").css("display","none");
		$("#login").css("display","block");
		$("#for").click(function()
		{
			$("#forgot").show("slow");
			$("#login").hide("slow");
			$('#nick').val('');
			loadq();
		});
		
	  });
</script>
		<div id="login">
		<h4>Login </h4><br>
		<form action='?action=account_login' method='post'>
			<table><colgroup><col width="250" /><col width="150" /></colgroup>
				<tr><td>Nick </td><td><input type="text"  name="nick"/></td></tr>
				<tr><td>Password </td><td><input type="password" name="pass0" style="color: #ccc;
				font-family: Tahoma, Geneva, sans-serif; 
				font-size: 12px; 
				padding: 5px; 
				border: 1px solid #102a61;  
				background: #000; " /></td></tr>
				<tr><td><div id="for"><input type="button" onclick="" style='width:100%;' class="submit_btn" value="Forgot Password?" /></div></td><td><input type="submit" class="submit_btn float_l" style='width:97%;font-weight:bold;' value="Login" class='button' /></td></tr>
			</table>
		</form>
		</div>
		<div id="forgot">
		<h4>Reset Password </h4><br>
		<form action='?action=password_reset' method='post'>
			<table><colgroup><col width="200" /><col width="200" /></colgroup>
				<tr><td>Nick </td><td><input type="text" name="nick" id='nick' onKeyUp='loadq();' onBlur='loadq();' onFocus='loadq();'></td></tr>
				<tr><td>E-Mail </td><td><input type="text" name="email"/></td></tr>
				<tr><td>Security Question</td><td><div id='sec_q'></div></td></tr>
				<tr><td>Security Answer</td><td><input type="text"  name="sec_a" /></td></tr>
				<tr><td></td><td><input type="submit" class="submit_btn float_l" style='width:85%;font-weight:bold;' value="Retrieve Password" class='button' /></td></tr>
				</table>
		</form>
		</div>
		</div>  
		'''
		print '''
	  	
	<div class="sidebar_box">
		<h4>Links</h4>
		<ul class="tmo_list">'''
		if dchub.mydc.auth(5): print "<li><a href=\"?display=adminconsole\">Admin Console</a></li>"
		
		print '''
			<li><a href="?display=main">Home</a></li>
			<li><a href="?display=register">Register</a></li>
			<li><a href="?display=repo">Repo</a></li>
			<li><a href="?display=faq">FAQ</a></li>
			<li><a href="/acm">ACM</a></li>
			<li><a href="/bitlug">Linux User Group</a></li>
			<li><a href="/music">Music Club</a></li>
		</ul>
	</div>
            

</div>
<div class="cleaner"></div>
</div> <!-- end of main -->
</div> <!-- end of main wrapper -->

<div id="footer_wrapper">
	<div id="footer">
        
    	<div class="footer_col_w300">
            <h4>Sitemap</h4>
				<ul class="tmo_list">
					<li><a href="?display=main">Home</a></li>
					<li><a href="?display=register">Register</a></li>
					<li><a href="?display=repo">Repo</a></li>
					<li><a href="?display=faq">FAQ</a></li>
				</ul>          
        </div>
        
        <div class="footer_col_w300">
            <h4>Links</h4>
            	<ul class="tmo_list">
					<li><a href="/acm">ACM</a></li>
					<li><a href="/bitlug">Linux User Group</a></li>
					<li><a href="/music">Music Club</a></li>
				</ul>         
        </div>
        
        <div class="footer_col_w300 last">
            <h4>Admins</h4>
			<p>2k8 : khajjal_VaccuumHead | Machinist | Volvo<br>2k9 : DJ | SourceCode</p>
            <p>Copyleft 2011 : <a href="http://192.168.154.51">SourceCode</a> | <a href="http://192.168.153.32">DJ</a></p>        
        </div>
    
		<div class="cleaner"></div>
    </div> <!-- end of templatemo_footer -->
</div> <!-- end of templatemo_footer wrapper -->

</body>
</html>
'''

	def index(self): # Home page with Search Box + Latest Content [Written by : DJ]
		print '''
		<title>Welcome to MyDC</title>
    </div> <!-- end of header -->
</div> <!-- end of header wrapper -->

<div id="main_wrapper">
	<div id="main">
    
    	<div id="content">
		<h4>Latest Content</h4>'''
		# Latest Content Streams
		links, content_ids = dchub.mydc.content()
		try: cat = dchub.http.get["category"]
		except: cat = 'None'
		try: term = dchub.http.get["term"]
		except: term = ""
		try:
			sort = int(dchub.http.get["sort"])
			if sort not in (0,1): sort=1
		except: sort = 0
		print "<select id='categoryselect' onChange=\"window.location='"+links["category"]+"'+this.value;\"><option value='None'>All Categories</option>"
		for i in range(len(dchub.category)):
			print "<option value="+str(i)+">"+dchub.category[i]+"</option>",
		print "</select> <input type='text' id='searchterm' size=15 placeholder='Search' value='"+term+"' onKeyPress=\"if(event.keyCode==13) window.location = '"+links["term"]+"'+this.value; \">",
		print "<a href='"+links["first"]+"'><input type='button' class=\"field\" value='First'></a>",
		print "<a href='"+links["prev"]+"'><input type='button' class=\"field\" value='Previous'></a>",
		print "<a href='"+links["next"]+"'><input type='button' class=\"field\" value='Next'></a>"
		print "<a href='"+links["last"]+"'><input type='button' class=\"field\" value='Last'></a>",
		print "<select id='sortselect' onChange=\"window.location='"+links["sort"]+"'+this.value;\"><option value=0 selected=\"selected\">Sort By Time</option><option value=1>Sort By Popularity</option></select>",
		print "<script> document.getElementById('categoryselect').value = '"+cat+"'; document.getElementById('sortselect').value = '"+str(sort)+"'; </script>"
		print "<br><br>"
		print "<table  style='font-size: 14px;text-align:left'><colgroup><col width=\"200\" /><col width=\"170\" /><col width=\"100\" /><col width=\"50\" /><col width=\"50\" /></colgroup><tr><th>Content</th><th>Category</th><th>Nickname</th><th>Likes</th>"
		if dchub.mydc.auth(1):
			print "<th>Options</th>"
		print "</tr>"
		for content_id in content_ids:
			item = dchub.class_content(content_id)
			likes = item.data["likex"].split()
			t = datetime.datetime.fromtimestamp(int(item.data["timex"])).strftime("%d %b %Y, %H:%M:%S")
			print "<tr title='Date & Time of Submission : "+t+"'>",
			print "<td>"+item.data["content"]+"</td>",
			print "<td>"+dchub.category[item.data["category"]]+"</td>",
			print "<td>"+item.data["nick"]+"</td>",
			print "<td>"+str(len(likes))+"</td>",
			if dchub.mydc.auth(1):
				print "<td>",
				if dchub.http.session["current"]["nick"] not in likes:
					print "<a href='?action=content_like&id="+str(content_id)+"'><input type=\"button\" onclick=\"\" style='width:90%;padding: 0px 0px;' class=\"submit_btn\" value=\"Like\" /></a>",
				else: print "<a href='?action=content_unlike&id="+str(content_id)+"'><input type=\"button\" onclick=\"\" style='width:90%;padding: 0px 0px;' class=\"submit_btn\" value=\"Unlike\" /></a>",
				if dchub.mydc.auth(5) or dchub.http.session["current"]["nick"]==item.data["nick"]:
					print "<a href='?action=content_delete&id="+str(content_id)+"'><input type=\"button\" onclick=\"\" style='width:90%;padding: 0px 0px;' class=\"submit_btn\" value=\"Delete\" /></a>",
				print "</td>",
			else: print "<td></td>",
			print "</tr>"
		print "</table></div>"
		

	def register(self): # Rules + Registration Form [Written by DJ]
		print '''
		"<style>#form input { width:80%; }</style>" 
		
    <title>Register For DC Hub</title>
    </div> <!-- end of header -->
</div> <!-- end of header wrapper -->

<div id="main_wrapper">
	<div id="main">
		<div id="content">
		
<script>
$(document).ready(function(){

		$("#rules").css("display","block");
		$("#form").css("display","none");

		$("#agree").click(function()
		{

			$("#rules").hide("slow");
			$("#form").show("slow");
		});
		
	  });
function validate(){
	if(document.forms["form"].nick.value=="" || document.forms["form"].login_pwd1.value=="" || document.forms["form"].login_pwd2.value=="" || document.forms["form"].name.value==""|| document.forms["form"].no.value==""|| document.forms["form"].branch.value==""|| document.forms["form"].email.value==""|| document.forms["form"].sec_q.value=="NULL"|| document.forms["form"].sec_a.value==""){ alert("One or more empty fields!"); return false; }
	if(document.forms["form"].login_pwd1.value!=document.forms["form"].login_pwd2.value){ alert("Passwords do not match!"); return false; }
var x=document.forms["form"]["email"].value;
var atpos=x.indexOf("@");
var dotpos=x.lastIndexOf(".");
if (atpos<1 || dotpos<atpos+2 || dotpos+2>=x.length)
  {
  alert("Invalid e-mail address");
  return false;
  }
	
	document.forms["form"].roll.value=document.forms["form"].course.value+"/"+document.forms["form"].no.value+"/"+document.forms["form"].year.value;
	return true;
	}
	  
	  
</script>

<div id="rules" style='text-align:justify'>
<h4>Rules</h4>
<li><b>Content</b> : I shall be responsible for all use of this network. In case I own a computer and decide to connect it to BIT Ranchi network, I will be responsible for all the content on it, especially that which I make available to other users. (This provision will also apply to any computer or device for which I am responsible, and is included in the meaning of "my computer".) In case I do not own a computer but am provided some IT resources by BIT Ranchi, I will be held responsible for the content stored in the designated workspace allotted to me (examples: file storage area, web pages, stored/archived emails, on Computer Centre or Department machines).</li>
<li><b>Network</b> : I will be held responsible for all the network traffic generated by "my computer". I understand that network capacity is a limited, shared resource. I agree that physically tampering with network connections/equipments, sending disruptive signals, or making EXCESSIVE USE of network resources is strictly prohibited. Repeated offenses of this type could result in permanent disconnection of network services. I shall not share the network connection beyond my own use and will not act as a forwarder/ masquerader for anyone else.</li>
<li><b>Academic Use</b> : I understand that the IT infrastructure at BIT Ranchi is for academic use and I shall not use it for any commercial purpose or to host data services for other people or groups. Also, I shall not host or broadcast information that might harm others or may be otherwise considered objectionable or illegal as per Indian law.</li>
<li><b>Identity</b> : I shall not attempt to deceive others about my identity in electronic communications or network traffic. I will also not use BIT Ranchi IT resources to threaten, intimidate, or harass others.</li>
<li><b>Privacy</b> : I will not intrude on privacy of anyone. In particular I will not try to access computers (hacking), accounts, files, or information belonging to others without their knowledge and explicit consent.</li>
<li><b>Monitoring</b> : I understand that the IT resources provided to me are subject to monitoring, with cause, as determined through consultation with the BIT Ranchi administration, when applicable. The monitoring may include aggregate bandwidth usage to effectively manage limited IT resources as well as monitoring traffic content in response to a legal or law enforcement request to do so. I authorize BIT Ranchi administration to perform network vulnerability and port scans on my systems, as needed, for protecting the overall integrity and efficiency of BIT Ranchi network.</li>
<li><b>Viruses</b> : I shall maintain my computer on this network with current virus detection software and current updates of my operating system, and I shall attempt to keep my computer free from viruses, worms, trojans, and other similar programs.</li>
<li><b>File Sharing</b> : I shall not use the IT infrastructure to engage in any form of illegal file sharing (examples: copyrighted material, obscene material).</li>
<li><b>Security</b> : I understand that I will not take any steps that endanger the security of the BIT Ranchi network. Specifically, I will not attempt to bypass firewalls and access rules in place. This includes not setting up servers of any kind (examples: web, mail, proxy, DC++ Hubs) or any other softwares without concern of network team. In critical situations, BIT Ranchi authorities reserve the right to disconnect any device or disable any account if it believed that either is involved in compromising the information security of BIT Ranchi.</li>
<li><b>Settings</b> : I understand that I will no change or tamper any settings for the network setup which are done by the Network team.</li>
<li><b>Penalties</b> : I understand that any use of IT infrastructure at BIT Ranchi that constitutes a violation of BIT Ranchi Regulations could result in administrative or disciplinary procedures.</li>
<br>
<div style="text-align:center">
<button class="submit_btn" id="agree" style='font-weight:bold;'>I Agree To Abide By These Terms And Conditions</button>
</div>
</div>
		
		<div id="form">
		<h4>Register</h4>
		<br>		
		<form action='?action=account_register' method='post' name="form" onSubmit="return validate();">
			<table><colgroup><col width="200" /><col width="250" /></colgroup>
				<tr><td>DC Nick </td><td><input  type="text" size="32" maxlength="30" placeholder='3-30 characters long' name="nick"/></td></tr>
				<tr><td>Password </td><td><input class="field" type="password" size="32" maxlength="30"  placeholder='**********'name="login_pwd1"/></td></tr>
				<tr><td>Re-Enter Password </td><td><input class="field" type="password" size="32" maxlength="30"  placeholder='**********'name="login_pwd2"/></td></tr>
				<tr><td>IP Address</td><td><input  type="text" size="32" name="login_ip" value=' '''+dchub.http.env["REMOTE_ADDR"]+''' 'disabled=disabled /></td></tr>
				<tr><td>Full Name</td><td><input  type="text" size="32" maxlength="50" placeholder='First-Name Last-Name' name="name"/></td></tr>
				<tr><td>Roll Number</td>
				<td><select  style="width:30%;" name="course">
				<option>BARCH</option>
				<option>BPH</option>
				<option selected="selected">BE</option>
				<option>ME</option>
				<option>MSc</option>
				</select>
				<input  style="width:22%;" placeholder='2357' type="text" maxlength="4" name="no"/>
				<select  style="width:24%;" name="year">
				<option>2007</option>
				<option selected="selected">2008</option>
				<option>2009</option>
				<option>2010</option>
				<option>2011</option>
				</select></td></tr>
				<tr><td>Branch Code</td><td><input  type="text" maxlength="50" placeholder='CSE|IT|ECE|EEE|MECH|CIVIL|PROD' name="branch"/></td></tr>
				<tr><td>E-mail</td><td><input  type="text" maxlength="50" placeholder='name@email.com' name="email"/></td></tr>
				<tr><td>
				<select  style='width:230px;' name="sec_q" id="choice">
				<option value="NULL" selected="selected" disabled="disabled">Choose your security question</option>
				<option>Who was your childhood superhero?</option>
				<option>What is your Mother's middle name?</option>
				<option>What was your childhood nickname? </option>
				<option>Who was your first crush in college?</option>
				<option>What was your first phone number?</option>
				</select></td>
				<td>
				<input type="text"  name="sec_a"  maxlength="100" placeholder='Answer' size="32"/></td></tr>	
				</tr>
				<tr><td></td><td>
				<input type="hidden" name="roll" value=''>
				<input class="submit_btn float_l" style='font-weight:bold;' value='Register' type='submit'>
				
				</td></tr>
			</table>
		</form>
		</div>
	</div>
		'''
		
	def repo(self): # Details for the Repositories
		print '''
		
		<title>Repositories</title>
    </div> <!-- end of header -->
</div> <!-- end of header wrapper -->

<div id="main_wrapper">
	<div id="main">
    
    	<div id="content" style='font-size: 14px;'>
		<h4>Linux Repositories</h4>
		<br>
		Run the following command in the terminal to add the local repository to your distro's package manager :
		<br><br>
		<table border=1 style='font-size: 12px;'>
			<tr><td style='text-align:center; width:100px;'>Ubuntu 10.04</td><td>sudo wget..........................................................................................</td></tr>
			<tr><td style='text-align:center;'>Ubuntu 10.10</td><td>sudo wget..........................................................................................</td></tr>
			<tr><td style='text-align:center;'>Fedora 13</td><td>sudo wget..........................................................................................</td></tr>
			<tr><td style='text-align:center;'>Fedora 14</td><td>sudo wget..........................................................................................</td></tr>
		</table>
		</div>
		'''
		


	def adminconsole(self): # Written by SourceCode
		if not dchub.mydc.auth(5): return
		print '''
			<title>Admin Console</title>
			</div> <!-- end of header -->
			</div> <!-- end of header wrapper -->
			<div id="main_wrapper"><div id="main"><div id="content" style='font-size: 14px;'>
			'''
		try: nick = dchub.http.get["nick"]
		except: nick = None
		if nick is None:
			print "<table width=100%><tr><th style='text-align:left;'>Nickname</th><th style='text-align:left;'>Class</th><th style='text-align:left;'>IP Address</th></tr>"
			userlist = dchub.mydc.users()
			for user in userlist:
				link = re.sub("\?&","?","?"+re.sub("&nick=([^&]*)","",dchub.http.env["QUERY_STRING"])+"&nick="+str(user["nick"]))
				print "<tr><td><a href='"+link+"'>"+str(user["nick"])+"</a></td><td>"+str(user["class"])+"</td><td>"+str(user["login_ip"])+"</td></tr>"
			print "</table>"
		else:
			user = dchub.class_user(str(dchub.http.get["nick"]))
			if user.data == None: print "Could not find specified user in database."
			else:
				print "<h4 style='text-align:center;'>User Data</h4><br><table width=100%><tr><th>Variable</th><th>Value</th></tr><tr>"
				for key in user.data:
					if key in ["reg_op"]: continue
					print "<tr><td style='text-align:center;'>"+str(key)+"</td><td style='text-align:center;'>"+str(user.data[key])+"</td></tr>"
				print "</table><br><br>";
				print "<h4 style='text-align:center;'>Search Terms</h4><br><table width=100%><tr><td style='text-align:center;'>"
				search = []
				tth = []
				pm = {}
				try:
					f = open("/etc/verlihub/logs/"+nick+".txt","r")
					for line in f:
						try:
							data = eval(line)
							t = datetime.datetime.fromtimestamp(int(data["time"])).strftime("%d %b %Y, %H:%M:%S")
							if data["type"]=="search":
								s = "<span title='Date & Time : "+str(t)+" ; IP Address : "+str(data["ip"])+"'>"+str(data["term"])+"</span>"
								if re.search("^TTH\:",data["term"]) is None: search.append(s)
								else: tth.append(s)
							if data["type"]=="pm-recieve":
								other = data["from"]
								l = re.sub("\?&","?","?"+re.sub("&nick=([^&]*)","",dchub.http.env["QUERY_STRING"])+"&nick="+other)
								try: pm[data["from"]]
								except: pm[data["from"]]=""
								pm[data["from"]]+="<span title='Date & Time : "+str(t)+" ; IP Address : "+str(data["ip"])+"'><a href='"+l+"'>"+other+"</a> : "+data["message"]+"</span><br>"							
							if data["type"]=="pm-send":
								try: pm[data["to"]]
								except: pm[data["to"]]=""
								pm[data["to"]]+="<span title='Date & Time : "+str(t)+" ; IP Address : "+str(data["ip"])+"'>"+nick+" : "+data["message"]+"</span><br>"
						except: pass
				except: pass
				print "<b>Normal Searches</b> : "+", ".join(search)+"<br>"
				print "<b>TTH Searches</b> : "+", ".join(tth)+"<br>"
				print "</td></tr></table><br><br>"
				print "<h4 style='text-align:center;'>Private Coversations</h4><br><table width=100%><tr><td>"
				for other in pm:
					print "<b onClick=\"$('.pm-logs').not('#pm-log-"+other+"').slideUp(250); $('#pm-log-"+other+"').slideToggle(250);\">PM with "+other+"</b><div class='pm-logs' id='pm-log-"+other+"' style='display:none'>"+pm[other]+"</div><br><br>"
				print "</table>"
					
		print "</div>"

dchub.process(theme)
		
