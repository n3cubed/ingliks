const input = document.getElementById('translation-input');
const output = document.getElementById('translation-output');
// const feedback = document.getElementById('feedback');
const warning = document.getElementById('warning');
const pronunciation_guide = document.getElementById('pronunciation-guide');
const info = document.getElementById('info');
const copy_elements = document.getElementsByClassName('copy');
const feedback = document.getElementById('feedback');

function copy_to_clipboard(value) {
    navigator.clipboard.writeText(value);
}


// auto_grow(input);
// auto_grow(output);
function translate_now() {
   let input_value = input.value.toLowerCase();
   // input_value = input_value.replace(/[.,\/#?!$@%\^&\*;:{}'=\-_`~()]/g,"")
   // input_value = input_value.replace(/\s{2,}/g," ");
   // input.value = input_value;
   fetch('./translate', {
      method: 'POST',
      body: JSON.stringify({'text': input_value}),
      headers: {
         'Content-Type': 'application/json'
      }
   })
     .then(response => response.json())
     .then(data => {
         output.value = data.translation;
         auto_grow(output);
         if (data.not_in_dict.length > 0) {
         let plural;
            if (data.not_in_dict.length > 1)
               warning.textContent = data.not_in_dict.slice(0, -1).join(', ') +
             ' and ' + data.not_in_dict[data.not_in_dict.length - 1] +
             ' are not in our database.';
            else
               warning.textContent = data.not_in_dict +
               ' is not in our database.';
            warning.style.display = "block"
         } else {
            warning.style.display = "none";
            warning.textContent = "";
         }
     })
     .catch((error) => {
            warning.textContent = "Server Error: ";
            warning.style.display = "block"
     });
}

let pronunciation_guide_html = "";
let info_html = "";

fetch('./pronunciation_guide')
    .then(response => response.json())
    .then(data => {
        let pronunciation_guide_text = data.pronunciation_guide;
        pronunciation_guide_html = parseToHTML(pronunciation_guide_text);
        pronunciation_guide.innerHTML = pronunciation_guide_html;
    })
    .catch((error) => {
        pronunciation_guide_html = "<div class='subsection-title'>?</div><div class='subsection-text'>???</div>";
        pronunciation_guide.innerHTML = pronunciation_guide_html;
        console.log(error);
    });

fetch('./info')
    .then(response => response.json())
    .then(data => {
        let info_text = data.info;
        info_html = parseToHTML(info_text);
        info.innerHTML = info_html;
    })
    .catch((error) => {
        info_html = "<div class='subsection-title'>?</div><div class='subsection-text'>???</div>";
        info.innerHTML = info_html;
    });

function toggle_section(section_title) {
    section_text = section_title.nextElementSibling.nextElementSibling;
    console.log(section_text.style.height);
    if (section_text.style.height === "0px") {
        section_text.style.opacity = "1";
        section_text.style.height = "max-content";
        section_text.style.transform = "translateY(0px)";
        section_text.style.pointerEvents = "auto";
        section_text.style.overflow = "auto";
        section_title.getElementsByClassName("expand-arrow")[0].style.transform = "rotate(180deg)";
    } else {
        section_text.style.height = "0";
        section_text.style.opacity = "0";
        section_text.style.transform = "translateY(-20px)";
        section_text.style.pointerEvents = "none";
        section_text.style.overflow = "hidden";
        section_title.getElementsByClassName("expand-arrow")[0].style.transform = "rotate(0deg)";
    }
}

function parseToHTML(text) {
    // replace copy(text) with <div class="copy">
    text = text.replace(/copy\((.*?)\)/g, "<span class='copy' onclick='copy_to_clipboard(this.innerText)'>$1</span>");


    // replace [title]\n with <div class="subsection-title">
    text = text.replace(/\[(.*?)\]\n/g, "<div class='subsection-title'>$1</div>");
    /* replace
        /start\n
        text
        \n/end\n
    with <div> */
    text = text.replace(/\/start\n([\s\S]*?)\n\/end\n/g, "<div class='subsection-text'>$1</div>");
    /* get
        /pillar_start\n
        text
        \n/pillar_end\n
    */
    let match = text.match(/\/pillar_start\n([\s\S]*?)\/pillar_end\n/);
    let pillar_text = match && match[1] ? match[1] : '';
    /* replace
        left - right\n
    */
    pillar_text = pillar_text.replace(/(.*?)-(.*?)\n/g, function(_, group1, group2) {
        return "<div class='pillar-row'><div class='pillar-left'>" + group1 + "</div><div class='pillar-right'>" + group2.trim() + "</div></div>";
    });

    text = text.replace(/\/pillar_start\n[\s\S]*?\n\/pillar_end\n/g, `<div class="pillar-container">${pillar_text}</div>`);

    // replace `text` with <span class="funny-text">
    text = text.replace(/\`(.*?)\`/g, "<span class='funny-text'>$1</span>");
    // replace *word* with <b>
    text = text.replace(/\*(.*?)\*/g, "<b>$1</b>");
    // replace \n with <br> - put this at the end
    text = text.replace(/\n/g, "<br>");

    return text;
}


function send_feedback() {
  feedback_text = feedback.value.trim();
  if (feedback_text.length = 0) return;
  feedback.value = "";
  fetch("./feedback",  {
       method: 'POST',
       body: JSON.stringify({'feedback': feedback_text}),
       headers: {
          'Content-Type': 'application/json'
       }
    })
    .then(_ => {
        console.log("feedback sent")
    })
    .catch((error) => {
        console.log("feedback failed to send")
    })
  }

function auto_grow(element) {
  element.style.height = "0px"
  element.style.height = (element.scrollHeight) + 2 * +getComputedStyle(element)
    .borderTopWidth.slice(0,-2) + "px";
}

function clear_field() {
   warning.style.display = "none";
   warning.textContent = "";
   input.value = '';
   output.value = '';
   auto_grow(input);
   auto_grow(output);
}