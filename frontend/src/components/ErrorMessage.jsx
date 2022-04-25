// function that is run when an error occurs and takes the error message and displays it in paragraph tag

const ErrorMessage = ({ message }) => (
  <p className="has-text-weight-bold has-text-danger">{message}</p>
)

// export to use in other files
export default ErrorMessage