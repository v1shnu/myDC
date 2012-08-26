This site has been coded and designed by Kaustubh Karkare (SourceCode) & Vishnu Mohandas (DJ).

If you are here to try and understand or make modifications to this code, please remember a few things:
	This script has been exclusively designed for a specific server configuration : Ubuntu, apache with mod_wsgi, python, Verlihub.
	In order that destructors are called in proper order (ie - before those of another class on which this one depends), "del" is wherever required.
	Sessions have been implemented using the database system because I was too lazy to implement it using files (concurrency issues).
	
Installation Commands (MySQL):
	CREATE TABLE sessions (pysessid varchar(50) primary key, data text, expire int);
	CREATE TABLE content (id int not null primary key auto_increment, timex int, nick tinytext, content tinytext, category int, magnet tinytext, likex tinytext);
	ALTER TABLE reglist ADD name TINYTEXT NULL DEFAULT NULL, ADD roll TINYTEXT NULL DEFAULT NULL, ADD branch TINYTEXT NULL DEFAULT NULL, ADD sec_q TINYTEXT NULL DEFAULT NULL, ADD sec_a TINYTEXT NULL DEFAULT NULL;
		
Installation Commands (Verlihub):
	!set default_password_encryption 0
	!set use_reglist_cache 0
	!set send_user_info 0

Things you should know if you're trying to create a new theme (for DJ):
	1) Create a new theme class (class theme).
	2) Use the constructor, __init__(self), and the destructor, __del__(self) to print the HTML/JS/CSS	code that is constant across all pages.
	3) Create a separate function for each page, with the function name being the same as the page name. The GET argument 'display' will be used to decide which function to call. For example, http://<server-addr>/<script-path>?display=home will call the class_<themename>().home() function. Default function called is 'index'
	4) You may use the following object properties and methods for generating content in these functions:
		dchub.mydc.auth(level) : Returns True only if the user has a class equal to or above given level (which is an integer).
		dchub.mydc.content() : Returns a tuple, the first element of which is a set of useful links, and the seconds is the list of content IDs which have been filtered according to given restrictions.
		dchub.mydc.users(): Returns a list of nicknames of all users that are registered.
		dchub.mydc.motd_display_notice(): Returns the current MOTD Notice message.
		dchub.class_user(str nickname) : Creates a user object, loads data from the database about the user whose nickname is specified and save it in the object_user.data dictionary.
		dchub.class_content(id) : Creates a content object, loads data from the database about the user whose id (which is an integer) is specified and save it in the object_user.data dictionary.
		dchub.object_content.liked() : Returns if the current user (who shall be viewing the page) likes this content.
		dchub.http.get[variable] : Corresponds to PHP's $_GET[$variable]. Do not use the variable names 'action', 'display', 'ajax', 'term', 'category', 'offset', 'size' and 'sort', as they have a special meaning to the classes defined in this module.
		dchub.http.post[variable] : Corresponds to PHP's $_POST[$variable]. This dictionary will probably not be of much use to you, as you will not be performing any 'actions' yourself.
		dchub.http.session[variable] : Corresponds to PHP's $_SESSION[$variable].
		dchub.http.cookie[variable] : Corresponds to PHP's $_COOKIE[$variable].
		dchub.http.env[variable] : A combination of PHP's $_SERVER and $_ENV superglobal associatove arrays.
	5) The following actions are available to you, and can be invoked by sending appropriate form data to this script, specifying the action using the GE variable 'action'. Form tag example : "<form action='?action=account_login' method='post'>"
		account_login : Requires POST variables "nick" and "pass0". Also requires the password to be stored in an unencrypted form on the Verlihub database, so that comparison is possible.
		account_logout : Requires no additional data. Users need to be logged in to do this.
		account_register : Requires POST variables "nick" (may only contain alphanumeric and underscore characters), "login_pwd1", "login_pwd2" (should be equal to "login_pwd1"), "email", "name", "roll", "branch", "sec_q", "sec_a".
		account_delete : Requires POST variable "nick".
		password_reset : Requires POST variables "nick", "email" and "sec_a" (Security Answer). Used to reset a user's password, in case he/she forgets it. You shall need to display their security question using object_user.data["sec_q"] before they can provide the appropriate answer.
		password_update : Requires POST variables "nick", "pass0" (original), "pass1" (new), "pass2" (repeat new). Users need to be logged in to do this.
		content_create : Requires POST variables "content", "category", "magnet". Users need to be logged in to do this.
		content_like : Requires GET variable "id" (content-id). Users need to be logged in to do this.
		content_unlike : Requires GET variable "id" (content-id). Users need to be logged in to do this.
		content_delete : Requires GET variable "id" (content-id). Only users who have created the content or have a level of 5 and above can do this.
		motd_update_content : Updates the motd file for Verlihub, posting details of new content items.
		motd_update_notice : Updates the motd file for Verlihub, which contains notices. Requires POST variable "notice".
	6) You need to import this module (import dchub), define the class as described above, and finally call: dchub.process(theme)