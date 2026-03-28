$(document).ready(function () {

    const usernameRegex = /^[a-z][a-z0-9_]{4,14}$/;
    const passwordRegex =
        /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/;

    /* ======================
       SIGNUP
    ====================== */
    $("#signupForm").on("submit", async function (e) {
        e.preventDefault();
        $(".error").text("");

        //console.log("Doing signup");

        const username = $("#signupUsername").val()?.trim();
        const password = $("#signupPassword").val()?.trim();
        const confirm  = $("#signupConfirm").val()?.trim();

        if (!username) return;

        if (!usernameRegex.test(username)) {
            $("#signupUsernameError").text("Invalid username format");
            return;
        }

        if (!passwordRegex.test(password)) {
            $("#signupPasswordError").text("Weak password");
            return;
        }

        if (password !== confirm) {
            $("#signupConfirmError").text("Passwords do not match");
            return;
        }

        const res = await fetch("/api/signup/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            $("#signupUsernameError").text(data.username?.[0] || "Signup failed");
            return;
        }

        localStorage.setItem("accessToken", data.token);
        window.location.href = "/";
    });

    /* ======================
       LOGIN
    ====================== */
    $("#loginForm").on("submit", async function (e) {
        e.preventDefault();
        $(".error").text("");

        console.log("Doing login");

        const username = $("#loginUsername").val()?.trim();
        const password = $("#loginPassword").val()?.trim();

        if (!username || !password) {
            $("#loginPasswordError").text("All fields required");
            return;
        }

        const res = await fetch("/api/signin/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await res.json();

        if (!res.ok) {
            $("#loginPasswordError").text(data.error || "Login failed");
            return;
        }

        localStorage.setItem("accessToken", data.token);
        window.location.href = "/";
    });

    /* ======================
       PASSWORD TOGGLE
    ====================== */
    $(document).on("click", ".toggle-password", function () {
        const input = $("#" + $(this).data("target"));
        if (!input.length) return;

        input.attr(
            "type",
            input.attr("type") === "password" ? "text" : "password"
        );

        $(this).text(input.attr("type") === "password" ? "👁" : "🙈");
    });

});
