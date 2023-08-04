// 画像が保存されているディレクトリ
const dir = 'img/';

// 最後に表示された画像のインデックス
let lastIndex = null;

// JSONファイルから読み込んだ画像情報のリスト
let imageList = [];

// JSONファイルを読み込む関数
function loadImageList() {
    fetch('./data.json')
        .then(response => response.json())
        .then(data => {
            imageList = data;
            changeImage();
        })
        .catch(error => console.error('Error:', error));
}

// 画像を変更する関数
function changeImage() {
    let randIndex;

    // 画像のリストが1枚以上で、かつ前回と異なる画像を選ぶようにする
    do {
        randIndex = Math.floor(Math.random() * imageList.length);
    } while (imageList.length > 1 && randIndex === lastIndex)

    const imgPath = dir + imageList[randIndex].png_name;

    const imgElement = document.getElementById('photo');
    imgElement.style.right = '100%';
    setTimeout(() => {
        // 画像のソースを更新
        imgElement.src = imgPath;
        imgElement.style.right = '0';

        // 画像名を表示
        document.getElementById('photoName').innerText = imageList[randIndex].raw_text;

        // 最後に表示された画像のインデックスを保存
        lastIndex = randIndex;

        countdown(20); // Start the countdown

        // 15秒後に再度画像を変更
        setTimeout(changeImage, 20000);
    }, 1000);
}

function countdown(seconds) {
    let counter = seconds;
    const countdownElement = document.getElementById('countdown');
    countdownElement.innerText = counter;
    const intervalId = setInterval(() => {
        counter--;
        if (counter < 0) {
            clearInterval(intervalId);
            countdownElement.innerText = '';
        } else {
            countdownElement.innerText = counter;
        }
    }, 1000);
}

// ページの読み込みが完了したら初期化
window.onload = function() {
    loadImageList(changeImage);

    // 以降、1分ごとに再度JSONファイルをロード
    setInterval(() => {
        loadImageList();
    }, 60000); // 60000ミリ秒 = 1分
};
