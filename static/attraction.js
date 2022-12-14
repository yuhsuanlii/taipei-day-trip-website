// 導覽費用
let field_price = document.getElementById("field-price");
let morning = document.getElementById("morning");
let afternoon = document.getElementById("afternoon");
let radio1 = document.querySelector(".radio1")
let radio2 = document.querySelector(".radio2")
let bookingText = document.querySelector(".booking-text");
let booking = document.querySelector(".booking")


let now = new Date();
console.log(now.toISOString()) // 2022-12-28T09:05:37.383Z
let today = now.toISOString().split('T')[0];
document.getElementById("booking_date").min = today;

// ------------------------------------------------

field_price.innerText = morning.value

radio1.addEventListener('click', function () {
    field_price.innerText = morning.value
    bookingText.innerText = "";
}, false);

radio2.addEventListener('click', function () {
    field_price.innerText = afternoon.value
    bookingText.innerText = "";
}, false);

booking.addEventListener('click', function () {
    bookingText.innerText = "";
});

// ---------------------------------------------------------------

console.log(window.location.pathname)

let originURL = window.location.origin;

let path = window.location.pathname;
path = path.split("/");
const id = path[2] * 1;

let infoname = document.getElementById("infoname")
let category = document.getElementById("category")
let mrt = document.getElementById("mrt")
let description = document.getElementById("description")
let address = document.getElementById("address")
let transport = document.getElementById("transport")



fetch(`${originURL}/api/attraction/${id}`
).then((response) => response.json()
).then(function (data) {

    allpic(data);
    alldot(data);
    // console.log(data.data)
    infoname.innerHTML = data.data.name
    category.innerHTML = data.data.category
    mrt.innerHTML = data.data.mrt
    description.innerHTML = data.data.description
    address.innerHTML = data.data.address
    transport.innerHTML = data.data.transport
});


function alldot(data) {

    let alldot = document.getElementById("alldot");
    let dotElement = document.createElement('span');
    let main = '';
    for (let i = 0; i <= data.data.images.length - 1; i++) {
        main += `<span class="dot"></span>`
        // main+=`<span class="dot" onclick="currentSlide(${i})"></span>`
        console.log(i);
        alldot.innerHTML = main;
        alldot.appendChild(dotElement);
    }
}


function allpic(data) {

    let card = document.getElementById("card");
    let picElement = document.createElement('div');

    let main1 = '';
    for (let i = 0; i <= data.data.images.length - 1; i++) {
        // console.log(data.data.images[i]);
        let images = data.data.images[i]

        if (i == 0) {
            main1 += `<div class="mySlides fade" style="display:flex;"><img src="${images}"></div>`
        } else {
            main1 += `<div class="mySlides fade"><img src="${images}"></div>`
        }

        picElement.innerHTML = main1;
        card.appendChild(picElement);
    }
}


// 輪播開始------------------------------------------------------

let slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot")
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex - 1].style.display = "block";
    dots[slideIndex - 1].className += " active";
}


// 輪播結束------------------------------------------------------


function book(){
    const booking_date = document.querySelector(".booking_date");
    const attractionId = location.pathname.replace("/attraction/", "");
    const date = booking_date.value;
    const bookTime = document.querySelector("[name=booking-options]:checked").id;
    const price = bookTime == "morning" ? 2000 : 2500;

    myBooking(attractionId, date, bookTime, price);
}

async function myBooking(attractionId, date, bookTime, price) {
    try {
        const response = await fetch(`${originURL}/api/booking`, {
            method: "POST",
            headers: { "content-type": "application/json" },
            body: JSON.stringify({
                attractionId: attractionId,
                date: date,
                time: bookTime,
                price: price,
            }),
        });
        if (response.status == 403) {
            // 後端回復403
            login_wrapper.classList.toggle("show");
            mask.classList.toggle("show")
        }
        const data = await response.json();
        if (data.ok) {
            bookingText.innerText = "";
            document.location.href = "/booking";
        } else if (data.error) {
            // 按下按鈕但未登入
            bookingText.classList.remove("show");
            bookingText.textContent = data.message;
        }
    } catch (error) {
        console.log("error", error);
    }
}
