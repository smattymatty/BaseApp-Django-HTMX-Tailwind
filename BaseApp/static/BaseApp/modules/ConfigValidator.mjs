// configValidator.mjs
import { setup_logger } from './LoggingUtils.mjs';

const MODULE_NAME = 'configValidator';
const DEBUG = true;
const logger = setup_logger(MODULE_NAME, DEBUG);

export function validateConfig(config, schema) {
  const errors = [];

  for (const [key, rules] of Object.entries(schema)) {
    if (rules.required && !config.hasOwnProperty(key)) {
      const errorMessage = `Configuration error: The "${key}" field is required. Please provide a value for "${key}".`;
      logger.error(errorMessage, 'validateConfig');
      errors.push(errorMessage);
    }

    if (
      config.hasOwnProperty(key) &&
      rules.type &&
      typeof config[key] !== rules.type
    ) {
      const errorMessage = `Configuration error: The "${key}" field must be of type ${
        rules.type
      }. Received type: ${typeof config[key]}.`;
      logger.error(errorMessage, 'validateConfig');
      errors.push(errorMessage);
    }

    if (rules.validator && !rules.validator(config[key])) {
      const errorMessage = `Configuration error: The "${key}" field failed custom validation. Received value: ${config[key]}.`;
      logger.error(errorMessage, 'validateConfig');
      errors.push(errorMessage);
    }
  }

  if (errors.length > 0) {
    throw new Error(errors.join('\n'));
  }

  logger.info('Config validation passed', 'validateConfig');
  return true;
}
