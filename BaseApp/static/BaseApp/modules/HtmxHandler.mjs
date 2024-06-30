const DEBUG = false;

export class HtmxHandler {
  constructor(button) {
    this.button = button;
    this.htmxAttributes = {};
    this.extractHtmxAttributes();
  }

  extractHtmxAttributes() {
    for (const attr of this.button.attributes) {
      if (attr.name.startsWith("hx-")) {
        this.htmxAttributes[attr.name] = attr.value;
      }
    }
  }
  // TODO: DEBUG Uncaught TypeError: this.htmxHandlers[buttonIndex].triggerHtmxRequest is not a function
  triggerHtmxRequest() {
    // DEBUG
    if (DEBUG) {
      console.log(`Triggering HTMX request for button ${this.button.id}`);
      console.log(`HTMX attributes: ${JSON.stringify(this.htmxAttributes)}`);
      console.log(`Method: ${this.htmxAttributes["hx-post"] ? "POST" : "GET"}`);
      console.log(
        `URL: ${
          this.htmxAttributes["hx-post"] ||
          this.htmxAttributes["hx-get"] ||
          this.htmxAttributes["hx-boost"]
        }`
      );
    }
    const hasValidRequestAttribute =
      this.htmxAttributes["hx-get"] ||
      this.htmxAttributes["hx-post"] ||
      this.htmxAttributes["hx-boost"];
    // ERROR CHECKING
    if (!this.button || !this.htmxAttributes || !hasValidRequestAttribute) {
      console.error(
        `Error: Button ${
          this.button ? this.button.id : "unknown"
        } is missing required HTMX attributes. Make sure it has hx-get and is present on the page.`
      );
      return;
    }
    const triggerAttr = this.htmxAttributes["hx-trigger"];
    const validTriggers = ["click", "load", "mousedown"];
    if (triggerAttr && !validTriggers.includes(triggerAttr)) {
      console.warn(
        `[ToggledButtonGroup Warning] Unsupported hx-trigger value "${triggerAttr}" on button ${
          this.button.id
        }. Supported triggers are: ${validTriggers.join(", ")}`
      );
    }
    if (this.htmxAttributes["hx-get"] && this.htmxAttributes["hx-post"]) {
      console.warn(
        `[ToggledButtonGroup Warning] Button ${this.button.id} has both hx-get and hx-post attributes. This might lead to unexpected behavior. Consider using hx-boost for POST requests.`
      );
    }
    const targetId = this.htmxAttributes["hx-target"];
    if (targetId && !document.querySelector(targetId)) {
      console.error(
        `[ToggledButtonGroup Error] The target element "${targetId}" for button ${this.button.id} was not found. Please ensure the target exists.`
      );
      return;
    }
    // Determine the request type based on hx-boost or hx-get or hx-post
    const method = this.htmxAttributes["hx-post"] ? "POST" : "GET";
    const url =
      this.htmxAttributes["hx-post"] ||
      this.htmxAttributes["hx-get"] ||
      this.htmxAttributes["hx-boost"];
    // Trigger the HTMX request using htmx.ajax()
    htmx.ajax(method, url, {
      target: this.htmxAttributes["hx-target"],
      swap: this.htmxAttributes["hx-swap"],
      source: this.button, // Set the source element
    });
  }
}
