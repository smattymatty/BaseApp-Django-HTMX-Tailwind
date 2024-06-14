export class Modal {
  constructor(modalId, options = {}) {
    this.modalId = modalId;
    this.modal = document.getElementById(modalId);
    this.backdrop = document.getElementById(`${modalId}-backdrop`);
    this.showButton = document.getElementById(`${modalId}-button`);
    this.class = options.class || "hidden";
    this.delayedClass = options.delayedClass || "opacity-0";
    this.delay = options.delay || 100;
    this.closeButton = document.getElementById(`${modalId}-close`);
    this.init();
  }
  init() {
    if (!this.modal) {
      console.error(`Modal with ID "${this.modalId}" not found in the DOM.`);
      return; // Exit early if modal is not found
    }
    console.log(`Initializing modal with ID "${this.modalId}"`);
    if (this.closeButton) {
      this.closeButton.setAttribute("aria-label", "Close");
      this.closeButton.addEventListener("mousedown", () => {
        this.delayHideModal();
      });
    } else {
      console.error(
        `Modal with ID "${this.modalId}" does not have a close button. Please add a close button with the ID "${this.modalId}-close".`
      );
    }
    if (this.backdrop) {
      this.backdrop.addEventListener("mousedown", () => {
        this.delayHideModal();
      });
    } else {
      console.error(
        `Modal with ID "${this.modalId}" does not have a backdrop. Please add a backdrop with the ID "${this.modalId}-backdrop".`
      );
    }
    if (this.showButton) {
      this.showButton.setAttribute("role", "button");
      this.modal.setAttribute("aria-labelledby", this.showButton.id);
      this.showButton.addEventListener("mousedown", () => {
        this.showModal();
      });
    } else {
      console.error(
        `Modal with ID "${this.modalId}" does not have a show button. Please add a show button with the ID "${this.modalId}-button".`
      );
    }
    if (this.modal) {
      this.modal.setAttribute("role", "dialog");
      this.modal.setAttribute("aria-modal", "true");
      this.modal.addEventListener("mousedown", (event) => {
        event.stopPropagation(); // Prevent event from bubbling up to backdrop
      });
    }
  }
  showModal() {
    console.log(`Showing modal with ID "${this.modalId}"`);
    this.backdrop.classList.remove(this.class);
    this.modal.classList.remove(this.class);
    this.showButton.style.transform = "scale(1.1)";
    this.showButton.style.borderWidth = "0.2rem";
    this.showButton.style.borderColor = "#ffffffaa";
    // Focus Management
    this.modal.setAttribute("tabindex", "-1"); // Make modal focusable
    this.modal.focus(); // Set focus on the modal after it's visible
    setTimeout(() => {
      this.backdrop.classList.remove(this.delayedClass);
      this.modal.classList.remove(this.delayedClass);
    }, this.delay / 4); // Optional: Adjust delay for entering animations
  }
  delayHideModal() {
    console.log(`Hiding modal with ID "${this.modalId}"`);
    this.backdrop.classList.add(this.delayedClass);
    this.modal.classList.add(this.delayedClass);
    this.showButton.style.transform = "scale(1)";
    this.showButton.style.transform = "";
    this.showButton.style.borderWidth = "";
    this.showButton.style.borderColor = "";
    setTimeout(() => {
      this.backdrop.classList.add(this.class);
      this.modal.classList.add(this.class);
    }, this.delay);
  }
  static initAll() {
    document.querySelectorAll("[data-toggle='modal']").forEach((button) => {
      const modalId = button.getAttribute("data-target");
      if (!modalId) {
        console.error("Modal button found without a data-target attribute.");
      } else {
        new Modal(modalId, {
          class: "hidden",
          delayedClass: "opacity-0",
          delay: 300,
        });
      }
    });
  }
}
