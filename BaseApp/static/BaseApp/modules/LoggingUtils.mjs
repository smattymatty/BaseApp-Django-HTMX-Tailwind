// Logger.mjs
// TODO: Add support for custom logger configurations via python settings

const LOG_LEVELS = {
  DEBUG: 0,
  INFO: 1,
  WARNING: 2,
  ERROR: 3,
  CRITICAL: 4,
};

class Logger {
  constructor(options = {}) {
    this.moduleName = options.moduleName;
    this.logLevel = options.logLevel || LOG_LEVELS.DEBUG;
    this.useColors = options.useColors !== undefined ? options.useColors : true;
    this.logToFile = options.logToFile || false;
    this.fileStream = null;
    // TODO: Add functionality to filter logs based on module name, log level, or other criteria
    if (this.logToFile) {
      // Implementation for file logging would go here
      // TODO: Implement file logging
      // TODO: Implement log rotation (e.g., rotate logs daily, weekly, or when they reach a certain size)
    }
  }
  // TODO: Allow users to add custom annotations or tags to log messages
  // TODO: Integrate performance monitoring (e.g., measure and log execution time of functions)
  // TODO: Implement asynchronous logging to avoid blocking main thread execution
  // TODO: Develop a web-based dashboard to view and analyze aggregated log data
  // TODO: Add support for hierarchical loggers (e.g., per-module loggers with inherited configurations)
  // TODO: Add the ability to configure different log levels and settings for development, staging, and production environments
  // TODO: Implement contextual logging to include request/session info or other contextual data in log messages
  // TODO: Add support for obfuscating sensitive data in logs (e.g., masks for credit card numbers)
  // TODO: Implement log buffering and batch writing to improve performance
  // TODO: Automatically log uncaught JavaScript errors and promise rejections
  log(message, functionName = null, level = LOG_LEVELS.INFO) {
    if (level < this.logLevel) return;

    const timestamp = new Date().toTimeString().split(' ')[0];
    // TODO: Allow customization of the timestamp format in log messages
    if (this.useColors) {
      this.colorLog(timestamp, level, functionName, message);
    } else {
      let logMessage = `${timestamp} ${Object.keys(LOG_LEVELS)[level]} `;
      if (this.moduleName) logMessage += `[${this.moduleName}] `;
      if (functionName) logMessage += `(${functionName}) `;
      logMessage += message;
      console.log(logMessage);
    }

    if (this.logToFile) {
      // Implementation for writing to file would go here
    }
  }

  colorLog(timestamp, level, functionName, message) {
    const styles = {
      timestamp: 'color: #6c757d', // Gray
      level: {
        [LOG_LEVELS.DEBUG]: 'color: #6c757d; font-weight: bold', // Gray
        [LOG_LEVELS.INFO]: 'color: #17a2b8; font-weight: bold', // Blue
        [LOG_LEVELS.WARNING]: 'color: #ffc107; font-weight: bold', // Yellow
        [LOG_LEVELS.ERROR]: 'color: #dc3545; font-weight: bold', // Red
        [LOG_LEVELS.CRITICAL]: 'color: #6f42c1; font-weight: bold', // Purple
      },
      module: 'color: #28a745', // Green
      function: 'color: #fd7e14', // Orange
      message: {
        [LOG_LEVELS.DEBUG]: 'color: #fffff',
        [LOG_LEVELS.INFO]: 'color: #ffffff',
        [LOG_LEVELS.WARNING]: 'color: #ffffff',
        [LOG_LEVELS.ERROR]: 'color: #ffffff',
        [LOG_LEVELS.CRITICAL]: 'color: #ffffff',
      },
    };

    let logParts = [`%c${timestamp}`, `%c${Object.keys(LOG_LEVELS)[level]}`];
    let styleArgs = [styles.timestamp, styles.level[level]];

    if (this.moduleName) {
      logParts.push(`%c[${this.moduleName}]`);
      styleArgs.push(styles.module);
    }
    if (functionName) {
      logParts.push(`%c(${functionName})`);
      styleArgs.push(styles.function);
    }

    logParts.push(`%c${message}`);
    styleArgs.push(styles.message[level]);

    console.log(logParts.join(' '), ...styleArgs);

    if (this.logToFile) {
      // Implementation for writing to file would go here
    }
  }

  debug(message, functionName = null) {
    this.log(message, functionName, LOG_LEVELS.DEBUG);
  }

  info(message, functionName = null) {
    this.log(message, functionName, LOG_LEVELS.INFO);
  }

  warning(message, functionName = null) {
    this.log(message, functionName, LOG_LEVELS.WARNING);
  }

  error(message, functionName = null) {
    this.log(message, functionName, LOG_LEVELS.ERROR);
  }

  critical(message, functionName = null) {
    this.log(message, functionName, LOG_LEVELS.CRITICAL);
    // TODO: Implement email alerts for critical logs
  }

  startTimer(label) {
    console.time(label);
  }

  endTimer(label) {
    console.timeEnd(label);
  }
}

export function setup_logger(module_name, debug = false) {
  const log_level = debug ? LOG_LEVELS.DEBUG : LOG_LEVELS.INFO;
  return new Logger({
    moduleName: module_name,
    logLevel: log_level,
    useColors: true,
    logToFile: false,
  });
}

export const logger = new Logger();
export default Logger;
