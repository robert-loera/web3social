import { useEffect, useState } from "react";
import Register from "./components/Register";

const App = () => {
  // create message we will be getting from root endpoint
  const [message, setMessage] = useState("")
  
  // function to make request to API
  const getWelcomeMessage = async () => {
    // create request options
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      },
    }
    // make the actual request
    const response = await fetch("http://127.0.0.1:8000/", requestOptions)
    const data = await response.json()

    if (!response.ok) {
      console.log("something went wrong")
    }
    else{
      // assign the message from api to message
      setMessage(data.message)
    }
  }

  useEffect(() => {
    getWelcomeMessage()
  }, [])
  return (
    <div>
      <h1>{message}</h1>
      {/* call  register function that returns all this html*/}
      <Register/>
    </div>
  );
}

export default App;
