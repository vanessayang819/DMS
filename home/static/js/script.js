window.onload = function(){
  $(".button-collapse").sideNav();
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //Jan 0
  var yyyy = today.getFullYear();
   if(dd<10){
          dd='0'+dd
      }
      if(mm<10){
          mm='0'+mm
      }

  today = yyyy+'-'+mm+'-'+dd;
  if(document.getElementById("following_date")){
    document.getElementById("following_date").setAttribute("min", today);
  }


};
