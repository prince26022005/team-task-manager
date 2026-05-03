function login(event) {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    axios.post("/api/login/", {
        username: email,
        password: password
    })
    .then(res => {

        // ✅ SAVE TOKEN
        localStorage.setItem("token", res.data.access);

        alert("Login Success ✅");

        // ✅ FORCE REDIRECT
        window.location.href = "/dashboard/";

    })
    .catch(err => {
        alert("Invalid credentials ❌");
    });
}
localStorage.setItem("token", data.access);
fetch("/tasks/1/update/", {
    method: "POST",
    headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + localStorage.getItem("token")
    },
    body: JSON.stringify({ status: "done" })
})
