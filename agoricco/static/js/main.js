var root = null;
var useHash = false; // Defaults to: false
var hash = '#!'; // Defaults to: '#'
var router = new Navigo(root, useHash, hash);

// Variables for clock and coordinates
var time,
    gmt;
var y = document.getElementById("clock");
var x = document.getElementById("coords");

// Global size variables
var windowWidth = $(window).width();
var windowHeight = $(window).height();
var headerHeight = $("header").height() + 24; /* top margin: 2rem */
var navHeight = $("nav").height();
var elementsOnScreen;
var contentWindowHeight;

// Update size variables on resize
$(window).resize(function() {
  windowWidth = $(window).width();
  windowHeight = $(window).height();
  headerHeight = $("header").height() + 24; /* top margin: 2rem */
  navHeight = $("nav").height();
});

function openContentSection(section) {
  $(".content").remove();
  $(".drawer").removeClass("active");
  if (!$(".menu-items").hasClass("active")) {
    toggleMobileMenu();
  }
  var $contentSection = $("#" + section);
  $contentSection.toggleClass("active");
}

router
  .on({
    'about': function () {
      section = 'about';
      openContentSection(section);
    },
    'witness-proposal': function () {
      section = 'witness-proposal';
      openContentSection(section);
    },
    'faucet': function () {
      section = 'faucet';
      openContentSection(section);
    },
    '*': function (){
      $(".flash > .message").text("");
      $(".drawer").removeClass("active");
    }
  })
  .resolve();

function toggleMobileMenu() {
  $(".content").remove();
  $('.menu-items').toggleClass('active');
  var t = $(".collapse-button").find('button');
  if(t.text() == 'Menu') {
    t.text('Close');
  } else {
    t.text('Menu');
  }
  elementsOnScreen = navHeight + headerHeight;
  contentWindowHeight = windowHeight - elementsOnScreen;
}

$('.collapse-button').on('click', function() {
  toggleMobileMenu();
  router.navigate("");
});

$('.video').click(function(event) {
  router.navigate("");  
});

// Click menu item event
$('.nav').find('a').on('click', function(e) {
  router.navigate($(this).data("target"));
});

$('.revealer').click(function (e) {
  if ($(this).siblings('input')[0].type == "password") {
    $(this).siblings('input')[0].type = "text";
    $(this).removeClass('revealer');
    $(this).addClass('hider');
    $(this).val("Hide");
  } else {
    $(this).siblings('input')[0].type = "password";
    $(this).removeClass('hider');
    $(this).addClass('revealer');
    $(this).val("Reveal");
  }
});

var account_name = null;
var password = null;
var pubKeys = null;

var handleFaucetResponse = function (data) {
  var $message = $(".flash > .message");
  switch (data.status) {
    case "error":
      $message.addClass("error");
      $message.text(data.message);
      break;
    case "success":
      $(".account_name").text(account_name);
      $("#password").val(password);
      new Clipboard('#password-clipboard', {
          text: function(trigger) {
              return password;
          }
      });
      var private_keys = steem.auth.getPrivateKeys(account_name, password, ['posting']);
      $("#private_posting_key").val(private_keys['posting']);
      new Clipboard('#private-posting-key-clipboard', {
          text: function(trigger) {
              return private_keys['posting'];
          }
      });
      $("#faucet-form").hide();
      $("#account-registered").show();
      break;
    case "info":
      $message.addClass("info");
      $message.text(data.message);
      break;
    case "unknown":
      $message.addClass("error");
      $message.text("An unknown issue has occurred. Please try again later.")
      break;
  }
}

$("#redemption-form").on('submit', function(event) {
  event.preventDefault();
  $("#redemption-form > [name='register']").attr('disabled', 'disabled');
  account_name = $(this).children('[name="account_name"]').val();
  var code = $(this).children('[name="code"]').val();
  var referrer = $(this).children('[name="referrer_account"]').val();
  var csrf_token = $(this).children('[name="_csrf_token"]').val();
  password = steem.formatter.createSuggestedPassword();
  pubKeys = steem.auth.generateKeys(account_name, password, ['owner', 'active', 'posting', 'memo']);
  $.post('/faucet', { 
    'account_name': account_name,
    'owner_key': pubKeys['owner'],
    'active_key': pubKeys['active'],
    'posting_key': pubKeys['posting'],
    'memo_key': pubKeys['memo'],
    'code': code,
    'referrer': referrer,
    '_csrf_token': csrf_token,
  }, handleFaucetResponse)
  .always(function (data) {
    $("#redemption-form > [name='register']").removeAttr('disabled');
  });
  event.stopImmediatePropagation();
  return false;
});
