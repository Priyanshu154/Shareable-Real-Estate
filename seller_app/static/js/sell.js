function isVisible(){

  var x = document.getElementById('type');

  if(x.value === "RK"){
    document.getElementById('bhk1').style.display = 'none';
    document.getElementById('bhk2').style.display = 'none';
  }
  else{
    document.getElementById('bhk1').style.display = 'block';
    document.getElementById('bhk2').style.display = 'block';
  }

}
