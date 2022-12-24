let originURL = window.location.origin;
let path = location.href
let URLorderNum = path.split('=')[1];
let orderNum = document.querySelector(".ordernum")
let msgTitle = document.querySelector(".msgtitle")
let msgNotice = document.querySelector(".msgnotice")

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
                showOrderNum();
            } else {
                document.location.href = "/";
                console.log("未登入");
            }
        });
}

async function showOrderNum() {
    let response = await fetch(`${originURL}/api/orders/${URLorderNum}`)
    let data = await response.json();
    let result = data.data;
    if (result) {
        // 有資料成功，顯示訂單號碼
        orderNum.innerText = URLorderNum;
    } else {
        document.location.href = "/";
    }
    if (result.status == "已付款") {
        // 付款成功
        msgTitle.innerText = "行程付款成功";
        msgNotice.innerHTML = "感謝您的預訂！<br>當日將以通話聯繫，請確保手機暢通。"
    } else {
        // 付款失敗
        msgTitle.innerText = "行程付款失敗";
        msgNotice.innerText = "如仍需預約行程，請重新預訂。"
    }
}
