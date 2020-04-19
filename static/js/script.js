var $fileInput = $('.file-input');
var $droparea = $(".file-drop-area");


var $form = $("#form");
var $results = $("#results");
var $resultsElements = $("#results-elements")
var $button = $("#button");
var $dragndrop = $("#dragndrop");
var $filename = $("#filename");
var $newfile = $("#new-file");
var filenameStr = "";

var $resultBg = $("#result-bg");

const separator = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";

// highlight drag area
$fileInput.on('dragenter focus click', function() {
    $droparea.addClass('is-active');
});

// back to normal state
$fileInput.on('dragleave blur drop', function() {
    $droparea.removeClass('is-active');
});

// change inner text
$fileInput.on('change', function() {
    let filesCount = $(this)[0].files.length;
    let $textContainer = $(this).prev();

    if (filesCount === 1) {
        // if single file is selected, show file name
        var fileName = $(this).val().split('\\').pop();
        if (fileName.endsWith(".docx") || fileName.endsWith(".doc")){
            $textContainer.text(fileName);
            filenameStr = fileName;
            $button.removeClass("hidden")
        }
        else{
            //todo: удалять неправильный файл
            //alert("Кажется, вам удалось прикрепить неверный файл. Ничего работать не будет. Обновите страницу.");
            $textContainer.text("Выберите файл .doc или .docx");
        }
    } else {
        // otherwise show number of files
        $textContainer.text("Выберите один документ");
    }
});

const wait_result_div = "<div class='spinner'><div></div><div></div></div>";
const ok_result_div = "<span class=\"animated zoomIn\"><span style=\"color: forestgreen\">&#10004;</span></span>";
const bad_result_div = "<span class=\"animated zoomIn\"><span style=\"color: darkred\">&#10006;</span></span>";
var listEntries = [];

class ListEntry{
    state;
    text;
    desc;
    constructor(root, text, desc) {
        let elem = document.createElement("li");
        this.text = text;
        this.documentID = root.appendChild(elem);
        this.state = 0;
        this.desc = desc;
        this.update();
        listEntries.push(this);
    }

    get state(){
        return this.state;
    }

    setState(newState){
        this.state = newState;
        this.update();
    }

    update(){
        let newAppearance = "";
        let newText = this.text;
        switch (this.state) {
            case 0:
            {
                newAppearance = wait_result_div;
                break;
            }
            case 1:
            {
                newAppearance = ok_result_div;
                break;
            }
            case 2:
            {
                newAppearance = bad_result_div;
                newText += " - " + this.desc;
                break;
            }
        }
        this.documentID.innerHTML = newAppearance + separator + newText;
    }

}


function fillList() {
    let root = document.getElementById("results-elements");
    for (let i = 0; i < names.length; i++){
        setTimeout(() => addElementToList(root, names[i], descs[i]), i * 5);
        //todo: remove timeout
    }
}

function addElementToList(root, item, desc){
    new ListEntry(root, item, desc);
}

// 0 - wait
// 1 - ok
// 2 - bad
function setDotAppearance(dotInd, newstate){
    listEntries[dotInd].setState(newstate);
}



$button.click(function(e) {
    e.preventDefault();
    // validate file
    // alert("КОД КРАСНЫЙ");
    $dragndrop.addClass('hidden');
    $results.removeClass('hidden');
    $filename.removeClass('hidden');
    $button.addClass('hidden');
    $newfile.removeClass('hidden');
    $filename.text(filenameStr);
    SendFile();
});

$newfile.click(function(e) {
    e.preventDefault();
    location.reload();
    return false;
});


// ========================================================================
let names = [
    "Шрифт",
    "Поля",
    "Названия таблиц",
    "Названия рисунков",
    "Заголовки"
];

let descs = [
    "должен быть Times New Roman, 14",
    "должны быть: слева - 3 см, остальные - 2 см",
    "должны быть выполнены слева сверху над таблицей",
    "должны быть по центру под рисунком",
    "должны быть по центру без точки на конце"
];

fillList(names, descs);

// 0 - wait
// 1 - ok
// 2 - bad

function SendFile() {
    // https://demo2398178.mockable.io
    var fd = new FormData(document.querySelector("form"));
    // fd.append("CustomField", "This is some extra data");
    $.ajax({
        // url: "https://6f412c5e-e568-4592-bcde-2f9f011ad67a.mock.pstmn.io",
        // url: "https://demo2398178.mockable.io/",
        url: window.location.href,
        type: "POST",
        data: fd,
        processData: false,  // tell jQuery not to process the data
        contentType: false,
        success: function (data, status, _) {
            if (typeof data === "string") {
                data = JSON.parse(data);
            }
            let ok = true;
            for (let i = 0; i < data.length; i++){
                if (data[i] === 2){
                    ok = false;
                }
                setTimeout(() => listEntries[i].setState(data[i]), i * 200);
            }
            setTimeout(() => updateBackground(ok), data.length * 200 + 150)

        },
        error: function (xhr, textStatus, errorThrown) {
            if (textStatus === "BAD REQUEST"){
                // TODO: сделать красивое сообщение
                alert("Отправленный вами файл не соответствует требованиям")
            }
            else{
                console.log(errorThrown);
                console.log(textStatus);
                alert("Ошибка. Скорее всего, это проблемы с соединением.");
            }
            //это для обновления страницы
            location.reload(false);
            return false;
            //============================
        },
        timeout: 15000
    });
}


function updateBackground(ok) {
    if (ok){
        $resultBg.addClass("green-bg")
    }
    else{
        $resultBg.addClass("red-bg")
    }
}