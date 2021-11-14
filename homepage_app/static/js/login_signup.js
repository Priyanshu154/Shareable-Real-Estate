function isHidden() {
    navigate = document.getElementsByName('btn')[0];

  if (navigate.value == "Login"){
    let labels = document.getElementsByName('label')[0];
    let pass2 = document.getElementsByName('pass2')[0];
    let one1  = document.getElementById('1');
    let one2  = document.getElementById('2');
    let one3  = document.getElementById('3');
    let one4  = document.getElementById('4');
    let one5 = document.getElementById('5');
    let one6 = document.getElementById('6');

    labels.style.display  = "none";
    pass2.style.display  = "none";
    one1.style.display  = "none";
    one2.style.display  = "none";
    one3.style.display  = "none";
    one4.style.display  = "none";
    one5.style.display  = "none";
    one6.style.display  = "none";

  }
    console.log("hello");
}
