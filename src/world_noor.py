class WorldNoor {
	constructor() {
		this.api = "https://worldnoor.com/api"
		this.nodeApi = "https://nodeapi.worldnoor.com/api"
		this.headers = {
			"user-agent": "okhttp/4.9.1",
			"authorization": `Bearer ${uuid4()}`
		}
		this.deviceType = "android"
	}

	async register(name, email, password, countryCode = "US") {
		const response = await fetch(
			`${this.api}/register_new?password=${password}&deviceType=${this.deviceType}&country_code=${countryCode}&&email=${email}&password_confirmation=${password}&firstname=${name}`, {
				method: "POST",
				headers: this.headers
			})
		return response.json()
	}

	async login(email, password) {
		const response = await fetch(
			`${this.api}/login?email=${email}&password=${password}&deviceType=${this.deviceType}`, {
				method: "POST",
				headers: this.headers
			})
		const data = await response.json()
		if ("token" in data) {
			this.token = data.token
			this.jwtToken = data.jwtToken
			this.headers["jwttoken"] = this.jwtToken
			this.userId = await this.verifyLogin().data.id
		}
	}

	async verifyLogin(email, password, verificationCode) {
		const response = await fetch(
			`${this.api}/login-verify?skip_verification=1&token=${this.token}`, {
				method: "POST",
				headers: this.headers
			})
		return response.json()
	}

	async getNotifications() {
		const response = await fetch(
			`${this.api}/notifications/get_all?token=${this.token}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getNewsFeed(page = 1) {
		const response = await fetch(
			`${this.api}/newsfeed?page=${page}&token=${this.token}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getStories() {
		const response = await fetch(
			`${this.api}/stories?token=${this.token}`, {
				method: "POST",
				headers: this.headers
			})
		return response.json()
	}

	async getReels(page = 1, fetchPublicPostsOnly = true) {
		const response = await fetch(
			`${this.api}/newsfeed-videos?page=${page}&fetch_public_posts_only=${fetchPublicPostsOnly}&token=${this.token}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getAccountBasic() {
		const response = await fetch(
			`${this.api}/profile/basic?token=${this.token}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async reactToPost(postId, reactionType) {
		const response = await fetch(
			`${this.api}/react?post_id=${postId}&type=${reactionType}&token=${this.token}`, {
				method: "POST",
				headers: this.headers
			})
		return response.json()
	}

	async commentPost(postId, body) {
		const response = await fetch(
			`${this.api}/comment`, {
				method: "POST",
				body: JSON.stringify({
					post_id: postId,
					body: body,
					identifier: Math.floor(Date.now() / 1000) * 1000,
					token: this.token
				}),
				headers: this.headers
			})
		return response.json()
	}


	async getPostInfo(postId) {
		const response = await fetch(
			`${this.api}/post/get-single-newsfeed-item/${postId}?token=${this.token}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getUserInfo(userId) {
		const response = await fetch(
			`${this.api}/profile/about?token=${this.token}&user_id=${userId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async sendFriendRequest(userId) {
		const response = await fetch(
			`${this.api}/user/send_friend_request?token=${this.token}&user_id=${userId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async cancelFriendRequest(userId) {
		const response = await fetch(
			`${this.api}/user/cancel_friend_request?token=${this.token}&user_id=${userId}`, {
				method: "GET",
				headers: this.headers
			})
		return response.json()
	}

	async getFriends() {
		const response = await fetch(
			`${this.api}/user/friends?token=${this.token}`, {
				method: "POST",
				headers: this.headers
			})
		return response.json()
	}

	async getConversations(page = 1, perPage = 10) {
		const response = await fetch(
			`${this.nodeApi}/conversations`, {
				method: "POST",
				body: JSON.stringify({
					page: page,
					per_page: perPage,
					token: this.token
				}),
				headers: this.headers
			})
		return response.json()
	}
}

module.exports = {WorldNoor}
