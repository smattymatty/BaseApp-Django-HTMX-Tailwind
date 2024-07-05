import { setup_logger } from './LoggingUtils.mjs';
import { validateConfig } from './ConfigValidator.mjs';
const MODULE_NAME = 'ContentToggleHandler';
const DEBUG = true;
const logger = setup_logger(MODULE_NAME, DEBUG);
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

export class ContentToggleHandler {
  static instances = [];

  constructor(config) {
    // TODO: add validation for config

    this.containerId = config.containerId;
    this.container = document.getElementById(
      `${this.containerId}-toggle-container`
    );
    this.triggerEvent = config.triggerEvent || 'click';
    this.closeEvent = config.closeEvent || 'mouseleave';
    this.activeClassForButton = config.activeClassForButton || '';
    this.activeClassForContent = config.activeClassForContent || '';
    this.delayedActiveClassForContent =
      config.delayedActiveClassForContent || '';
    this.animationDelay = config.animationDelay || 50; // milliseconds
    this.closeOthers = config.closeOthers || false;
    this.shouldHandleOutsideClick = config.handleOutsideClick || false;
    this.toggleType = config.toggleType || 'hidden';

    if (!this.container) {
      logger.error(
        `[ContentToggleHandler Error] Container with ID "${this.containerId}-toggle-container" not found.`,
        'constructor'
      );
      return;
    }

    this.triggerElement = document.getElementById(
      `${this.containerId}-toggle-trigger`
    );
    this.contentElement = document.getElementById(
      `${this.containerId}-toggle-content`
    );

    if (!this.triggerElement || !this.contentElement) {
      logger.error(
        `[ContentToggleHandler Error] Missing trigger or content element in container "${this.containerId}".`
      );
      return;
    }

    ContentToggleHandler.instances.push(this);
    this.init();
  }

  init() {
    if (DEBUG)
      logger.debug(
        `Setting up event listeners for ${this.containerId}`,
        'init'
      );

    if (this.triggerEvent === 'hover') {
      this.container.addEventListener(
        'mouseenter',
        this.showContent.bind(this)
      );
    } else {
      this.triggerElement.addEventListener(
        'click',
        this.toggleContent.bind(this)
      );
    }

    if (this.closeEvent === 'mouseleave') {
      this.container.addEventListener(
        'mouseleave',
        this.hideContent.bind(this)
      );
    } else if (this.closeEvent === 'click') {
      if (this.shouldHandleOutsideClick) {
        document.addEventListener('click', this.handleOutsideClick.bind(this));
      }
    } else if (this.closeEvent === 'none') {
      // do nothing
    } else {
      logger.error(
        `[ContentToggleHandler Error] Invalid closeEvent: "${this.closeEvent}".`,
        'constructor'
      );
      return;
    }
  }

  showContent() {
    if (DEBUG)
      logger.debug(
        `Showing content for ${this.containerId}, closeOthers: ${this.closeOthers}`,
        'showContent'
      );

    if (this.closeOthers) {
      ContentToggleHandler.instances.forEach((instance) => {
        if (instance !== this) {
          instance.hideContentWithoutClosingOthers();
        }
      });
    }

    // Remove hidden class immediately if using hidden toggle type
    if (this.toggleType === 'hidden') {
      this.contentElement.classList.remove('hidden');
    }

    // Use requestAnimationFrame to ensure the browser has time to process the removal of 'hidden'
    requestAnimationFrame(() => {
      if (this.activeClassForButton) {
        this.triggerElement.classList.add(
          ...this.activeClassForButton.split(' ')
        );
      }
      if (this.activeClassForContent) {
        this.contentElement.classList.add(
          ...this.activeClassForContent.split(' ')
        );
      }
      if (this.delayedActiveClassForContent) {
        setTimeout(() => {
          this.contentElement.classList.add(
            ...this.delayedActiveClassForContent.split(' ')
          );
        }, this.animationDelay);
      }
    });
  }

