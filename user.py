from config import users
import base64

class User:

	def __init__(self):
		pass


	def get_api_key(self, userid):
		log_user = users.find_one({'userid':userid})
		if log_user==None:
			return None
		return str(log_user['key'])


	def gen_api_key(self, key):
		return base64.b64encode(key)


	def gen_id(self, name, email):
		k=(name.split()[0]+base64.b64encode(email))[:10]
		return k


	def create(self,name,email,passwrd):
		user=users.find_one({"email":email})
		
		if user!=None:
			return "This Email Already Exists."
		else:
			temp_user={}
			temp_user['email']=email
			temp_user['userid']=self.gen_id(name, email)
			temp_user['password']=base64.b64encode(passwrd)
			temp_user['key']=self.gen_api_key(temp_user['userid']+passwrd)
			print temp_user
			try:
				ins_id = users.insert(temp_user)
				return "Success ID: "+temp_user['userid']+" API_KEY: " + temp_user['key']
			except:
				return "Error : User Not Created"



