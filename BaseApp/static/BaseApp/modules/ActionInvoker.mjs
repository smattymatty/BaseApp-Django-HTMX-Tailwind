// BaseApp/static/BaseApp/modules/ActionInvoker.mjs

import { setup_logger } from './LoggingUtils.mjs';
import { validateConfig } from './ConfigValidator.mjs';
import { initialActiveStrategies, VALID_STRATEGIES } from './strategies.mjs';

const MODULE_NAME = 'ActionInvoker';
const DEBUG = true;
const logger = setup_logger(MODULE_NAME, DEBUG);

// TODO: Implement debouncing for event handling to prevent rapid-fire execution
// TODO: Add support for animations when actions like 'show', 'hide', 'toggleClass', etc. are triggered
// TODO: Add support for conditional actions based on element state or other criteria
// TODO: Implement chainable actions so multiple actions can be defined in sequence for the same event
// TODO: Add support for responsive actions that adapt to different screen sizes or orientations
// TODO: Implement detailed logging for each action taken, including timestamps and context
// TODO: Add support for reversing actions (undo functionality)
// TODO: Implement the ability to dynamically bind events to new elements added to the DOM
// TODO: Design a plugin architecture to allow custom actions and strategies to be added by third-party developers
// TODO: Integrate with a state management library to synchronize the state across different components
// TODO: Track user interactions and gather analytics on which actions are most frequently executed
// TODO: Implement an error reporting mechanism to capture and report errors encountered during action execution
// TODO: Add support for handling concurrent actions and resolving conflicts
// TODO: Develop a graphical user interface to create and manage ActionInvoker configurations
// TODO: Allow users to define and trigger custom events within the ActionInvoker framework

export class ActionInvoker {
  constructor(config) {
    // Validate config schema
    const configSchema = {
      event: { required: true, type: 'string' },
      action: { required: true, type: 'string' },
      targetId: { required: true, type: 'string' },
      strategy: {
        required: false,
        type: 'string',
        validator: (val) => VALID_STRATEGIES.includes(val),
      },
    };

    try {
      validateConfig(config, configSchema);
    } catch (error) {
      logger.error(`Config validation failed: ${error.message}`, 'constructor');
      // Provide additional context for the user
      throw new Error(
        `ActionInvoker configuration error: ${error.message}. Please ensure the configuration is correct based on the expected schema.`
      );
    }

    this.event = config.event;
    this.action = config.action;
    this.targetId = config.targetId;
    this.strategy = config.strategy || 'all';

    logger.info('ActionInvoker instance created successfully', 'constructor');
    this.init();
  }

  init() {
    document.addEventListener('DOMContentLoaded', () => {
      const target = document.getElementById(this.targetId);
      if (target) {
        if (this.event === 'on-load') {
          this.handleOnLoad(target);
        }
        // TODO: Add support for other events like 'on-scroll-top', 'on-scroll-bottom', 'on-scroll-middle', 'on-hover', 'on-click', etc.
      } else {
        logger.error(
          `Target element with id "${this.targetId}" not found.`,
          'init'
        );
      }
    });
  }

  handleOnLoad(target) {
    logger.info(
      `Handling on-load event for target "${this.targetId}"`,
      'handleOnLoad'
    );
    switch (this.action) {
      case 'click':
        this.clickButtons(target);
        break;
      // TODO: Implement additional action types such as 'hide', 'show', 'addClass', 'removeClass', 'toggleClass', etc.
      default:
        logger.warning(`Unknown action: ${this.action}`, 'handleOnLoad');
    }
  }

  clickButtons(target) {
    logger.info(
      `Clicking buttons for target "${this.targetId}" with strategy "${this.strategy}"`,
      'clickButtons'
    );
    const buttons = this.getButtonsToAct(target);
    buttons.forEach((button) => button.click());
    // TODO: Add support for delayed or sequential button clicking based on configuration
  }

  getButtonsToAct(target) {
    const allButtons = Array.from(target.querySelectorAll('button'));
    if (this.strategy === 'all') {
      return allButtons;
    } else if (initialActiveStrategies.hasOwnProperty(this.strategy)) {
      const button = initialActiveStrategies[this.strategy](allButtons);
      return button ? [button] : [];
    } else {
      const errorMessage = `Unknown strategy: ${
        this.strategy
      }. Please use one of the valid strategies: ${VALID_STRATEGIES.join(
        ', '
      )}.`;
      logger.error(errorMessage, 'getButtonsToAct');
      return [];
    }
  }

  static initAll(configs) {
    logger.info(
      `Initializing ${configs.length} ActionInvoker instances`,
      'initAll'
    );
    configs.forEach((config) => new ActionInvoker(config));
  }
}
