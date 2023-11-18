const addBtn = document.querySelector(".add");

const input = document.querySelector(".inp-group");


function addInput(){
    const name = document.createElement("input");
    name.type ="text";
    name.placeholder = "Enter your name";

    const email = document.createElement("input");
    email.type ="text";
    email.placeholder = "Enter your name";
    
    const btn = document.createElement("a");
    btn.className ="delete";
    btn.innerHTML = "&times";

    const flex = document.createElement("div");
    flex.className = "flex";

    input.appendChild(flex);
    flex.appendChild(name);
    flex.appendChild(email);
    flex.appendChild(btn);

}

addBtn.addEventListener("click", addInput);