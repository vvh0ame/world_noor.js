import requests
from time import time
from uuid import uuid4

class WorldNoor:
	def __init__(self, device_type: str = "android") -> None:
		self.api = "https://worldnoor.com/api"
		self.node_api = "https://nodeapi.worldnoor.com/api"
		self.headers = {
			"user-agent": "okhttp/4.9.1",
			"authorization": f"Bearer {uuid4()}"
		}
		self.token = None
		self.user_id = None
		self.jwt_token = None
		self.device_type = device_type

	def register(
			self,
			name: str,
			email: str,
			password: str,
			country_code: str = "US") -> dict:
		return requests.post(
			f"{self.api}/register_new?password={password}&device_type={self.device_type}&country_code={country_code}&&email={email}&password_confirmation={password}&firstname={name}",
			headers=self.headers).json()

	def login(
			self,
			email: str,
			password: str) -> dict:
		response = requests.post(
			f"{self.api}/login?email={email}&password={password}&device_type={self.device_type}",
			headers=self.headers).json()
		if "token" in response["data"]:
			self.token = response["data"]["token"]
			self.jwt_token = response["data"]["jwtToken"]
			self.user_id = self.verify_login()["data"]["id"]
			self.headers["jwttoken"] = self.jwt_token
		return response

	def verify_login(self) -> dict:
		return requests.post(
			f"{self.api}/login-verify?skip_verification=1&token={self.token}",
			headers=self.headers).json()

	def get_all_notifications(self) -> dict:
		return requests.get(
			f"{self.api}/notifications/get_all?token={self.token}",
			headers=self.headers).json()

	def get_news_feed(self, page: int = 1) -> dict:
		return requests.get(
			f"{self.api}/newsfeed?page={page}&token={self.token}",
			headers=self.headers).json()

	def get_languages(self) -> dict:
		return requests.get(
			f"{self.api}/meta/languages?token={self.token}",
			headers=self.headers).json()

	def get_stories(self) -> dict:
		return requests.post(
			f"{self.api}/stories?token={self.token}",
			headers=self.headers).json()

	def get_reels(
			self,
			page: int = 1,
			fetch_public_posts_only: bool = True) -> dict:
		return requests.get(
			f"{self.api}/newsfeed-videos?page={page}&fetch_public_posts_only={fetch_public_posts_only}&token={self.token}",
			headers=self.headers).json()

	def get_account_basic(self) -> dict:
		return requests.get(
			f"{self.api}/profile/basic?token={self.token}",
			headers=self.headers).json()

	def react_to_post(
			self,
			post_id: int,
			reaction_type: str = "like") -> dict:
		return requests.post(
			f"{self.api}/react?post_id={post_id}&type={reaction_type}&token={self.token}",
			headers=self.headers).json()


	def comment_post(
			self,
			post_id: int,
			body: str) -> dict:
		data = {
			"post_id": post_id,
			"body": body,
			"identifier": int(time() * 1000),
			"token": self.token
		}
		return requests.post(
			f"{self.api}/comment",
			data=data,
			headers=self.headers).json() # 1669315224824

	def edit_comment(
			self,
			post_id: int,
			body: str,
			comment_id: int) -> dict:
		data = {
			"post_id": post_id,
			"body": body,
			"identifier": int(time() * 1000),
			"token": self.token,
			"comment_id": comment_id
		}
		return requests.post(
			f"{self.api}/comment",
			data=data,
			headers=self.headers).json()

	def delete_comment(
			self,
			comment_id: int) -> dict:
		return requests.delete(
			f"{self.api}/comment?token={self.token}&comment_id={comment_id}",
			headers=self.headers).json()

	def get_post_info(self, post_id: int) -> dict:
		return requests.get(
			f"{self.api}/post/get-single-newsfeed-item/{post_id}?token={self.token}",
			headers=self.headers).json()

	def report_post(
			self,
			post_id: int,
			report_id: int,
			body: str = None) -> dict:
		"""
		REPORT-IDS:
			1 - SPAM,
			2 - VIOLENCE,
			3 - HARASSMENT,
			4 - FALSE NEWS,
			5 - HATE SPEECH,
			6 - TERRORISM,
			7 - SUICIDE,
			8 - NUDITY,
			9 - SOMETHING ELSE
		"""
		url = f"{self.api}/post/report?report_id={report_id}&token={self.token}&report_post_id={post_id}"
		if body:
			url += f"&body={body}"
		return requests.post(
			url, headers=self.headers).json()

	def get_user_profile(self, user_id: int) -> dict:
		return requests.get(
			f"{self.api}/profile/about?token={self.token}&user_id={user_id}",
			headers=self.headers).json()

	def send_friend_request(
			self,
			user_id: int) -> dict:
		return requests.post(
			f"{self.api}/user/send_friend_request?token={self.token}&user_id={user_id}",
			headers=self.headers).json()

	def cancel_friend_request(
			self,
			user_id: int) -> dict:
		return requests.post(
			f"{self.api}/user/cancel_friend_request?token={self.token}&user_id={user_id}",
			headers=self.headers).json()

	def get_contacts(self) -> dict:
		return requests.get(
			f"{self.api}/contacts?token={self.token}",
			headers=self.headers).json()

	def get_friends(self) -> dict:
		return requests.get(
			f"{self.api}/user/friends?token={self.token}",
			headers=self.headers).json()

	def get_generic_notifications(self) -> dict:
		data = {
			"is_mobile": is_mobile,
			"token": self.token
		}
		return requests.post(
			f"{self.node_api}/generic_notifications",
			data=data,
			headers=self.headers).json()

	def get_conversations(
			self,
			page: int = 1,
			per_page: int = 10) -> dict:
		data = {
			"page": page,
			"per_page": per_page,
			"token": self.token
		}
		return requests.post(
			f"{self.node_api}/conversations",
			data=data,
			headers=self.headers).json()

	def get_images(self) -> dict:
		return requests.get(
			F"{self.api}/images/by_sections?token={self.token}",
			headers=self.headers).json()

	def get_saved_posts(self) -> dict:
		return requests.get(
			f"{self.api}/saved/newsfeed?token={self.token}",
			headers=self.headers).json()

	def get_pages(self) -> dict:
		return requests.get(
			f"{self.api}/page/list?token={self.token}",
			headers=self.headers).json()

	def get_page_categories(self) -> dict:
		return requests.get(
			f"{self.api}/page/categories_meta?token={self.token}",
			headers=self.headers).json()

	def create_page(
			self,
			title: str,
			category_id: int,
			page_url: str) -> dict:
		return requests.post(
			f"{self.api}/page/create?page_title={title}&page_category_ids[]={category_id}&token={self.token}&page_url={page_url}",
			headers=self.headers).json()

	def get_groups(self) -> dict:
		return requests.get(
			f"{self.api}/group/list?token={self.token}",
			headers=self.headers).json()

	def get_town_hall(self) -> dict:
		return requests.get(
			f"{self.api}/town_hall/get_data?token={self.token}",
			headers=self.headers).json()

	def update_password(
			self,
			old_password: str,
			new_password: str) -> dict:
		return requests.post(
			f"{self.api}/profile/update_password?token={self.token}&new_password={new_password}&current_password={old_password}&new_password_confirmation={new_password}",
			headers=self.headers).json()

	def get_login_sessions(self) -> dict:
		return requests.get(
			f"{self.api}/profile/login_sessions?token={self.token}",
			headers=self.headers).json()

	def delete_login_session(
			self,
			session_id: int) -> dict:
		return requests.post(
			f"{self.api}/profile/delete_login_session?session_id={session_id}&token={self.token}",
			headers=self.headers).json()

	def get_hidden_posts(self) -> dict:
		return requests.get(
			f"{self.api}/hidden/newsfeed?token={self.token}",
			headers=self.headers).json()

	def get_blocked_users(self) -> dict:
		return requests.get(
			f"{self.api}/user/blocked_users?token={self.token}",
			headers=self.headers).json()
