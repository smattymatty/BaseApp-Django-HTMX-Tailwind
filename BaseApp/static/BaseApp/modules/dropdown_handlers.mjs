const DEBUG = false;

/**
 * A class to manage dropdown menus where the parent element gets hovered and the dropdown menu appears.
 *
 * Usage:
 *   1. Create a dropdown container element in your HTML with an ID ending in "-dropdown".
 *   2. Place your dropdown menu items inside this container as buttons.
 *   3. (Optional) Add `data-dropdown-trigger="hover"` to the parent element to trigger the dropdown menu on hover. Else, default is click.
 *   4. (Optional) Add `data-active-class` to the dropdown container to customize the active button with tailwind CSS.
 *   5. Call `Dropdown.initAll()` to initialize all dropdowns on the page.
 *   6. (Optional) Add `data-active-class` to the dropdown container to customize the active button with tailwind CSS.
 */

export class Dropdown {
  constructor(config) {
    this.dropdownId = config.dropdownId;
    this.container = document.getElementById(`${this.dropdownId}-dropdown`);
    this.trigger = config.trigger || "click";
    this.items = this.container
      ? this.container.querySelectorAll("button")
      : [];
    this.activeClass = config.activeClass || "";
  }

  init() {
    // ERROR CHECKING
    if (!this.container) {
      console.error(
        `[Dropdown Error] Dropdown container with ID "${this.dropdownId}-dropdown" not found.`
      );
      return;
    }

    if (!this.items.length) {
      console.error(
        `[Dropdown Error] Dropdown container with ID "${this.dropdownId}-dropdown" has no items.`
      );
      return;
    }

    // WARNING CHECKING
    if (this.trigger !== "hover" && this.trigger !== "click") {
      console.warn(
        `[Dropdown Warning] Dropdown trigger "${this.trigger}" is not valid. Using default "click".`
      );
      this.trigger = "click";
    }

    if (this.close !== "click" && this.close !== "mouseleave") {
      console.warn(
        `[Dropdown Warning] Dropdown close "${this.close}" is not valid. Using default "mouseleave".`
      );
      this.close = "mouseleave";
    }

    // TRIGGER
    if (this.trigger === "hover") {
      this.container.addEventListener(
        "mouseenter",
        this.showDropdown.bind(this)
      );
    } else {
      // default is click
      this.container.addEventListener("click", this.showDropdown.bind(this));
    }

    // CLOSE
    if (this.close === "hover") {
      this.container.addEventListener(
        "mouseleave",
        this.hideDropdown.bind(this)
      );
    }
  }
}

Dropdown.initAll = function (dropdownFilter = "") {
  // Use this to Initialize all dropdowns
  // with an empty string, it will check for all elements with the ID ending in "-dropdown"
  // given a string as parameter, it will only look for elements with the ID starting with the string and ending in "-dropdown"
  // if the string includes spaces, it will split the string and call itself recursively
  const initializedDropdowns = new Set();

  const initializeGroup = (dropdownID) => {
    if (initializedDropdowns.has(dropdownID)) return; // Skip if already initialized

    const dropdownElement = document.getElementById(`${dropdownID}-dropdown`);
    if (!dropdownElement) {
      console.error(
        `[Dropdown Error] Dropdown container with ID "${dropdownID}-dropdown" not found.`
      );
      return;
    }

    console.log(`Initializing Dropdown with ID "${dropdownElement.id}"`);
    const config = {
      dropdownID,
      trigger: dropdownElement.dataset.trigger || "click",
      activeClass: dropdownElement.dataset.activeClass || "",
    };
    new Dropdown(config);
    initializedDropdowns.add(dropdownID);
  };

  if (dropdownFilter) {
    if (dropdownFilter.includes(" ")) {
      const dropdownFilterList = dropdownFilter.split(" ");
      dropdownFilterList.forEach(initializeGroup);
    } else {
      initializeGroup(dropdownFilter);
    }
  } else {
    // Initialize all dropdowns if no filter is provided
    document
      .querySelectorAll('[id$="-dropdown"]')
      .forEach((dropdownElement) => {
        initializeGroup(dropdownElement.id.replace("-dropdown", ""));
      });
  }
};
