const clamp = (value, min = 0, max = 100) => Math.min(Math.max(value, min), max);

export default class ProgressBar {
  constructor(elementId) {
    this.elementId = elementId;
  }

  async startOrAdvance(targetIncrement = 10, timeIncrement = 6, incrementBy = 1) {
    // must get new reference on each call
    // otherwise it won't work if an user clicks the back/forward button.
    let element = document.getElementById(this.elementId);
    let currentWidth = parseInt(element.style.width, 10) || 0;
    const targetWidth = clamp(currentWidth + targetIncrement);

    for (; currentWidth < targetWidth; currentWidth += incrementBy) {
      await this.incrementWidth(currentWidth, timeIncrement);
    }

    if (currentWidth >= 100) this.reset();
  }

  incrementWidth(currentWidth, timeIncrement) {
    let element = document.getElementById(this.elementId);
    return new Promise((resolve) => {
      setTimeout(() => {
        element.style.width = `${currentWidth + 1}%`;
        resolve();
      }, timeIncrement);
    });
  }

  reset() {
    let element = document.getElementById(this.elementId);
    element.style.width = '0%';
    element.style.opacity = '1';
  }
}
