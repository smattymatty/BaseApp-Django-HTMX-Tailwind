// BaseApp/static/BaseApp/modules/strategies.mjs

import { setup_logger } from './LoggingUtils.mjs';

const MODULE_NAME = 'strategies';
const DEBUG = true;
const logger = setup_logger(MODULE_NAME, DEBUG);

export const initialActiveStrategies = {
  all: (items) => {
    if (items.length === 0) {
      logger.warning("No items found for 'all' strategy", 'all');
    }
    return items;
  },
  first: (items) => {
    const item = items[0];
    if (!item) logger.warning('No first item found', 'first');
    return item;
  },
  last: (items) => {
    const item = items[items.length - 1];
    if (!item) logger.warning('No last item found', 'last');
    return item;
  },
  none: (items) => null,
  random: (items) => {
    if (items.length === 0) {
      logger.warning('No items available for random selection', 'random');
      return null;
    }
    return items[Math.floor(Math.random() * items.length)];
  },
};

// Dynamically generate strategies for specific indices
for (let i = 0; i <= 100; i++) {
  initialActiveStrategies[i] = (items) => {
    const item = items[i];
    if (!item) logger.warning(`No button at index ${i} found`, `index${i}`);
    return item;
  };
}

// Add strategy to search for button by text content
initialActiveStrategies.byText = (items, text) => {
  const item = items.find((item) => item.textContent.trim() === text);
  if (!item) logger.warning(`No button with text "${text}" found`, 'byText');
  return item;
};

export const VALID_STRATEGIES = Object.keys(initialActiveStrategies);
