function hideMobileMenu() {
  $(".three-o").css('height', '100%');
  $("nav").hide();
}

function showMobileMenu() {
  $(".three-o").css('height', '70vh');
  $("nav").show();
}

$(".text-input").focus(function(event) {
  hideMobileMenu();
});

$(".text-input").blur(function(event) {
  showMobileMenu();
});
