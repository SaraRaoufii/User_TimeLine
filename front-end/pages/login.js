function Login(){
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    if (!username || !password){
        alert("Complate all fields")
        return
    }
     
    fetch("http://127.0.0.1:8000/graphql/" , {
        method:"Post",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            query:
             `mutation{
                loginUser(password:"${password}",
                username:"${username}"){
                    userId
                    success
                    message}
                }`
                })
        
    })
    .then(res => res.json())
    .then(data => {
        console.log(data.data.loginUser);
        alert(data.data.loginUser.message);
        if (data.data.loginUser.success){
            localStorage.setItem("userId", data.data.loginUser.userId);
        }
    })
    .catch(err => console.error("Error:", err));

}
