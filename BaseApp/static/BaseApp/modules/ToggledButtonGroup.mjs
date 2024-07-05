import { initialActiveStrategies } from "./strategies.mjs";
import { HtmxHandler } from "./HtmxHandler.mjs";
import { logger } from "./LoggingUtils.mjs";
const MODULE_NAME = 'ToggledButtonGroup';
const DEBUG = false;
/**
 * A class to manage a group of buttons that toggle an 'active' class
 * and optionally trigger HTMX requests.
 *
 * Usage:
 *   1. Create a button group container element in your HTML with an ID ending in "-toggled-button-group".
 *   2. Add "button" elements inside the container.
 *   3. (Optional) Set `data-active-class` on the container to customize the active class (default is "active").
 *   4. (Optional) Set `data-initial-active` on the container to define the initially active button (options: "first", "last", "none", "random" or a number for the button index).
 *   5. (Optional) Add HTMX attributes (e.g., `hx-get`, `hx-target`) to buttons to trigger HTMX requests.
 *   6. Call `ToggledButtonGroup.initAll()` to initialize all button groups on the page.
 */
export class ToggledButtonGroup {
  constructor(config) {
    logger.info(`Initializing "${config.groupId}-toggled-button-group"`,
      MODULE_NAME, 'constructor');
    this.groupId = config.groupId;
    this.container = document.getElementById(
      `${this.groupId}-toggled-button-group`
    );
    if (!this.container) {
      logger.error(`Button group container with ID "${this.groupId}-toggled-button-group" not found. Please ensure the container element exists and has the correct ID.`, MODULE_NAME, 'constructor');
    }
    this.buttons = this.container
      ? this.container.querySelectorAll("button")
      : [];
    this.activeClass = config.activeClass || "active";
    this.initialActive = config.initialActive || "none";
    this.htmxHandlers = [];
    const buttonIds = new Set(); // Use a Set to track unique IDs
    for (const button of this.buttons) {
      if (buttonIds.has(button.id) && button.id !== "") {
        logger.error(`Duplicate button ID "${button.id}" found in group "${this.groupId}". Each button must have a unique ID.`, MODULE_NAME, 'constructor');
      }
      buttonIds.add(button.id);
    }
    const validInitialActiveValues = [
      "first",
      "last",
      "none",
      "random",
      ...Array.from({ length: this.buttons.length }, (_, i) => i.toString()),
    ];
    if (!validInitialActiveValues.includes(this.initialActive)) {
      logger.error(`Invalid data-initial-active value "${this.initialActive}" for group "${this.groupId}". Valid values are: ${validInitialActiveValues.join(", ")}`, MODULE_NAME, 'constructor');
      return;
    }
    if (this.htmxHandlers.length > 0 && typeof htmx === "undefined") {
      //check if the array buttonsWithHxAttributes is empty and if the type of the var htmx is undefined
      logger.error(`HTMX attributes found, but the HTMX library is not included. Please make sure to include the HTMX JavaScript library before using this component.`, MODULE_NAME, 'constructor');
      return;
    }
    this.init();
  }
  init() {
    if (!this.buttons.length) {
      logger.error(`Button group with ID "${this.groupId}" has no buttons.`);
      return;
    }
    if (this.activeClass.trim() === "") {
      logger.warning(`Active class for button group "${this.groupId}" is empty or invalid. Using default "active" class.`);
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
    this.setupHTMXHandlers();
    this.setInitialActiveButton();
  }
  setInitialActiveButton() {
    // strategy is a function that returns the button to be active
    const strategy = initialActiveStrategies[this.initialActive];
    // DEBUG
    if (DEBUG) {
      console.log(`Initial active button strategy: ${strategy}`);
    }
    // ERROR CHECKING
    if (!strategy) {
      logger.error(`Invalid initial_active option "${this.initialActive}".`, MODULE_NAME, 'setInitialActiveButton', 5);
      return;
    }
    // Set initial active button
    const initialButton = strategy(this.buttons, this.initialActive);
    if (initialButton) {
      this.setActiveButton(initialButton);
      // **New: Explicitly trigger the HTMX request for the initial active button**
      const buttonIndex = Array.from(this.buttons).indexOf(initialButton);
      if (buttonIndex !== -1 && this.htmxHandlers[buttonIndex]) {
        this.htmxHandlers[buttonIndex].triggerHtmxRequest();
      }
    }
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
}

ToggledButtonGroup.initAll = function (groupFilter = "") {
  if (DEBUG) {
    logger.startTimer('ToggledButtonGroup.initAll');
  }
  // Use this to Initialize all button groups
  // with an empty string, it will check for all elements with the ID ending in "-toggled-button-group"
  // given a string as argument, it will only check for elements with the ID starting with the string and ending in "-toggled-button-group"
  // if the string includes spaces, it will split the string and call itself recursively
  const initializedGroups = new Set();
  const initializeGroup = (groupId) => {
    if (initializedGroups.has(groupId)) return; // Skip if already initialized
    const groupElement = document.getElementById(
      `${groupId}-toggled-button-group`
    );
    if (!groupElement) {
      logger.error(`Button group container with ID "${groupId}-toggled-button-group" not found.`, MODULE_NAME, 'initAll');
      return;
    }
    const config = {
      groupId,
      activeClass: groupElement.dataset.activeClass || "active",
      initialActive: groupElement.dataset.initialActive || "none",
    };
    new ToggledButtonGroup(config);
    initializedGroups.add(groupId); // Mark as initialized
  };
  if (groupFilter) {
    if (groupFilter.includes(" ")) {
      const groupFilterList = groupFilter.split(" ");
      groupFilterList.forEach(initializeGroup);
    } else {
      initializeGroup(groupFilter);
    }
  } else {
    // Initialize all groups if no filter is provided
    document
      .querySelectorAll('[id$="-toggled-button-group"]')
      .forEach((groupElement) => {
        initializeGroup(groupElement.id.replace("-toggled-button-group", ""));
      });
  }
  if (DEBUG) {
    logger.endTimer('ToggledButtonGroup.initAll');
  }
};
