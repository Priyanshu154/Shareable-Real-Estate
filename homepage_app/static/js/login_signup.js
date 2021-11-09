function isHidden() {
    navigate = document.getElementsByName('btn')[0];

  if (navigate.value == "Login"){
    let label = document.getElementsByName('label')[0];
    let pass2 = document.getElementsByName('pass2')[0];

    label.style.display  = "none";
    pass2.style.display  = "none";

  }
    console.log("hello");
}
