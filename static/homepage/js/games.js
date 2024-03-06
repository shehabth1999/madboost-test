/*=============== SWIPER JS ===============*/
let gamesSwiperCards = new Swiper('.games-swiper', {
  loop: true,
  spaceBetween: 32,
  grabCursor: true,

  navigation: {
    nextEl: '.games-swiper-button-next',
    prevEl: '.games-swiper-button-prev',
  },

  breakpoints: {
    700: {
      slidesPerView: 2,
    },
    810: {
      slidesPerView: 4,
    },
    1200: {
      slidesPerView: 6,
    },
  },

});