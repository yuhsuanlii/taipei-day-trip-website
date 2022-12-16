let main = document.querySelector(".main");
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
        // contactName.value = memberName;
        // contactEmail.value = memberEmail;
        header_logout.classList.remove("show");
        header_login.remove();
        getData();
      } else {
        document.location.href = "/";
        console.log("未登入");
      }
    });
}

async function getData() {
  const response = await fetch(`${originURL}/api/booking`);
  const data = await response.json();
  const result = data.data;

  console.log(result)

  if (result != null) {
    myBooking(result);
    fakefooter.remove();
  } else {
    noBooking();
    console.log("no booking");
    fakefooter.classList.remove("show");
  }
}


function myBooking(result) {
  let hour =
    result.time == "morning" ? "早上 9 點到 12 點" : "下午 2 點到 5 點";

  const myBook = document.createElement("div");
  myBook.innerHTML = `
<div class="bookinglist">
  <div></div>
  <!-- pic -->
  <div class="bookingpic">
      <img src="${result.attraction.image}" alt="">
  </div>
  <!-- info -->
  <div class="maininfo">
      <div class="bookingtitle">
          台北一日遊：
          <span class="bookingname">${result.attraction.name}</span>
      </div>
      <div class="bookingdetail">
          <p>日期：
              <span>2021-12-13</span>
          </p>
          <p>時間：
              <span>${hour}</span>
          </p>
          <p>費用：
              <span class="content" id="field-price">新台幣 ${result.price} 元</span>
          </p>
          <p>地點：
              <span>${result.attraction.address}</span>
          </p>
      </div>
  </div>
  <div class="bookingdelete">
      <img src="/static/img/icon_delete.png">
  </div>
</div>
<div class="bookingcontact">
  <div></div>
  <div>
      <p class="bnotice1">您的聯絡資訊</p>
      <div class="btitle">聯絡姓名：
          <input type="text" class="binput" required>
      </div>
      <div class="btitle">連絡信箱：
          <input type="email" class="binput" required>
      </div>
      <div class="btitle">手機號碼：
          <input type="tel" class="binput" maxlength="10" pattern="^1[0-9]{10}$"
              title="手機號格式不正確" required>
      </div>
      <p class="bnotice2">請保持手機暢通，準時到達，導覽人員將用手機與您聯繫，務必留下正確的聯絡方式。</p>
  </div>
  <div></div>
</div>
<div class="bookingcontact">
  <div></div>
  <div>
      <p class="bnotice1">信用卡付款資訊</p>
      <div class="btitle">卡片號碼：
          <input type="number" class="binput" maxlength="16" placeholder="**** **** **** ****"
              pattern="[0-9]{13,16}" required>
      </div>
      <div class="btitle">過期時間：
          <input type="text" class="binput" maxlength="4" placeholder="MM / YY" required>
      </div>
      <div class="btitle">驗證密碼：
          <input type="number" class="binput" maxlength="3" placeholder="CVV" required>
      </div>
  </div>
  <div></div>
</div>
<div class="bookingbottom">
  <div></div>
  <div class="bookingbutton">
      <div class="bnotice2">總價：新台幣 ${result.price} 元</div><br>
      <button class="bbutton">確認訂購並付款</button>
  </div>
  <div></div>
</div>`

  main.appendChild(myBook);

  let bookingdelete = document.querySelector(".bookingdelete");
  bookingdelete.addEventListener("click", () => {
    const attractionId = result.attraction.id;
    const date = result.date;
    const myTime = result.time;
    deleteBooking(attractionId, date, myTime);
  });

}

// 無待預訂的行程
function noBooking() {
  const noBook = document.createElement("div");
  noBook.innerHTML = `<div class="nobooking">
    <div></div>
    <div class="btitle">目前沒有任何待預訂的行程。</div>
    <div></div>
  </div>`
  main.appendChild(noBook);
}

async function deleteBooking(attractionId, date, myTime) {
  try {
    const response = await fetch(`${originURL}/api/booking`, {
      method: "DELETE",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        attractionId: attractionId,
        date: date,
        time: myTime,
      }),
    });
    const data = await response.json();
    if (data.ok) {
      document.location.href = "/booking";
    }
  } catch (error) {
    console.log("error", error);
  }
}