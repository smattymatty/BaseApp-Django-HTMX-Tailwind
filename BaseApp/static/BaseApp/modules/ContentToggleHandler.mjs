/**
 * ContentToggleHandler: A class to manage togglable content elements with various trigger and close options.
 *
 * Usage:
 * 1. Create a container element with an ID ending in "-toggle-container".
 * 2. Add a trigger element (e.g., button) with an ID ending in "-toggle-trigger" inside the container.
 * 3. Add a content element with an ID ending in "-toggle-content" inside the container.
 * 4. Set data attributes on the container to customize behavior:
 *    - data-trigger-event: "click" (default) or "hover"
 *    - data-close-event: "mouseleave" (default) or "click"
 *    - data-active-class-for-button: CSS class(es) to apply to the trigger when content is shown
 *    - data-active-class-for-content: CSS class(es) to apply to the content when shown
 *    - data-delayed-active-class-for-content: CSS class(es) to apply to the content after a delay when shown
 *    - data-animation-delay: Delay in milliseconds for applying delayed classes (default: 50)
 *    - data-close-others: "true" or "false" (default) - whether to close other open toggles when this one opens
 *    - data-handle-outside-click: "true" or "false" (default) - whether to close on clicks outside the container
 *                                 (only applies when data-close-event is "click")
 * 
 * 5. Initialize the toggle(s) by calling ContentToggleHandler.initAll() in your JavaScript:
 *    - To initialize all toggles: ContentToggleHandler.initAll()
 *    - To initialize specific toggle(s): ContentToggleHandler.initAll('toggle-id-1 toggle-id-2')
 *
 * Example HTML:
 * <div id="my-toggle-container"
 *      data-trigger-event="click"
 *      data-close-event="click"
 *      data-active-class-for-button="bg-blue-500"
 *      data-active-class-for-content="opacity-100"
 *      data-delayed-active-class-for-content="translate-y-0"
 *      data-animation-delay="100"
 *      data-close-others="false"
 *      data-handle-outside-click="true">
 *   <button id="my-toggle-trigger">Toggle</button>
 *   <div id="my-toggle-content" class="hidden">
 *     Toggle content here
 *   </div>
 * </div>
 *
 * Example JavaScript:
 * import { ContentToggleHandler } from "./ContentToggleHandler.mjs";
 * ContentToggleHandler.initAll('my-toggle');
 */

const DEBUG = true;

export class ContentToggleHandler {
  static instances = [];

  constructor(config) {
    this.containerId = config.containerId;
    this.container = document.getElementById(`${this.containerId}-toggle-container`);
    this.triggerEvent = config.triggerEvent || "click";
    this.closeEvent = config.closeEvent || "mouseleave";
    this.activeClassForButton = config.activeClassForButton || "";
    this.activeClassForContent = config.activeClassForContent || "";
    this.delayedActiveClassForContent = config.delayedActiveClassForContent || "";
    this.animationDelay = config.animationDelay || 50; // milliseconds
    this.closeOthers = config.closeOthers || false;
    this.shouldHandleOutsideClick = config.handleOutsideClick || false;


    if (!this.container) {
      console.error(`[ContentToggleHandler Error] Container with ID "${this.containerId}-toggle-container" not found.`);
      return;
    }

    this.triggerElement = document.getElementById(`${this.containerId}-toggle-trigger`);
    this.contentElement = document.getElementById(`${this.containerId}-toggle-content`);

    if (!this.triggerElement || !this.contentElement) {
      console.error(`[ContentToggleHandler Error] Missing trigger or content element in container "${this.containerId}".`);
      return;
    }

    ContentToggleHandler.instances.push(this);
    this.init();
  }

  init() {
    if (DEBUG) console.log(`[DEBUG] Setting up event listeners for ${this.containerId}`);
  
    if (this.triggerEvent === "hover") {
      this.container.addEventListener("mouseenter", this.showContent.bind(this));
    } else {
      this.triggerElement.addEventListener("click", this.toggleContent.bind(this));
    }
  
    if (this.closeEvent === "mouseleave") {
      this.container.addEventListener("mouseleave", this.hideContent.bind(this));
    } else if (this.closeEvent === "click") {
      if (this.shouldHandleOutsideClick) {
        document.addEventListener("click", this.handleOutsideClick.bind(this));
      }
    }
  }

