function login(event) {
    event.preventDefault();

    const email = document.querySelector('input[name="email"]').value;
    const password = document.querySelector('input[name="password"]').value;

    axios.post("/api/login/", {
        email: email,
        password: password
    })
    .then(res => {

        // ✅ SAVE TOKEN
        localStorage.setItem("token", res.data.access);

        window.location.href = "/dashboard/";

    })
    .catch(() => {
        alert("Invalid credentials ❌");
    });
}