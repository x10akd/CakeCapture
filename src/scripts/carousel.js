function carousel() {
  return {
    currentIndex: 0,
    slides: [],
    totalSlides: 0,
    init() {
      this.slides = document.querySelectorAll('.carousel-slide');
      this.totalSlides = this.slides.length;
      this.showSlide(this.currentIndex);
      setInterval(() => {
        this.nextSlide();
      }, 3000);
    },
    showSlide(index) {
      this.currentIndex = index;
    },
    nextSlide() {
      this.currentIndex = (this.currentIndex + 1) % this.totalSlides;
    },
    prevSlide() {
      this.currentIndex = (this.currentIndex - 1 + this.totalSlides) % this.totalSlides;
    }
  }
}


export { carousel }