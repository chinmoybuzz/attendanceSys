document.addEventListener("DOMContentLoaded",function(){
    const loginForm  = document.getElementById("loginForm");
    
    if(loginForm ){ 
         loginForm.addEventListener("submit", function (event) {
            event.preventDefault(); 
            const username = document.getElementById("username").value.trim();
            const password = document.getElementById("password").value.trim();
            let messageDiv = document.getElementById("message");
            messageDiv.innerHTML = "";

            fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                messageDiv.innerHTML = `<p style="color: yellow;">Login successful! Redirecting...</p>`;
                    setTimeout(()=>{
                    window.location.href = "/take"; 
                    },1000)
                } else {
                    messageDiv.innerHTML = `<p style="color: red;">${data.message}</p>`;
                }
            })
            .catch(error =>{ console.error("Error:", error);
            messageDiv.innerHTML = `<p style="color: red;">An error occurred. Please try again later.</p>`;
        });

   
        })
    }
})

document.getElementById("runScript").addEventListener("click", function() {
            fetch("http://127.0.0.1:5000/run-script") // Call the Python server
                .then(response => response.json()) // Convert response to JSON
                .then(data => {
                    document.getElementById("output").innerText = "Output: " + data.message;
                })
                .catch(error => console.error("Error:", error));
        });



