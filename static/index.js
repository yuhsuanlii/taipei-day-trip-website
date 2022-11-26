
let originURL = window.location.origin;
console.log(window.location.origin)
let search = document.querySelector("#search");
let container = document.getElementById('container');
let searchmenu = document.querySelector("#searchmenu");

// 點擊"搜尋欄"，跳出"選單"
// 選單內串接 category API
// 點擊"選單" 複製文字到"搜尋欄"

// 分類選單
async function getCategoryList() {
    await fetch(`${originURL}/api/categories`)
        .then((response) => response.json())
        .then(function (catData) {
            let data = catData.data;
            data.map((category) => {
                let categoryList = document.createElement("span");
                categoryList.setAttribute("class", "category");
                categoryList.textContent = category;
                searchmenu.appendChild(categoryList);
                categoryList.addEventListener("click", function showlist() {
                    let categoryText = categoryList.outerText;
                    search.value = categoryText;
                    searchmenu.classList.add("show");
                });
            });
        });
};
getCategoryList();

// classList.toggle 重複新增又移除
search.addEventListener("click", function show() {
    searchmenu.classList.toggle("show");
});


let keyword = "";
let currentPage = 0;
let nextPage;

// 無關鍵字
async function getList() {
    const postResponse = await fetch(`${originURL}/api/attractions?page=${currentPage}&keyword=${keyword}`);
    const postData = await postResponse.json();
    // 中間card
    addDataToDOM(postData);
}

// 中間card
function addDataToDOM(postData) {
    let postElement = document.createElement('div')
    postElement.setAttribute("class", "mycard");
    nextPage = postData.nextPage;
    let data = postData.data;
    let main = '';
    for (let i = 0; i <= data.length; i++) {
        let title = data[i].name;
        let mrt = data[i].mrt;
        let category = data[i].category;
        let images = data[i].images[0];
        main += `<article class="card">
                    <img class="pic" id="img" src="${images}" alt=""></img>
                    <figcaption class="desc">
                        <span id="info">${title}</span>
                    </figcaption>
                    <div class="">
                        <span class="mrt" id="mrt">${mrt}</span>
                        <span class="cardcategory" id="category">${category}</span>
                    </div>
                </article>`
        postElement.innerHTML = main;
        container.appendChild(postElement);
    }
}

getList();

// 搜尋關鍵字
async function getKeyword() {
    while (container.children.length >= 1) {
        container.removeChild(container.lastElementChild);
        console.log(container.children);
    }
    currentPage = 0;
    keyword = search.value;
    await fetch(`${originURL}/api/attractions?page=${currentPage}&keyword=${keyword}`
    ).then((response) => response.json()
    ).then(function (postData) {
        if (postData.data.length == 0) {
            // 沒有相關景點
            const postElement = document.createElement('div')
            postElement.innerHTML = `<br><br><br><br>
                            <img class="noattr" src="/static/img/noattr.JPG" alt="">
                            <br><br><br><br><br><br><br><br>`;
            container.appendChild(postElement);
        } else {
            // 中間card
            addDataToDOM(postData);
        }
    });
    search.value = "";
};

function showLoading() {
    // 載入更多
    setTimeout(getList, 250)
}

window.addEventListener('scroll', () => {
    const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
    // 卷軸高度
    // console.log({ scrollTop, scrollHeight, clientHeight });
    if (clientHeight + scrollTop >= scrollHeight - 5) {
        // 處理頁碼
        if (currentPage + 1 != nextPage) {
            return;
        } else {
            url = `${originURL}/api/attractions?page=${currentPage + 1}&keyword=${keyword}`;
            // 載入更多
            showLoading();
            currentPage++;
        }
    }
});


function debounce(fn, delay = 200) {
    let timer;
    return function () {
        window.clearTimeout(timer);
        timer = setTimeout(() => {
            fn.apply(this, arguments);
            window.clearTimeout(timer);
        }, delay);
    };
}
let debounced = debounce(function () {
    console.log("debounce");
});
window.addEventListener("resize", debounced);