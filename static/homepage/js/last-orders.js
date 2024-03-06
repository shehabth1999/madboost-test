/*=============== SWIPER JS ===============*/
let lastOrdersSwiperCards = new Swiper('.last-orders-swiper', {
  loop: true,
  spaceBetween: 32,
  grabCursor: true,

  navigation: {
    nextEl: '.last-orders-swiper-button-next',
    prevEl: '.last-orders-swiper-button-prev',
  },

  breakpoints: {
    700: {
      slidesPerView: 1,
    },
    810: {
      slidesPerView: 2,
    },
    1200: {
      slidesPerView: 3,
    },
  },

});