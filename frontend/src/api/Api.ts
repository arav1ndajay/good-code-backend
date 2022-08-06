import request from "superagent";

export async function Get(url: string) {
  if (localStorage.getItem("access-token") != null) {
    const res = await request
      .get(url)
      .set("Authorization", `Bearer ${localStorage.getItem("access-token")}`)
      .set("Ocp-Apim-Subscription-Key", import.meta.env.VITE_OCPMID);

    return res;
  } else {
	throw new NotLoggedInError()
  }
}

export async function Post(body: any, url: string) {
	if (localStorage.getItem("access-token") != null) {
		const res = await request
		  .post(url)
		  .set("Authorization", `Bearer ${localStorage.getItem("access-token")}`)
		  .set("Ocp-Apim-Subscription-Key", import.meta.env.VITE_OCPMID)
		  .send(body);
	
		return res;
	  } else {
		throw new NotLoggedInError()
	  }
}

export class NotLoggedInError extends Error {
  constructor() {
    super("Not logged in");
    Object.setPrototypeOf(this, NotLoggedInError.prototype);
  }
}
