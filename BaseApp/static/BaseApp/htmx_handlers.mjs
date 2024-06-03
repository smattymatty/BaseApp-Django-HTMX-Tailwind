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

  triggerHtmxRequest() {
    // You can add the logic for triggering HTMX requests here,
    // based on the extracted attributes (e.g., using htmx.ajax())
    // For now, let's just log the attributes:
    console.log(
      `Triggering HTMX request for ${this.button.id} with attributes:`,
      this.htmxAttributes
    );
  }
}
