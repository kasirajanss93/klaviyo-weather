const BASE_URL = 'http://127.0.0.1:8000/klaviyo-weather/api'
export {getCities,postUser}

function getCities() {
//  console.log(eventId+" "+content)
  const url = `${BASE_URL}/cities/`;
  return fetch(url, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    }
  })
  .then(response=>response.json())
}

function postUser(email,cityId) {
//  console.log(eventId+" "+content)
  const url = `${BASE_URL}/users/`;
  var payload = {
	"email": email,
  "cityId": cityId
  }
  return fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify( payload )
  })
}
