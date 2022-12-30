let main = document.querySelector(".main");
let history = document.querySelector(".history");
let originURL = window.location.origin;
let bname = document.querySelector(".bname");
let fakefooter = document.querySelector(".fakefooter");

// 網頁載入時，確認登入狀態
window.onload = function checkSigninStatus() {
    fetch(`${originURL}/api/user/auth`)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            let result = data.data;
            if (result != null) {
                bname.textContent = result.name;
                header_logout.classList.remove("show");
                header_history.classList.remove("show");
                header_login.remove();
                getData();
            } else {
                document.location.href = "/";
                console.log("未登入");
            }
        });
}

let myBook = document.querySelector(".myBook");

async function getData() {
    const response = await fetch(`${originURL}/api/order`);
    const data = await response.json();
    result = data.data;
    console.log(result)

    if (result != null && result.length >= 4) {
        history.classList.remove("show");
        fakefooter.remove();
        myBooking(result);
    }else if(result.length < 4){
        history.classList.remove("show");
        fakefooter.classList.remove("show");
        myBooking(result);
    } else {
        noBooking();
        console.log("no booking");
        history.remove();
        fakefooter.classList.remove("show");
    }
}

function myBooking(result) {
    // let hour =
    //     result.time == "morning" ? "早上 9 點到 12 點" : "下午 2 點到 5 點";

    const myBook = document.createElement("div");

    let maindata = '';
    for (let i = 0; i <= result.length; i++) {

        let number = result[i].number;
        let bookingname = result[i].trip.attraction.name;
        let bimg = result[i].trip.attraction.image;
        let bdate = result[i].trip.date;
        let bhour = result[i].trip.time == "morning" ? "早上 9 點到 12 點" : "下午 2 點到 5 點";
        let bprice = result[i].price;
        let baddr = result[i].trip.attraction.address;
        let contactName = result[i].contact.name;
        let contactEmail = result[i].contact.email;
        let contactPhone = result[i].contact.phone;
        let bstatus = result[i].status;

        maindata += `
        <button class="collapsible">訂單編號：<span class="orderNum">${number}</span></button>
        <div class="content">
            <div class="bookinglist">
                <div></div>
                <!-- pic -->
                <div class="bookingpic">
                    <img src="${bimg}" alt="" id="bimg">
                </div>
                <!-- info -->
                <div class="maininfo">
                    <div>
                        <div class="bookingtitle">
                            台北一日遊：
                            <span class="bookingname">${bookingname}</span>
                        </div>
                        <div class="bookingdetail">
                            <p>• 日期：
                                <span class="bname">${bdate}</span>
                            </p>
                            <p>• 時間：
                                <span class="bhour">${bhour}</span>
                            </p>
                            <p>• 費用：
                                新台幣 <span class="bprice" id="field-price">${bprice}</span> 元
                            </p>
                            <p>• 地點：
                            <span class="baddr">${baddr}</span>
                        </p>
                        </div>
                    </div>
                    <div>
                        <div class="contactdetail">
                            <div class="contecttitle">
                                <span>&emsp;</span>
                            </div>
                            <p>• 狀態：
                                <span class="bstaus1">${bstatus}</span>
                            </p>
                            <p>• 聯絡姓名：
                                <span class="contactName">${contactName}</span>
                            </p>
                            <p>• 聯絡姓名：
                                <span class="contactEmail">${contactEmail}</span>
                            </p>
                            <p>• 手機號碼：
                                <span class="contactPhone">${contactPhone}</span>
                            </p>
                        </div>
                    </div>
                </div>
            </div>
            <div></div>
        </div><br><br><br>`
        myBook.innerHTML = maindata;
        history.appendChild(myBook);




        // collapsible
        var coll = document.getElementsByClassName("collapsible");
        var x;
        for (x = 0; x < coll.length; x++) {
            coll[x].addEventListener("click", function () {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.maxHeight) {
                    content.style.maxHeight = null;
                } else {
                    content.style.maxHeight = content.scrollHeight + "px";
                }
            });
        }
    }
}

function noBooking() {
    const noBook = document.createElement("div");
    noBook.innerHTML = `<div class="nobooking">
      <div></div>
      <div class="btitle">目前沒有任何歷史訂單。</div>
      <div></div>
    </div>`
    main.appendChild(noBook);
}


