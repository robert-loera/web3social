// File for creating the form and handle the mission

import { useContext, useState } from "react";
import { UserContext } from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";

// create component
const Register = () => {
  // need these 5 for a user to login
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [confirmationPassword, setConfirmationPassword] = useState("")
  const [errorMessage, setErrorMessage] = useState("")
    // still need to use the setToken from register file to set token if login successfull (able to only get setToken w out the token variable as well)
  // w/ this useContext(UserContext) we get the values passed from the provider which is the setToken variable
  const [, setToken] = useContext(UserContext)

  // helper function to submit the data from our form to API
  const submitRegistration = async () => {
    console.log('inside submit function')
    const requestOptions = {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({email: email, username: username, password: password })
    }

    // now make the request
    const response = await fetch("http://127.0.0.1:8000/users", requestOptions)
    const data = await response.json()

    // if the response is not ok set the error message
    if (!response.ok){
      setErrorMessage(data.detail)
    }
    else{
      console.log(data.access_token)
      setToken(data.access_token)
    }
  }

  // function to handle the submit
  const handleSubmit = (e) => {
    // this just prevents html to do its own default actions on the form
    e.preventDefault()
    // check to make sure passwords r equal and correct length
    if (password === confirmationPassword && password.length >= 8) {
      // run the submit registration function above
      submitRegistration()
    }
    else {
      setErrorMessage("Invalid password match or password length")
    }
  }



  return (
    // the styling for our form
    <div className="column">
      {/* when the form is submit run the function */}
      <form className="box" onSubmit={handleSubmit}>
        <h1 className="title has-text-centered">Register</h1>
        <div className="field">
          <label className="label">Email Address</label>
          <div className="control">
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              // when the input changes run this e=event
              onChange={(e) => setEmail(e.target.value)}
              className="input"
              required/>
          </div>
        </div>
        <div className="field">
          <label className="label">Username</label>
          <div className="control">
            <input
              type="username"
              placeholder="Enter username"
              value={username}
              // when the input changes run this e=event
              onChange={(e) => setUsername(e.target.value)}
              className="input"
              required/>
          </div>
        </div>
        <div className="field">
          <label className="label">Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={password}
              // when the input changes run this e=event
              onChange={(e) => setPassword(e.target.value)}
              className="input"
              required/>
          </div>
        </div>
        <div className="field">
          <label className="label">Confirm Password</label>
          <div className="control">
            <input
              type="password"
              placeholder="Enter password"
              value={confirmationPassword}
              // when the input changes run this e=event
              onChange={(e) => setConfirmationPassword(e.target.value)}
              className="input"
              required/>
          </div>
        </div>
        {/* error message from other file passing our own param*/}
        <ErrorMessage message={errorMessage}/>
        <br />
        <button className="button is-primary" type="submit">Register</button>
      </form>
    </div>
  )
}

// export so we can call in app
export default Register