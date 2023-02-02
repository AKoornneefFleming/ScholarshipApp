       
// Javascript from w3 schools
// https://www.w3schools.com/howto/tryit.asp?filename=tryhow_js_navbar_slide
// When the user scrolls down 20px from the top of the document, slide down the navbar 

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("navbar").style.top = "0";
  } else {
    document.getElementById("navbar").style.top = "-60px";
  }
}
