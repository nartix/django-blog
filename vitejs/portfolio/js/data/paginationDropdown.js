export default () => ({
  showPaginationDropdown: false,
  showMobilePaginationDropdown: false,
  togglePaginationDropdown() {
    this.showPaginationDropdown = !this.showPaginationDropdown;
  },
  toggleMobilePaginationDropdown() {
    this.showMobilePaginationDropdown = !this.showMobilePaginationDropdown;
  },
  resetPaginationDropdown() {
    this.showPaginationDropdown = false;
    this.showMobilePaginationDropdown = false;
  },
});
