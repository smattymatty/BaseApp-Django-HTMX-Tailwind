class NavbarDropdown {
  constructor(buttonId, dropdownId, options = {}) {
    this.button = document.getElementById(buttonId);
    this.dropdown = document.getElementById(dropdownId);
    this.class = options.class || "active";
    this.delayedClass = options.delayedClass || "visible";
    this.delay = options.delay || 100;
    this.isMouseInButton = false;
    this.isMouseInDropdown = false;

    this.init();
  }

  init() {
    this.button.addEventListener("mouseenter", () => {
      this.isMouseInButton = true;
      this.showDropdown();
    });
    this.button.addEventListener("mouseleave", () => {
      this.isMouseInButton = false;
      this.delayHideDropdown();
    });

    this.dropdown.addEventListener("mouseenter", () => {
      this.isMouseInDropdown = true;
    });
    this.dropdown.addEventListener("mouseleave", () => {
      this.isMouseInDropdown = false;
      this.delayHideDropdown();
    });
  }

  showDropdown() {
    this.dropdown.classList.remove(this.class);
    setTimeout(() => {
      this.dropdown.classList.remove(this.delayedClass);
    }, this.delay);
  }

  delayHideDropdown() {
    setTimeout(() => {
      if (!this.isMouseInButton && !this.isMouseInDropdown) {
        this.hideDropdown();
      }
    }, this.delay);
  }

  hideDropdown() {
    this.dropdown.classList.add(this.delayedClass);
    setTimeout(() => {
      this.dropdown.classList.add(this.class);
    }, this.delay);
  }
}

function initNavbarDropdown(navButtonId, navDropdownId) {
  const navButton = document.getElementById(navButtonId);
  const navDropdown = document.getElementById(navDropdownId);

  if (navButton && navDropdown) {
    return new NavbarDropdown(navButtonId, navDropdownId, {
      class: "hidden",
      delayedClass: "opacity-0",
    });
  } else {
    console.warn(
      `Navbar elements with IDs '${navButtonId}' and '${navDropdownId}' were not found.`
    );
    return null;
  }
}

// Define the maximum number of NavbarDropdowns you might have
const maxNavItems = 5;
const navInstances = [];

for (let i = 1; i <= maxNavItems; i++) {
  const navButtonId = `nav-button-${i}`;
  const navDropdownId = `nav-dropdown-${i}`;
  const navInstance = initNavbarDropdown(navButtonId, navDropdownId);
  if (navInstance) {
    navInstances.push(navInstance);
  }
}

// navInstances now contains all initialized NavbarDropdowns
