import { createContext, useEffect, useState } from "react"

// this is used to create a UserContext that we can use in the rest of the app
export const UserContext = createContext()

// set UserProvider to a function that takes props argument
export const UserProvider = (props) => {
  const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"))
  // use effect w/ function to fetch the user ( runs everytime the token is changed)
  useEffect(() => {
    // function to fetch the user from the API
    const fetchUser = async () => {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": 'application/json',
          // pass the auth type and token value for auth
          Authorization: "Bearer " + token
      }
    }
    // make the request to the API
    const response = await fetch("http://127.0.0.1:8000/usersme", requestOptions)

    // if the response is not ok set the token to null
    if (!response.ok) {
      console.log('there was a problem')
      setToken(null)
    }
    // local storage saves data in the browser
    localStorage.setItem('awesomeLeadsToken', token)
    }
    // call the function
    fetchUser()
    // every time token is updated run the above
  }, [token])

  return (
    // token and setToken can noe be accessed by all children
    <UserContext.Provider value={[token, setToken]}>
      {/* use props.children when dont know children ahead of time */}
      {/* props is passed in the function call */}
      {props.children}
    </UserContext.Provider>
  )
}