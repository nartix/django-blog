export default () => ({
  menuOpen: false,

  init() {
    this.setResizeListener();
  },

  setResizeListener() {
    window.addEventListener('resize', () => {
      if (window.innerWidth > 768) {
        this.menuOpen = false;
      }
    });
  },
});
