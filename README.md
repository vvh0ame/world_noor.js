# world_noor.js
Mobile-API for [worldnoor](https://play.google.com/store/apps/details?id=com.ogoul.worldnoor) social network with all in one networking features like posts, videos, audios and documents sharing etc

## Example
```JavaScript
async function main() {
	const { WorldNoor } = require("./world_noor.js")
	const worldNoor = new WorldNoor()
	await worldNoor.login("email", "password")
}

main()
```
