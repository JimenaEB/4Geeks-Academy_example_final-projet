const getState = ({ getStore, getActions, setStore }) => {
	return {
		store: {
			baseURL: "https://3001-crimson-cockroach-74szw807.ws-eu08.gitpod.io/api",
			currentUser: {}
		},
		actions: {
			login: (mail, pass) => {
				fetch(getStore().baseURL.concat("/login"), {
					method: "POST",
					mode: "no-cors",
					headers: { "Content-Type": "application/json" },
					body: JSON.stringify({ email: mail, password: pass })
				}).then(response => {
					if (response.ok) {
						response = response.json();
						console.log(response);
					}
				});
			}
		}
	};
};

export default getState;
