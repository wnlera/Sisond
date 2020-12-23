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

// var timeout_t = 15000;
var timeout_t = 99999999;

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
            //todo: проверять размер файла перед отправкой - не более 25 мб
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
const info_result_div = "<span id='result-link'></span>"
var listEntries = [];

class ListEntry{
    state;
    text;
    desc;
    constructor(root, text, desc, state) {
        let elem = document.createElement("li");
        this.text = text;
        this.documentID = root.appendChild(elem);
        this.state = state;
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
            case 3:
            {
                newAppearance = info_result_div;
                break;
            }
            case -1:
            {
                newAppearance = "";
                break;
            }
        }
        this.documentID.innerHTML = newAppearance + separator + newText;
    }

}


function fillList() {
    let root = document.getElementById("results-elements");
    for (let i = 0; i < names.length; i++){
        addElementToList(root, names[i], descs[i], 0)
    }
    // todo: bad spacers
    addElementToList(root,"","",-1)
    addElementToList(root,"","",-1)
    addElementToList(root,"","",-1)
    addElementToList(
        root,
        "",
        "",
        3)
}

function addElementToList(root, item, desc, state){
    new ListEntry(root, item, desc, state);
}

// 0 - wait
// 1 - ok
// 2 - bad
// 3 - info
// -1 - empty
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
    "Автосодержание",
    "Поля",
    "Шрифт",
    "Выравнивание",
    "Междустрочный интервал",
    "Названия таблиц",
    "Названия рисунков"
];

let descs = [
    "в документе должно быть автосодержание, без него проверка может осуществляться некорректно",
    "должны быть: левое - 3 см, правое - 1, верхнее и нижнее - 2 см",
    "должен быть Times New Roman",
    "должно быть у заголовков и названий рисунков по центру, у всего остального текста по ширине",
    "должен быть 1.5",
    "должны быть выполнены сверху над таблицей с выравниванием по ширине без абзацного отступа в формате \"Таблица 1.1 - Название\"",
    "должны быть по центру под рисунком в формате \"Рисунок 1.2 - Название\"",
];

fillList(names, descs);

// 0 - wait
// 1 - ok
// 2 - bad
// 3 - info

function setLink(link) {
    console.log("setlink: " + link)
    link_obj = document.createElement("a");
    link_obj.textContent = "Скачать детализированный отчёт";
    link_obj.href = "//" + link;
    document.getElementById("result-link").appendChild(link_obj);
}

function SendFile() {
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
            console.log(data)

            for (let i = 0; i < data["results"].length; i++){
                setTimeout(() => listEntries[i].setState(data["results"][i]), i * 200);
            }
            setTimeout(() => setLink(data["fileUrl"]), data["results"].length * 210);
            // setTimeout(() => updateBackground(ok), data.length * 200 + 150)

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
        timeout: timeout_t
    });
}


// function updateBackground(ok) {
//     if (ok){
//         $resultBg.addClass("green-bg")
//     }
//     else{
//         $resultBg.addClass("red-bg")
//     }
// }