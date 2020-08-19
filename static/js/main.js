$(document).ready(function () {


// similar-contest slider

$('.similar_slider_area').owlCarousel({
  loop: true,
  margin: 20,
  dots:false,
  autoplay:true,
  autoplayHoverPause: true,
  nav: true,
  navText: ['<i class="fas fa-angle-left"></i>', '<i class="fas fa-angle-right"></i>'],
  responsive: {
    0: {
      items: 1
    },
    600: {
      items: 3
    },
    1000: {
      items: 3
    }
  }
})

// judge slider

$('.judge_slider_area').owlCarousel({
  loop: true,
  margin: 20,
  dots:false,
  autoplay:true,
  autoplayHoverPause: true,
  nav: true,
  navText: ['<i class="fas fa-angle-left"></i>', '<i class="fas fa-angle-right"></i>'],
  responsive: {
    0: {
      items: 1
    },
    600: {
      items: 3
    },
    1000: {
      items: 4
    }
  }
})

// home page main slider
  $('.home_slider_active').owlCarousel({
    loop: true,
    margin: 0,
    nav: false,
    autoplay:true,
    autoplayHoverPause: true,
    responsive: {
      0: {
        items: 1
      },
      600: {
        items: 1
      },
      1000: {
        items: 1
      }
    }
  })






});