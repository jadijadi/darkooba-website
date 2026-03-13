$(document).ready(function(){

	$('.js-calender-slide').slick({
		arrows: false,
		dots: true,
		infinite: true,
		speed: 600,
		slidesToShow: 1,
		slidesToScroll: 1,
		autoplay: true,
  		autoplaySpeed: 2500,
		pauseOnHover: false
	});

	$('.js-slider-dotted').slick({
		arrows: false,
		dots: true,
		infinite: true,
		speed: 600,
		slidesToShow: 1,
		slidesToScroll: 1,
		autoplay: true,
  		autoplaySpeed: 2500,
  		variableWidth: true,
  		centerMode: true
	});

	$('.js-home-header-slide').slick({
		arrows: false,
		dots: true,
		infinite: true,
		speed: 600,
		slidesToShow: 1,
		slidesToScroll: 1,
		autoplay: true,
  		autoplaySpeed: 2500,
		pauseOnHover: false
	});

	// slider for lanscape and portrait photos with thumbnails

	$('.slider-for').slick({
		centerMode: true,
		speed: 600,
		arrows: false,
		variableWidth: true,
		asNavFor: '.slider-nav'
	});

	$('.slider-nav').slick({
		arrows: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		centerMode: true,
		variableWidth: true,
		centerPadding: '30px',
		focusOnSelect: true,
		asNavFor: '.slider-for',
	});

	// slider for only lanscape photos

	$('.js-slider-landscape').slick({
		slidesToShow: 1,
		slidesToScroll: 1,
		speed: 600,
		arrows: false,
		asNavFor: '.js-slider-landscape-nav'
	});

	$('.js-slider-landscape-nav').slick({
		arrows: true,
		slidesToShow: 3,
		slidesToScroll: 1,
		centerMode: true,
		variableWidth: true,
		centerPadding: '30px',
		focusOnSelect: true,
		asNavFor: '.js-slider-landscape',
	});


});