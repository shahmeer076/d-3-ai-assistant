let selectedVoice = null;


// ================= LOAD FEMALE VOICE =================

function loadVoice(){

    let voices = window.speechSynthesis.getVoices();


    selectedVoice = voices.find(

        voice =>
        voice.name.includes("Samantha") ||
        voice.name.includes("Zira") ||
        voice.name.includes("Female") ||
        voice.name.includes("Google UK English Female")

    );


    // Agar female voice na mile to pehli available voice use hogi

    if(!selectedVoice && voices.length > 0){

        selectedVoice = voices[0];

    }


}



window.speechSynthesis.onvoiceschanged = loadVoice;

loadVoice();




// ================= SEND MESSAGE =================


function sendMessage(){


    let input = document.getElementById("message");


    let message = input.value.trim();



    if(message === "")
    {
        return;
    }




    let chat = document.getElementById("chat-box");



    chat.innerHTML +=

    `
    <div class="user-message">
        ${message}
    </div>
    `;



    input.value = "";




    fetch("/chat",{


        method:"POST",


        headers:{

            "Content-Type":"application/json"

        },


        body:JSON.stringify({

            message:message

        })


    })



    .then(response => response.json())



    .then(data => {



        chat.innerHTML +=


        `
        <div class="ai-message">
            ${data.reply}
        </div>
        `;



        speakAI(data.reply);



        chat.scrollTop = chat.scrollHeight;



    })



    .catch(error => {


        console.log(error);



        chat.innerHTML +=


        `
        <div class="ai-message">
            Error connecting to AI
        </div>
        `;


    });



}






// ================= VOICE INPUT =================



function startListening(){



    if(!('webkitSpeechRecognition' in window))
    {

        alert(
            "Chrome browser required for voice recognition"
        );

        return;

    }




    let recognition = new webkitSpeechRecognition();



    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.lang = "en-US";




    recognition.onstart = function(){


        console.log("Listening...");


    };





    recognition.onresult = function(event){



        let text =
        event.results[0][0].transcript;




        document.getElementById("message").value = text;



        sendMessage();



    };





    recognition.onerror = function(event){



        console.log(
            "Voice Error:",
            event.error
        );



        alert(
            "Voice Error: " + event.error
        );



    };




    recognition.start();



}






// ================= AI VOICE OUTPUT =================



function speakAI(text){



    // Pehle se chal rahi voice stop kare

    window.speechSynthesis.cancel();




    let speech = new SpeechSynthesisUtterance(text);



    speech.lang = "en-US";


    speech.rate = 1;


    speech.pitch = 1;




    if(selectedVoice){


        speech.voice = selectedVoice;


    }





    window.speechSynthesis.speak(speech);



}
// ================= LOAD CHAT HISTORY =================


function loadHistory(){


    fetch("/history")


    .then(response => response.json())


    .then(data =>{


        let historyBox = document.getElementById("history");


        historyBox.innerHTML="";



        Object.keys(data).reverse().forEach(title => {



            let button = document.createElement("button");



            button.innerHTML = title;



            button.onclick = function(){


                openChat(data[title]);


            };



            historyBox.appendChild(button);



        });



    });



}





// ================= OPEN OLD CHAT =================


function openChat(messages){



    let chat = document.getElementById("chat-box");



    chat.innerHTML="";




    messages.forEach(msg => {



        if(msg.sender=="You"){


            chat.innerHTML +=


            `

            <div class="user-message">

            ${msg.message}

            </div>

            `;


        }


        else{


            chat.innerHTML +=


            `

            <div class="ai-message">

            ${msg.message}

            </div>

            `;


        }



    });



    chat.scrollTop = chat.scrollHeight;



}







// ================= NEW CHAT =================



function newChat(){



    let chat=document.getElementById("chat-box");



    chat.innerHTML=



    `

    <div class="ai-message">

    New chat started. How can I help you?

    </div>

    `;



}





// Load history when page opens

window.onload=function(){


    loadHistory();


};