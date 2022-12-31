let main = document.querySelector(".main");
let originURL = window.location.origin;
let bname = document.querySelector(".bname");
let fakefooter = document.querySelector(".fakefooter");

let inputName = document.querySelector(".inputName");
let inputEmail = document.querySelector(".inputEmail");
let inputPhone = document.querySelector(".inputPhone");
let orderMsg = document.querySelector(".orderMsg");


let result;

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
        // 預先填入會員資料
        inputName.value = result.name;
        inputEmail.value = result.email;
        getData();
      } else {
        document.location.href = "/";
        console.log("未登入");
      }
    });
}

let myBook = document.querySelector(".myBook");

async function getData() {
  const response = await fetch(`${originURL}/api/booking`);
  const data = await response.json();
  result = data.data;
  console.log(result)

  if (result != null) {
    myBooking(result);
    myBook.classList.remove("show");
    fakefooter.remove();
  } else {
    noBooking();
    console.log("no booking");
    myBook.remove();
    fakefooter.classList.remove("show");
  }
}

let bimg = document.querySelector("#bimg");
let bookingname = document.querySelector(".bookingname");
let bhour = document.querySelector(".bhour");
let bprice = document.querySelector(".bprice");
let baddr = document.querySelector(".baddr");
let totleprice = document.querySelector(".totleprice");
let bdate = document.querySelector(".bdate");



function myBooking(result) {
  let hour =
    result.time == "morning" ? "早上 9 點到 12 點" : "下午 2 點到 5 點";

  //   const myBook = document.createElement("div");
  //   myBook.innerHTML = ` `
  //   main.appendChild(myBook);

  bimg.src = result.attraction.image;
  bookingname.innerText = result.attraction.name;
  bhour.innerText = hour;
  bprice.innerText = result.price;
  baddr.innerText = result.attraction.address
  totleprice.innerText = result.price;
  bdate.innerText = result.date;

  let bookingdelete = document.querySelector(".bookingdelete");
  bookingdelete.addEventListener("click", () => {
    const attractionId = result.attraction.id;
    const date = result.date;
    const myTime = result.time;
    deleteBooking(attractionId, date, myTime);
  });

}

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

// tappay----------------------------------------------------

TPDirect.setupSDK(
  126911,
  'app_tkCvWjPZ0UdPMZPtTzjAgho3cDSWupfj8mHpM2eqVq5IPfWFpxgd2v8E0Zos',
  'sandbox'
);

let fields = {
  number: {
    // css selector
    element: "#card-number",
    placeholder: "**** **** **** ****",
  },
  expirationDate: {
    // DOM object
    element: document.getElementById("card-expiration-date"),
    placeholder: "MM / YY",
  },
  ccv: {
    element: "#card-ccv",
    placeholder: "CCV",
  },
};

TPDirect.card.setup({
  fields: fields,
  styles: {
    // Style all elements
    input: {
      color: "#757575",
    },
    // Styling ccv field
    "input#ccv": {
      "font-size": "18px",
    },
    // Styling expiration-date field
    "input#expiration-date": {
      "font-size": "18px",
    },
    // Styling card-number field
    "input#card-number": {
      "font-size": "18px",
    },
    // style focus state
    ":focus": {
      color: "#757575",
    },
    // style valid state
    ".valid": {
      color: "#448899",
    },
    // style invalid state
    ".invalid": {
      color: "rgb(185, 38, 38)",
    },
    // Media queries
    // Note that these apply to the iframe, not the root window.
    "@media screen and (max-width: 400px)": {
      input: {
        color: "rgb(185, 38, 38)",
      },
    },
  },
  // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

let primeNum;

function onClick() {
  // event.preventDefault()
  // 取得 TapPay Fields 的 status
  const tappayStatus = TPDirect.card.getTappayFieldsStatus()

  // 確認是否可以 getPrime
  if (tappayStatus.canGetPrime === false) {
    // alert('can not get prime')
    orderMsg.innerText = '信用卡資訊有誤，請重新輸入';
    return
  }

  if (inputName.value == "" || inputEmail.value == "" || inputPhone.value == "") {
    orderMsg.innerText = '請填寫所有欄位';
    return
  }

  orderMsg.setAttribute("style", "color:#448899")
  orderMsg.innerText = "信用卡驗證中，請稍等";

  // Get prime
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      console.log('get prime error ' + result.msg)
      return
    }
    // alert('get prime 成功，prime: ' + result.card.prime)
    primeNum = result.card.prime;
    myOrder(primeNum);

    // send prime to your server, to pay with Pay by Prime API .
    // Pay By Prime Docs: https://docs.tappaysdk.com/tutorial/zh/back.html#pay-by-prime-api
  })
}

// 按其他地方備註會消失
let bcard = document.querySelector(".bcard");
bcard.addEventListener("click", () => {
  orderMsg.innerText = "";
});
let binfo = document.querySelector(".binfo");
binfo.addEventListener("click", () => {
  orderMsg.innerText = "";
});


async function myOrder(prime) {
  let orderData = {
    prime: prime,
    order: {
      price: result.price,
      trip: result
    },
    contact: {
      name: inputName.value,
      email: inputEmail.value,
      phone: inputPhone.value
    }
  };
  console.log(orderData)

  let response = await fetch(`${originURL}/api/orders`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(orderData)
  });

  let responseData = await response.json();
  let orderresult = responseData.data;
  console.log(orderresult)
  number = orderresult.number

  if (orderresult) {
    console.log("訂單建立成功，包含付款狀態 ( 可能成功或失敗 )");
    // document.location.herf = `/thankyou?number=${orderresult.number}`;
    orderMsg.innerText = "訂單建立成功，系統將自動跳轉";
    orderMsg.setAttribute("style", "color:green")
    setTimeout(`thankyou(${number})`, 1000);
  } else {
    console.log("訂單建立失敗，輸入不正確");
    orderMsg.innerText = data.message;
  }
}

function thankyou(number) {
  document.location.href = `/thankyou?number=${number}`;
}