  hideContent() {
    if (DEBUG)
      logger.debug(`Hiding content for ${this.containerId}`, 'hideContent');

    if (this.delayedActiveClassForContent) {
      this.contentElement.classList.remove(
        ...this.delayedActiveClassForContent.split(' ')
      );
    }
    if (this.activeClassForContent) {
      this.contentElement.classList.remove(
        ...this.activeClassForContent.split(' ')
      );
    }
    if (this.activeClassForButton) {
      this.triggerElement.classList.remove(
        ...this.activeClassForButton.split(' ')
      );
    }

    if (this.toggleType === 'hidden') {
      setTimeout(() => {
        this.contentElement.classList.add('hidden');
      }, this.animationDelay);
    }
  }

  toggleContent() {
    if (DEBUG)
      logger.debug(`Toggling content for ${this.containerId}`, 'toggleContent');

    const isContentVisible =
      this.toggleType === 'hidden'
        ? !this.contentElement.classList.contains('hidden')
        : this.activeClassForContent
            .split(' ')
            .some((cls) => this.contentElement.classList.contains(cls));

    if (!isContentVisible) {
      this.showContent();
    } else {
      this.hideContent();
    }
  }

  hideContentWithoutClosingOthers() {
    if (DEBUG)
      logger.debug(
        `Hiding content for ${this.containerId} without closing others`,
        'hideContentWithoutClosingOthers'
      );

    if (this.delayedActiveClassForContent) {
      this.contentElement.classList.remove(
        ...this.delayedActiveClassForContent.split(' ')
      );
    }
    if (this.activeClassForContent) {
      this.contentElement.classList.remove(
        ...this.activeClassForContent.split(' ')
      );
    }
    if (this.activeClassForButton) {
      this.triggerElement.classList.remove(
        ...this.activeClassForButton.split(' ')
      );
    }
  }

  handleOutsideClick(event) {
    if (
      !this.container.contains(event.target) &&
      !this.contentElement.classList.contains('hidden')
    ) {
      if (DEBUG)
        logger.debug(
          `Outside click detected for ${this.containerId}`,
          'handleOutsideClick'
        );
      this.hideContent();
    }
  }

  static initAll(containerFilter = '') {
    if (DEBUG)
      logger.debug(
        `Initializing all ContentToggleHandlers with filter: "${containerFilter}"`,
        'initAll'
      );

    const initializedContainers = new Set();

    const initializeContainer = (containerId) => {
      if (initializedContainers.has(containerId)) return;

      const containerElement = document.getElementById(
        `${containerId}-toggle-container`
      );
      if (!containerElement) {
        logger.error(
          `Container with ID "${containerId}-toggle-container" not found.`,
          'initializeContainer'
        );
        return;
      }

      if (DEBUG)
        logger.debug(
          `Initializing ContentToggleHandler with ID "${containerElement.id}"`,
          'initializeContainer'
        );

      const config = {
        containerId,
        triggerEvent: containerElement.dataset.triggerEvent || 'click',
        closeEvent: containerElement.dataset.closeEvent || 'mouseleave',
        activeClassForButton:
          containerElement.dataset.activeClassForButton || '',
        activeClassForContent:
          containerElement.dataset.activeClassForContent || '',
        delayedActiveClassForContent:
          containerElement.dataset.delayedActiveClassForContent || '',
        animationDelay: parseInt(containerElement.dataset.animationDelay) || 50,
        closeOthers: containerElement.dataset.closeOthers === 'true',
        handleOutsideClick:
          containerElement.dataset.handleOutsideClick === 'true',
        toggleType: containerElement.dataset.toggleType || 'hidden',
      };
      if (DEBUG)
        logger.debug(
          `Config for ${containerId}: ${config}`,
          'initializeContainer'
        );
      new ContentToggleHandler(config);
      initializedContainers.add(containerId);
    };

    if (containerFilter) {
      if (containerFilter.includes(' ')) {
        containerFilter.split(' ').forEach(initializeContainer);
      } else {
        initializeContainer(containerFilter);
      }
    } else {
      document
        .querySelectorAll('[id$="-toggle-container"]')
        .forEach((containerElement) => {
          initializeContainer(
            containerElement.id.replace('-toggle-container', '')
          );
        });
    }
  }
}
