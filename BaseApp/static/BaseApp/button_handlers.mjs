import { initialActiveStrategies } from "./strategies.mjs";
// Strategies for initial active button
// ( first, last, none, random, 0-100, etc. )
export class ToggledButtonGroup {
  constructor(groupId, activeClass = "active", initialActive = "none") {
    this.groupId = groupId;
    this.container = document.getElementById(`${groupId}-button-group`);
    this.buttons = this.container
      ? this.container.querySelectorAll("button")
      : []; // Get buttons inside
    this.activeClass = activeClass;
    // ERROR CHECKING
    if (!this.container) {
      console.error(
        `Error: Button group container with ID "${groupId}-button-group" not found. Make sure the HTML element exists with the correct ID.`
      );
      return; // Exit constructor since we can't proceed without a container.
    }
    this.initialActive = initialActive;

    this.htmxHandlers = {};

    this.setInitialActiveButton();

    this.init();
  }

  init() {
    // ERROR CHECKING
    if (!this.buttons.length) {
      console.error(`Button group with ID "${this.groupId}" not found.`);
      return;
    }
    // WARNING CHECKING
    if (this.activeClass.trim() === "") {
      console.warn(
        `Warning: Active class for button group "${this.groupId}" is empty or invalid. Using default "active" class.`
      );
      this.activeClass = "active";
    }
    // When button is clicked, set active class
    this.container.addEventListener("mousedown", (event) => {
      const button = event.target.closest("button"); // Find the clicked button
      if (button && Array.from(this.buttons).includes(button)) {
        // Check if it's a valid button in the group
        this.setActiveButton(button);
      }
    });
  }

  setInitialActiveButton() {
    const strategy = initialActiveStrategies[this.initialActive];
    // ERROR CHECKING
    if (!strategy) {
      console.error(
        `Error: Invalid initial_active option "${this.initialActive}".`
      );
      return;
    }
    this.setupHTMXHandlers();
  }

  setActiveButton(button) {
    const classesToAdd = this.activeClass.split(" ").filter(Boolean);
    // Split and into an array of classes, filter out empty strings
    if (button.classList.contains(this.activeClass)) {
      this.deactivateAllButtons();
    } else {
      this.deactivateAllButtons();
      classesToAdd.forEach((className) => {
        button.classList.add(className);
      });
    }
  }

  deactivateAllButtons() {
    const classesToRemove = this.activeClass.split(" ").filter(Boolean);
    // Split and into an array of classes, filter out empty strings
    this.buttons.forEach((button) => {
      classesToRemove.forEach((className) => {
        button.classList.remove(className);
      });
    });
  }

  setupHTMXHandlers() {
    // Create htmxHandlers object (modified)
    Array.from(this.buttons).forEach((button, index) => {
      this.htmxHandlers[index] = {};
      // Convert to array for indexing
      let hasHxAttribute = false;
      const buttonText = button.textContent.trim() || `button-${index}`;
      for (const attr of button.attributes) {
        console.log(`Button ${button.id} has attribute ${attr.name}`);
        if (attr.name.startsWith("hx-")) {
          hasHxAttribute = true;
          this.htmxHandlers[index]["name"] = buttonText;
          this.htmxHandlers[index][attr.name] = attr.value;
        }
      }

      if (hasHxAttribute) {
        console.log(`Found button with hx- attribute: ${button.id}`);
        console.log(this.htmxHandlers[index]); // Log using the key
      }
    });
  }
}

ToggledButtonGroup.initAll = function (groupFilter = "") {
  // Use this to Initialize all button groups
  // with an empty string, it will check for all elements with the ID ending in "-button-group"
  // given a string as argument, it will only check for elements with the ID ending in "-button-group" and the string
  // if the string includes spaces, it will split the string and call itself recursively
  let selector = "[id$='-button-group']";
  if (groupFilter) {
    if (groupFilter.includes(" ")) {
      //split into an array of strings
      const groupFilterList = groupFilter.split(" ");
      groupFilterList.forEach((groupFilter) => {
        // call self recursively
        ToggledButtonGroup.initAll(groupFilter);
      });
    } else {
      selector = `#${groupFilter}-button-group`;
    }
  }
  // ERROR CHECKING
  const groups = document.querySelectorAll(selector);
  if (!groups.length) {
    if (groupFilter) {
      console.error(
        `Error: No button group found with the filter "${groupFilter}-button-group". Check the ID and filter string.`
      );
    } else {
      console.error(
        `Error: No button groups found on the page. Make sure elements with the ID pattern "*-button-group" exist.`
      );
    }
    return;
  }
  // Initialize all button groups
  document.querySelectorAll(selector).forEach((group) => {
    console.log(`Initializing ToggledButtonGroup with ID "${group.id}"`);
    const groupId = group.id.replace("-button-group", "");
    const activeClass = group.dataset.activeClass || "active";
    const initialActive = group.dataset.initialActive || "none";
    // Create new class instance
    new ToggledButtonGroup(groupId, activeClass, initialActive);
  });
};