  showContent() {
    if (DEBUG) console.log(`[DEBUG] Showing content for ${this.containerId}, closeOthers: ${this.closeOthers}`);
    
    if (this.closeOthers) {
      if (DEBUG) console.log(`[DEBUG] Closing other instances for ${this.containerId}`);
      ContentToggleHandler.instances.forEach(instance => {
        if (instance !== this) {
          instance.hideContentWithoutClosingOthers();
        }
      });
    }

    this.contentElement.classList.remove("hidden");
    if (this.activeClassForButton) {
      this.triggerElement.classList.add(...this.activeClassForButton.split(' '));
    }
    if (this.activeClassForContent) {
      this.contentElement.classList.add(...this.activeClassForContent.split(' '));
    }
    if (this.delayedActiveClassForContent) {
      setTimeout(() => {
        this.contentElement.classList.add(...this.delayedActiveClassForContent.split(' '));
      }, this.animationDelay);
    }
  }

  hideContent() {
    if (DEBUG) console.log(`[DEBUG] Hiding content for ${this.containerId}`);

    if (this.delayedActiveClassForContent) {
      this.contentElement.classList.remove(...this.delayedActiveClassForContent.split(' '));
    }
    if (this.activeClassForContent) {
      this.contentElement.classList.remove(...this.activeClassForContent.split(' '));
    }
    if (this.activeClassForButton) {
      this.triggerElement.classList.remove(...this.activeClassForButton.split(' '));
    }
    setTimeout(() => {
      this.contentElement.classList.add("hidden");
    }, this.animationDelay);
  }

  toggleContent() {
    if (DEBUG) console.log(`[DEBUG] Toggling content for ${this.containerId}`);
  
    if (this.contentElement.classList.contains("hidden")) {
      this.showContent();
    } else {
      this.hideContentWithoutClosingOthers();
    }
  }
  
  hideContentWithoutClosingOthers() {
    if (DEBUG) console.log(`[DEBUG] Hiding content for ${this.containerId} without closing others`);
  
    if (this.delayedActiveClassForContent) {
      this.contentElement.classList.remove(...this.delayedActiveClassForContent.split(' '));
    }
    if (this.activeClassForContent) {
      this.contentElement.classList.remove(...this.activeClassForContent.split(' '));
    }
    if (this.activeClassForButton) {
      this.triggerElement.classList.remove(...this.activeClassForButton.split(' '));
    }
    setTimeout(() => {
      this.contentElement.classList.add("hidden");
    }, this.animationDelay);
  }
  handleOutsideClick(event) {
    if (!this.container.contains(event.target) && !this.contentElement.classList.contains("hidden")) {
      if (DEBUG) console.log(`[DEBUG] Outside click detected for ${this.containerId}`);
      this.hideContent();
    }
  }

  static initAll(containerFilter = "") {
    if (DEBUG) console.log(`[DEBUG] Initializing all ContentToggleHandlers with filter: "${containerFilter}"`);
    
    const initializedContainers = new Set();

    const initializeContainer = (containerId) => {
      if (initializedContainers.has(containerId)) return;

      const containerElement = document.getElementById(`${containerId}-toggle-container`);
      if (!containerElement) {
        console.error(`[ContentToggleHandler Error] Container with ID "${containerId}-toggle-container" not found.`);
        return;
      }

      if (DEBUG) console.log(`[DEBUG] Initializing ContentToggleHandler with ID "${containerElement.id}"`);
      
      const config = {
        containerId,
        triggerEvent: containerElement.dataset.triggerEvent || "click",
        closeEvent: containerElement.dataset.closeEvent || "mouseleave",
        activeClassForButton: containerElement.dataset.activeClassForButton || "",
        activeClassForContent: containerElement.dataset.activeClassForContent || "",
        delayedActiveClassForContent: containerElement.dataset.delayedActiveClassForContent || "",
        animationDelay: parseInt(containerElement.dataset.animationDelay) || 50,
        closeOthers: containerElement.dataset.closeOthers === "true",
        handleOutsideClick: containerElement.dataset.handleOutsideClick === "true",
      };
      if (DEBUG) console.log(`[DEBUG] Config for ${containerId}:`, config);
      new ContentToggleHandler(config);
      initializedContainers.add(containerId);
    };

    if (containerFilter) {
      if (containerFilter.includes(" ")) {
        containerFilter.split(" ").forEach(initializeContainer);
      } else {
        initializeContainer(containerFilter);
      }
    } else {
      document.querySelectorAll('[id$="-toggle-container"]').forEach((containerElement) => {
        initializeContainer(containerElement.id.replace("-toggle-container", ""));
      });
    }
  }
}