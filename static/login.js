let header_login = document.querySelector(".header_login");
let header_logout = document.querySelector(".header_logout");
let login_wrapper = document.querySelector(".login_wrapper");
let clicktosign = document.querySelector("#clicktosign");
let signup_wrapper = document.querySelector(".signup_wrapper");
let clicktologin = document.querySelector("#clicktologin");
let icon_close = document.querySelector(".icon_close");
let icon_close2 = document.querySelector(".icon_close2");
let mask = document.querySelector(".mask");
let signup_message = document.querySelector(".signup_message");
let login_message = document.querySelector(".login_message");
let pathname = location.pathname;
let loginform = document.querySelector("#loginform");
let signupform = document.querySelector("#signupform");
let header_booking = document.querySelector(".header_booking");

// header預訂行程
header_booking.addEventListener("click", () => {
    fetch(`${originURL}/api/user/auth`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            let result = data.data;
            if (result != null) {
                console.log("已登入")
                document.location.href = "/booking";
            } else {
                login_wrapper.classList.toggle("show");
                mask.classList.toggle("show")
            }
        });
});

// 網頁載入時，確認登入狀態
window.onload = function checkSigninStatus() {
    fetch(`${originURL}/api/user/auth`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            let result = data.data;
            if (result != null) {
                header_logout.classList.remove("show");
                header_login.remove();
            } else {
                header_login.classList.remove("show");
                header_logout.remove();
            }
        });
}


// classList.toggle 重複新增又移除
header_login.addEventListener("click", () => {
    login_wrapper.classList.toggle("show");
    signup_wrapper.classList.add("show");
    mask.classList.toggle("show")
});

// 點此註冊
clicktosign.addEventListener("click", () => {
    signup_wrapper.classList.remove("show");
    login_wrapper.classList.add("show");
    mask.classList.remove("show")
});

// 點此登入
clicktologin.addEventListener("click", () => {
    login_wrapper.classList.remove("show");
    signup_wrapper.classList.add("show");
    mask.classList.remove("show");
});

// icon X
icon_close.addEventListener("click", () => {
    login_wrapper.classList.add("show");
    mask.classList.add("show")
    // signup_wrapper.classList.add("show");
});
icon_close2.addEventListener("click", () => {
    // login_wrapper.classList.add("show");
    signup_wrapper.classList.add("show");
    mask.classList.add("show")
});

mask.addEventListener("click", () => {
    login_wrapper.classList.add("show");
    signup_wrapper.classList.add("show");
    mask.classList.add("show")
});

// 輸入錯誤後，按其他地方會清空錯誤訊息
loginform.addEventListener("click", () => {
    login_message.textContent = "";
});
signupform.addEventListener("click", () => {
    signup_message.textContent = "";
});

// ------------------------------------------------------------------------



let loginButton = document.querySelector("#loginbutton");

loginButton.addEventListener("click", function () {
    let email = document.querySelector("#email").value;
    let password = document.querySelector("#password").value;

    fetch("/api/user/auth", {
        method: "PUT",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ email: email, password: password }),
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.ok) {
                console.log("ok");
                document.location.href = originURL + pathname;

            } else if (data.error) {
                //   signinError.classList.remove("none");
                login_message.textContent = data.message;
            }
        })
        .catch(function (error) {
            console.log("error", error);
        });
});


// ---------------------------------------------------------------------------------
let signupButton = document.querySelector("#signupbutton");
// const signup_message = document.querySelector(".signup_message");

signupButton.addEventListener("click", function () {
    let sname = document.querySelector("#sname").value;
    let email = document.querySelector("#semail").value;
    let password = document.querySelector("#spassword").value;

    console.log(sname, email, password)

    fetch(`${originURL}/api/user`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ name: sname, email: email, password: password }),
    })
        .then(function (response) {
            console.log(response)
            return response.json();
        })
        .then(function (data) {
            console.log(data)
            if (data.ok) {
                signup_message.setAttribute("style", "color:green")
                signup_message.textContent = "註冊成功，請登入系統";
                // document.location.href = originURL+pathname;
                console.log("註冊成功")
                // 重新整理
                // window.location.reload();
            } else if (data.error) {
                signup_message.setAttribute("style", "color:rgb(207, 35, 35)")
                signup_message.textContent = data.message;
                console.log("註冊失敗")
            }
        })
        .catch(function (error) {
            console.log("error", error);
        });
});

header_logout.addEventListener("click", function () {
    fetch(`${originURL}/api/user/auth`, {
        method: "DELETE",
        headers: { "content-type": "application/json" },
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            if (data.ok) {
                document.location.href = originURL + pathname;
            }
        });
});