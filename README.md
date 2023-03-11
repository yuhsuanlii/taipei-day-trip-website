# Taipei Day-trip 📍

Taipei Daytrip is a e-commerce tourism website.
Adopt the development method of separating Front-End and Back-End, connect the Restful API in series, and use AJAX to obtain about 50+ public scenic spot information. 
Click on the photo of the scenic spot information to view more information, and make an appointment for travel and payment by TapPay SDK.

台北一日遊是一個電商旅遊網站。
採用前後端分離開發，串聯 Restful API 並使用 AJAX 獲取約50多筆公共景點資料。
點擊景點照片以查看更多細節，也可預定旅遊日期時段並通過 TapPay SDK 第三方支付付款。

![Desktop - 3 (1)](https://user-images.githubusercontent.com/101781321/224505193-7e062666-4162-4cad-b5e2-1efe26e5290a.png)

## Live DEMO

http://100.20.194.8:3000/

<br/>

## Test Account

You can preview the information related to attractions upon entering the website. 
If you want to book a trip on a specific date and time, you will need to login first. 
Here are the test account and password.

進入網站即可預覽景點相關資訊，若想要預定行程日期及時段，需要登入才可以使用。以下是測試帳號及密碼。

| Account | Password |
|-----|--------|
| test@test.com | test1234 |

| Card Number | Valid Date | CVV |
|-----|--------|--------|
| 4242 4242 4242 4242 | 01/24 | 123 |

<br/>

## Skills Structure

In front-end development, based on the guidelines with ```Figma```, try to enhance fundamental skills by using pure ```HTML```, ```CSS```, and ```JavaScript``` for layout design. 
At first, Write an additional independent ```Python``` program to store the attraction data in ```MySQL``` database.
```Python Flask``` was used as the back-end framework, the project adopts a development method that separation of front-end and back-end. 
According to the ```Request``` method sent by the front-end, data was obtained from the back-end using ```AJAX``` technology and returned in ```JSON``` format through ```RESTful API```.

The project taked 8 weeks of intensive development.
After the weekly development is completed, will sent ```Pull Request``` to the ```Reviewer```, and after obtaining consent, the ```develop``` branch will be merged into the ```main``` branch, and the code will be synchronized to the ```AWS EC2``` computer update website.

在前端開發根據引導文件提供的 Figma 規劃，使用基礎的 HTML、CSS、JavaScript 進行切版加強鍛鍊基本功。
一開始需要額外寫⼀隻獨立的 Python 程式統⼀將景點資料先存放到 MySQL 資料庫中。
使用 Python Flask 作為後端框架，採用前後端分離的方式，
根據前端發送的 Request 方法，使用 AJAX 技術從後端獲取數據，通過 RESTful API 回傳 JSON 格式的資料。

連續八週密集開發，使用 Git/GitHub 進行版本控管，
每週完成階段性任務後，向 Reviewer 發送 Pull Request，取得同意後將 develop 分支合併到 main 分支，並將程式碼同步到 AWS EC2 更新網站。

<br/>

## RESTful API

Developed using the RESTful API method based on the guideline.

根據說明文件要求，使用 RESTful API 進行開發。

<img src=https://user-images.githubusercontent.com/101781321/224511570-9121ecd0-4d16-48dc-a746-593b6f278aa6.JPG width=80% />


## Database Schema

<img src=https://user-images.githubusercontent.com/101781321/224508944-735d46ae-f134-436f-bdf1-3981650c94af.JPG width=50% />


## Features

### 📜 Infinite Scroll & Lazy Loading
<img src=https://user-images.githubusercontent.com/101781321/224511319-804eeb29-c602-49ab-9b64-beb61e488998.gif width=80% />
<br/>

### 🔎 Keyword Search
<img src=https://user-images.githubusercontent.com/101781321/224511341-73e4ede1-e9d2-40c4-8ff7-d19d1e8d47dc.gif width=80% />
<br/>

### 💁‍♂️ Member System
<img src=https://user-images.githubusercontent.com/101781321/224511352-2e8bda11-fb7e-4d14-9804-9ab07c439d94.gif width=80% />
<br/>

### 🎠 Carousel & Attraction Detail
<img src=https://user-images.githubusercontent.com/101781321/224511363-22d56d1a-82fa-4594-b59d-4fe55ec9c0e7.gif width=80% />
<br/>

### 💳 Booking & TapPay SDK
<img src=https://user-images.githubusercontent.com/101781321/224511369-679c2953-9104-44b1-914d-f5142904d243.gif width=80% />
<br/>

### 📋 Order History
<img src=https://user-images.githubusercontent.com/101781321/224511370-229a67ce-78d3-4c39-bd0f-f32c54bc80ce.gif width=80% />
<br/>

### 📱 Responsive Web Design (RWD)
<img src=https://user-images.githubusercontent.com/101781321/224511372-95c42881-1571-411f-9a2f-411c4c373d5d.gif width=80% />
<br/>




***  

_Thanks for your reading & have a nice day 🌞_

