import { initialActiveStrategies } from "./strategies.mjs";
import { HtmxHandler } from "./htmx_handlers.mjs";

const DEBUG = true;
export class ToggledButtonGroup {
  constructor(config) {
    this.groupId = config.groupId;
    this.container = document.getElementById(`${this.groupId}-button-group`);
    this.buttons = this.container
      ? this.container.querySelectorAll("button")
      : [];
    this.activeClass = config.activeClass || "active";
    this.initialActive = config.initialActive || "none";
    this.htmxHandlers = {};
    // ERROR CHECKING
    if (!this.container) {
      console.error(
        `Error: Button group container with ID "${groupId}-button-group" not found. Make sure the HTML element exists with the correct ID.`
      );
      return; // Exit constructor since we can't proceed without a container.
    }
    this.setInitialActiveButton();
    if (DEBUG) {
      console.log(`htmxHandlers = ${JSON.stringify(this.htmxHandlers)}`);
    }
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
    // DEBUG
    if (DEBUG) {
      console.log(`Initial active button strategy: ${strategy}`);
    }
    // ERROR CHECKING
    if (!strategy) {
      console.error(
        `Error: Invalid initial_active option "${this.initialActive}".`
      );
      return;
    }
    // Set initial active button
    const initialButton = strategy(this.buttons, this.initialActive);
    if (initialButton) {
      this.setActiveButton(initialButton);
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
        if (attr.name.startsWith("hx-")) {
          const new_HTMXHandler = new HtmxHandler(button);
          hasHxAttribute = true;
          this.htmxHandlers[index] = new_HTMXHandler;
        }
      }
    });
  }
  triggerHtmxEvent(button) {
    const handler = this.htmxHandlers[button.textContent.trim()];
    if (handler) {
      handler.triggerHtmxRequest(); // Call the triggerHtmxRequest method on the appropriate handler
    }
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
    const config = {
      groupId: group.id.replace("-button-group", ""),
      activeClass: group.dataset.activeClass || "active",
      initialActive: group.dataset.initialActive || "none",
    };
    // Create new class instance
    new ToggledButtonGroup(config);
  });
};
